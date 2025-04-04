# account_history/views.py
# 거래 내역 관련 API 뷰 정의

from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import AccountHistory
from accounts.models import Account
from .serializers import (
    AccountHistorySerializer,
    AccountHistoryUpdateSerializer,
    AccountHistoryFilterSerializer
)


class AccountHistoryListAPIView(generics.ListAPIView):
    """
    계좌 거래 내역 목록 조회 API

    사용자의 모든 계좌에 대한 거래 내역을 조회하고 필터링합니다.
    """
    serializer_class = AccountHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['amount_date', 'amount', 'type']
    ordering = ['-amount_date']  # 기본 정렬: 최신순

    def get_queryset(self):
        """사용자 소유 계좌의 거래 내역만 반환"""
        user = self.request.user

        # 삭제되지 않은 거래 내역만 조회
        queryset = AccountHistory.objects.filter(
            Q(user=user) | Q(account__user=user),  # 사용자가 직접 수행하거나 사용자 계좌의 거래
            deleted_at__isnull=True  # 삭제되지 않은 거래
        ).distinct()

        # 필터 파라미터 처리
        filter_serializer = AccountHistoryFilterSerializer(data=self.request.query_params)
        if filter_serializer.is_valid():
            filters = filter_serializer.validated_data

            # 계좌 ID 필터링
            account_id = filters.get('account_id')
            if account_id:
                # 해당 계좌가 사용자 소유인지 확인
                if Account.objects.filter(account_id=account_id, user=user).exists():
                    queryset = queryset.filter(account_id=account_id)
                else:
                    return AccountHistory.objects.none()

            # 거래 유형 필터링
            history_type = filters.get('type')
            if history_type:
                queryset = queryset.filter(type=history_type)

            # 금액 범위 필터링
            min_amount = filters.get('min_amount')
            if min_amount:
                queryset = queryset.filter(amount__gte=min_amount)

            max_amount = filters.get('max_amount')
            if max_amount:
                queryset = queryset.filter(amount__lte=max_amount)

            # 날짜 범위 필터링
            start_date = filters.get('start_date')
            if start_date:
                queryset = queryset.filter(amount_date__date__gte=start_date)

            end_date = filters.get('end_date')
            if end_date:
                queryset = queryset.filter(amount_date__date__lte=end_date)

        return queryset


class AccountHistoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    계좌 거래 내역 상세 API

    특정 거래 내역을 조회, 수정, 삭제하는 API입니다.
    - GET: 거래 내역 상세 정보 조회
    - PATCH: 거래 내역 설명 수정
    - DELETE: 거래 내역 삭제 (24시간 이내의 거래만 가능)
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'account_history_id'

    def get_queryset(self):
        """사용자 소유 계좌의 거래 내역 또는 사용자가 직접 수행한 거래만 반환"""
        user = self.request.user
        return AccountHistory.objects.filter(
            Q(user=user) | Q(account__user=user),
            deleted_at__isnull=True
        ).distinct()

    def get_serializer_class(self):
        """요청 메서드에 따라 시리얼라이저 선택"""
        if self.request.method in ['PUT', 'PATCH']:
            return AccountHistoryUpdateSerializer
        return AccountHistorySerializer

    def update(self, request, *args, **kwargs):
        """거래 내역 수정 처리 (설명만 수정 가능)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 전체 객체 데이터 반환
        response_serializer = AccountHistorySerializer(instance)
        return Response(response_serializer.data)

    @db_transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        거래 내역 삭제 처리

        - 최근 24시간 이내의 거래만 삭제 가능
        - 실제 삭제가 아닌 소프트 삭제 구현
        - 거래 취소 시 계좌 잔액도 원상복구
        """
        instance = self.get_object()

        # 최근 24시간 이내의 거래만 삭제 가능
        time_threshold = timezone.now() - timedelta(hours=24)
        if instance.amount_date < time_threshold:
            return Response(
                {"error": "생성 후 24시간이 지난 거래는 삭제할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 계좌 잔액 조정
        account = Account.objects.select_for_update().get(account_id=instance.account.account_id)

        # 거래 유형에 따라 잔액 원상복구
        if instance.type == 'DEPOSIT':
            # 입금 취소: 잔액 감소
            account.balance -= instance.amount
        elif instance.type == 'WITHDRAWAL' or instance.type == 'TRANSFER':
            # 출금/이체 취소: 잔액 증가
            account.balance += instance.amount

        account.save()

        # 소프트 삭제 실행
        instance.soft_delete()

        return Response(
            {
                "message": "거래가 성공적으로 취소되었습니다.",
                "new_balance": float(account.balance)
            },
            status=status.HTTP_200_OK
        )