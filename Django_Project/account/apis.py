from rest_framework.exceptions import APIException ,PermissionDenied
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from account.models import Account
from account_history.models import AccountHistory
from account.serializers import (
    AccountCreateSerializer,
    AccountReadSerializer,
    AccountTransactionSerializer)
from django.utils import timezone
from django.shortcuts import get_object_or_404


#계좌 생성
class AccountCreateAPIView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

#계좌 조회
class AccountMeAPIView(APIView):

    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 조회 가능

    def get(self, request):
        try:
            accounts = Account.objects.filter(user_id=request.user.id, deleted_at__isnull=True)
            serializer = AccountReadSerializer(accounts, many=True)

            return Response(serializer.data)
        except Exception as e:
            raise APIException(f"서버 오류 발생: {str(e)}")

    def delete(self, request):
        try:
            # 요청 데이터에서 account_number를 가져옴
            account_number = request.data.get("account_number")
            if not account_number:
                raise APIException("account_number가 필요합니다.")

            # 해당 계좌 찾기
            account = Account.objects.get(account_number=account_number)

            # 사용자 본인 계좌인지 확인
            if account.user_id != request.user:
                raise PermissionDenied("본인의 계좌만 삭제할 수 있습니다.")

            # soft delete
            account.deleted_at = timezone.now()
            account.save()

            return Response({"message": "계좌가 삭제되었습니다."}, status=200)

        except Account.DoesNotExist:
            raise APIException("해당 계좌를 찾을 수 없습니다.")
        except Exception as e:
            raise APIException(f"서버 오류 발생: {str(e)}")




#거래 생성
class AccountTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def patch(self, request):
        try:
            account_number = request.data.get("account_number")
            account = get_object_or_404(Account, account_number=account_number)

            serializer = AccountTransactionSerializer(account, data=request.data)
            if serializer.is_valid():
                updated_account = serializer.save()
                return Response(
                    {
                        "account_number": str(updated_account.account_number),
                        "balance": updated_account.balance,
                    },
                    status=201
                )
            return Response(serializer.errors, status=400)

        except Exception as e:
            raise APIException(f"서버 오류 발생: {str(e)}")

class AccountDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, account_number):
        try:
            account = get_object_or_404(Account, account_number=account_number)
            if account.user_id != request.user.id:
                raise PermissionDenied("본인의 계좌만 삭제할 수 있습니다.")

            account.deleted_at = timezone.now()
            account.save()

            return Response({"message": "계좌가 삭제되었습니다."}, status=200)

        except Exception as e:
            raise APIException(f"서버 오류 발생: {str(e)}")