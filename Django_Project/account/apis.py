
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from account.models import Account
from account.serializers import AccountCreateSerializer, AccountReadSerializer

#계좌 생성
class AccountCreateAPIView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer

#계좌 조회
class AccountMeAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 조회 가능

    def get(self, request):
        accounts = Account.objects.filter(user_id=request.user.id)
        serializer = AccountReadSerializer(accounts, many=True)

        return Response(serializer.data)


#거래 생성
