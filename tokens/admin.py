from django.contrib import admin
from .models import TokenHistory, Token
from accounts.models import UserDetail
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.
@admin.register(TokenHistory)
class TokenHistoryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'balance_before', 'balance_after', 'updated_at')

    def first_name(self, data):
        try: 
            user_token = Token.objects.get(id=data.token.id)
            user_detail = UserDetail.objects.get(user=user_token.user)
        except ObjectDoesNotExist:
            return ''

        return str(user_detail.first_name)

    def last_name(self, data):
        try: 
            user_token = Token.objects.get(id=data.token.id)
            user_detail = UserDetail.objects.get(user=user_token.user)
        except ObjectDoesNotExist:
            return ''

        return str(user_detail.last_name)

    def email(self, data):
        try: 
            user_token = Token.objects.get(id=data.token.id)
        except ObjectDoesNotExist:
            return ''

        return str(user_token.user.email)