from django.contrib import admin
from .models import UserDetail
from django.core.exceptions import ObjectDoesNotExist
from tokens.models import Token
from .forms import UserDetailAdminForm

# Register your models here.
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'wallet_token', 'token_frozen')

    form = UserDetailAdminForm

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'wallet_token', 'wallet_token_paused'),
        }),
    )

    def wallet_token(self, data):
        try: 
            user_token = Token.objects.get(user=data.user)
        except ObjectDoesNotExist:
            return str(0)

        return str(user_token.balance)

    def token_frozen(self, data):
        try: 
            user_token = Token.objects.get(user=data.user)
        except ObjectDoesNotExist:
            return str(0)

        return str(user_token.paused_balance)
