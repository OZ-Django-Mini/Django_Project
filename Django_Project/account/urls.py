from django.urls import path
from account import apis

urlpatterns = [
    #POST /account -> 신규 계좌 생성
    path('', apis.AccountCreateAPIView.as_view(), name='account_create'),

    #GET /account/me -> 내 계좌 조회
    path('me', apis.AccountMeAPIView.as_view(), name='account_me'),

    #POST /account/create -> 거래내역 생성
    path('create', apis.AccountTransactionAPIView.as_view(), name='account_create'),

]