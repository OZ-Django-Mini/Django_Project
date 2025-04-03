# account_history/urls.py
# 앱 내의 URL 라우팅을 정의하는 파일입니다.

from django.urls import path
from .views import (
    AccountHistoryListAPIView,
    AccountHistoryCreateAPIView,
    AccountHistoryDetailAPIView
)

urlpatterns = [
    # 거래 내역 목록 조회
    path('account-histories/', AccountHistoryListAPIView.as_view(), name='account-history-list'),

    # 새 거래 내역 생성
    path('account-histories/create/', AccountHistoryCreateAPIView.as_view(), name='account-history-create'),

    # 특정 거래 내역 조회/수정/삭제
    path('account-histories/<int:account_history_id>/', AccountHistoryDetailAPIView.as_view(),
         name='account-history-detail'),
]