from rest_framework import serializers
from .models import Bet, BetOption, BetUser
from datetime import datetime
from django.db import transaction
from rest_framework.exceptions import ParseError
from tokens.utils import decrease_balance, increase_balance, create_user_balance

class BetSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=400)
    token = serializers.DecimalField(max_digits=10, decimal_places=0)
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    selected_option = serializers.CharField(max_length=400)
    options = serializers.ListField(
        child = serializers.CharField(max_length=400)
    )

    def create(self, validated_data):
        token = validated_data['token']
        user = self.context['user']
        
        with transaction.atomic():
            try:
                bet = Bet.objects.create(
                    user = user,
                    title = validated_data['title'],
                    min_token_allowed = validated_data['token'],
                    token_credited = validated_data['token'],
                    token_paid_out = 0,
                    start_at = validated_data['start_at'],
                    end_at = validated_data['end_at'],
                    created_at = datetime.now(),
                    updated_at = datetime.now()
                )
            except:
                raise ParseError("Could not create bet")

            options = validated_data['options']
            bet_option = None
            for option in options:
                try:
                    bet_option = BetOption.objects.create(
                        bet = bet,
                        name = option,
                        created_at = datetime.now(),
                        updated_at = datetime.now()
                    )

                    if option == validated_data['selected_option']:
                        bet_option = bet_option
                except:
                    raise ParseError("Could not create bet option")

            try:
                bet_user = BetUser.objects.create(
                        user = user,
                        bet = bet,
                        bet_option = bet_option,
                        token_on_bet = validated_data['token'],
                        token_paid_out = 0,
                        created_at = datetime.now(),
                        updated_at = datetime.now()
                    )
            except:
                raise ParseError("Could not place user bet")

        decrease_balance(self.context['user'], validated_data['token'], bet, "New bet of " + validated_data['token'] + " placed")

        # perform order creation
        return bet

    def validate(self, data):
        options = data.get('options')
        selected = data.get('selected_option')
        selectedExist = False

        for option in options:
            if option == selected:
                selectedExist = True

        if selectedExist == False:
            raise serializers.ValidationError("Selected option must exist in available options.")

        user_token = create_user_balance(self.context['user'])
        if data.get('token') > user_token.balance:
            raise serializers.ValidationError("You do not have enough token to perform this action")

        return data


class UpdateBetChoiceSerializer(serializers.Serializer):   
    id = serializers.DecimalField(max_digits=10, decimal_places=0)
    choice_id = serializers.DecimalField(max_digits=10, decimal_places=0)

    def create(self, validated_data):
        user = self.context['user']
        bet = Bet.objects.get(id=validated_data['id'])

        try:
            selected_bet_option = BetOption.objects.get(bet=bet, id = validated_data['choice_id'])
            bet_user = BetUser.objects.get(user = user, bet = bet)
            bet_user.bet_option = selected_bet_option
            bet_user.save()
        except:
            raise ParseError("Could not update user selected bet")

        return bet

    def validate(self, data):
        try:
            bet = Bet.objects.get(id=data.get('id'))
        except:
            raise serializers.ValidationError("Could not find the selected Bet.")

        options = BetOption.objects.filter(bet=bet)
        selected = data.get('choice_id')
        selectedExist = False

        for option in options:
            if option.id == selected:
                selectedExist = True

        if selectedExist == False:
            raise serializers.ValidationError("Selected option must exist in available options.")

        return data


class PlaceUserBetSerializer(serializers.Serializer):   
    id = serializers.DecimalField(max_digits=10, decimal_places=0)
    choice_id = serializers.DecimalField(max_digits=10, decimal_places=0)
    token = serializers.DecimalField(max_digits=10, decimal_places=0)

    def create(self, validated_data):
        user = self.context['user']
        bet = Bet.objects.get(id=validated_data['id'])

        try:
            bet_users = BetUser.objects.filter(user = user, bet = bet)
        except:
            bet_users = None
            
        if len(bet_users) != 0:
            raise ParseError("You have already placed a bet.")

        bet_option = BetOption.objects.get(bet=bet, id = validated_data['choice_id'])
        try:
            bet_user = BetUser.objects.create(
                user = user,
                bet = bet,
                bet_option = bet_option,
                token_on_bet = validated_data['token'],
                token_paid_out = 0,
                created_at = datetime.now(),
                updated_at = datetime.now()
            )

            # increase token credit on bet
            bet.token_credited = bet.token_credited + float(validated_data['token'])
            bet.save()

            # decrease balance
            decrease_balance(self.context['user'], validated_data['token'], bet, "New bet of " + str(validated_data['token']) + " placed")
        except:
            raise ParseError("Could not place user bet")

        return bet

    def validate(self, data):
        try:
            bet = Bet.objects.get(id=data.get('id'))
        except:
            raise serializers.ValidationError("Could not find the selected Bet.")

        options = BetOption.objects.filter(bet=bet)
        choice_id = data.get('choice_id')
        selectedExist = False

        for option in options:
            if option.id == choice_id:
                selectedExist = True

        if selectedExist == False:
            raise serializers.ValidationError("Selected option must exist in available options.")

        user_token = create_user_balance(self.context['user'])
        if float(data.get('token')) > user_token.balance:
            raise serializers.ValidationError("You do not have enough token to perform this action")

        if float(data.get('token')) < bet.min_token_allowed:
            raise serializers.ValidationError("The minimum token allowed for this bet is " + str(bet.min_token_allowed))

        return data


class WithdrawUserPlacedBetSerializer(serializers.Serializer):   
    id = serializers.DecimalField(max_digits=10, decimal_places=0)

    def create(self, validated_data):
        user = self.context['user']
        bet_user = BetUser.objects.get(id=validated_data['id'])

        bet = Bet.objects.get(id=bet_user.bet.id)

        if bet.user.id == bet_user.user.id:
            raise ParseError("You can not withdraw from the user you created. Try to delete the entire bet instead")

        try:
            # increase token credit on bet
            bet.token_credited = bet.token_credited - bet_user.token_on_bet
            bet.save()

            # increase user balance
            increase_balance(self.context['user'], bet_user.token_on_bet, bet, "Refund of " + str(bet_user.token_on_bet) + " from withdrawn bet")

            bet_user.delete()
        except:
            raise ParseError("Could not delete this bet.")

        return bet

    def validate(self, data):
        try:
            bet_user = BetUser.objects.get(id=data.get('id'), user=self.context['user'])
        except:
            raise serializers.ValidationError("Could not find the placed Bet by Id.")

        return data