from django import forms
from django.forms import ModelForm, RadioSelect
from tokens.models import Token
from .models import UserDetail
from tokens.utils import increase_balance, decrease_balance, create_user_balance, pause_balance, reverse_pause_balance


class UserDetailAdminForm(ModelForm):
    wallet_token = forms.FloatField(label="Token Balance")
    wallet_token_paused = forms.FloatField(label="Token Balance Frozen")

    class Meta:
        model = UserDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = {}

        if instance:
            user = instance.user
            token_balance = 0
            token_balance_frozen = 0
            try: 
                user_token = Token.objects.get(user=user)
                token_balance = user_token.balance
                token_balance_frozen = user_token.paused_balance
            except:
                user_token = create_user_balance(user)
                token_balance = user_token.balance
                token_balance_frozen = user_token.paused_balance

            initial = {
                "wallet_token": token_balance,
                "wallet_token_paused": token_balance_frozen,
            }

        super().__init__(*args, **kwargs, initial=initial)

    def save(self, commit=True):
        wallet_token = self.cleaned_data.get('wallet_token', None)
        wallet_token_paused = self.cleaned_data.get('wallet_token_paused', None)
        user_token = Token.objects.get(user=self.instance.user)

        # update user wallet balance 
        if wallet_token != user_token.balance:
            amount_diff = wallet_token - user_token.balance

            if amount_diff > 0:
                increase_balance(self.instance.user, amount_diff)
            else:
                decrease_balance(self.instance.user, abs(amount_diff))

        # update user wallet frozen
        if wallet_token_paused != user_token.paused_balance:
            paused_amount_diff = wallet_token_paused - user_token.paused_balance

            if paused_amount_diff > 0:
                pause_balance(self.instance.user, paused_amount_diff)
            else:
                reverse_pause_balance(self.instance.user, abs(paused_amount_diff))

        return super().save(commit)