from django.contrib import admin
from .models import User
from accounts.models import UserDetail
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'provider')

    def first_name(self, data):
        try: 
            user_detail = UserDetail.objects.get(user=data)
        except ObjectDoesNotExist:
            return ''

        return str(user_detail.first_name)

    def last_name(self, data):
        try: 
            user_detail = UserDetail.objects.get(user=data)
        except ObjectDoesNotExist:
            return ''

        return str(user_detail.last_name)