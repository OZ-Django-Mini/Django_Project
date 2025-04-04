# account_history/urls.py
# 앱 내의 URL 라우팅을 정의하는 파일입니다.

from django.urls import path
from .views import (
    AccountHistoryListAPIView,
    AccountHistoryDetailAPIView
)

urlpatterns = [
    # 거래 내역 목록 조회
    path('', AccountHistoryListAPIView.as_view(), name='account-history-list'),

    # 특정 거래 내역 조회/수정/삭제
    path('<int:account_history_id>/', AccountHistoryDetailAPIView.as_view(),
         name='account-history-detail'),
]