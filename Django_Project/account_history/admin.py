# account_history/admin.py
# Django 관리자 페이지에 모델을 등록하고 커스터마이징하는 파일입니다.

from django.contrib import admin
from .models import AccountHistory


@admin.register(AccountHistory)
class AccountHistoryAdmin(admin.ModelAdmin):
    """거래 내역 관리자 설정"""

    # 목록 페이지에 표시할 필드들
    list_display = (
        'account_history_id', 'account', 'get_account_number', 'user', 'get_username',
        'amount', 'type', 'amount_date', 'is_deleted'
    )

    # 검색 필드
    search_fields = (
        'account__account_number', 'user__name', 'user__email',
        'description', 'amount'
    )

    # 필터 옵션
    list_filter = ('type', 'amount_date', 'deleted_at')

    # 상세 페이지에서 필드 그룹화
    fieldsets = (
        ('기본 정보', {
            'fields': ('account', 'user', 'amount', 'type', 'description')
        }),
        ('시간 정보', {
            'fields': ('amount_date', 'deleted_at')
        }),
    )

    # 읽기 전용 필드
    readonly_fields = ('account_history_id', 'account', 'user', 'amount', 'type', 'amount_date')

    # 날짜 계층 구조 필터
    date_hierarchy = 'amount_date'

    # 정렬 기본값
    ordering = ('-amount_date',)

    # 페이지당 항목 수
    list_per_page = 20

    def get_account_number(self, obj):
        """계좌번호 표시"""
        return obj.account.account_number

    get_account_number.short_description = '계좌번호'
    get_account_number.admin_order_field = 'account__account_number'

    def get_username(self, obj):
        """사용자 이름 표시"""
        return obj.user.name

    get_username.short_description = '사용자명'
    get_username.admin_order_field = 'user__name'

    def has_add_permission(self, request):
        """추가 권한 비활성화"""
        return False

    def has_change_permission(self, request, obj=None):
        """변경 권한 비활성화"""
        return False

    def has_delete_permission(self, request, obj=None):
        """삭제 권한 (관리자만 가능)"""
        return request.user.is_superuser