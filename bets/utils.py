from .models import BetOption, BetUser
from accounts.models import UserDetail

def format_bet(bet, user = None):
    options = BetOption.objects.filter(bet=bet)
    details = UserDetail.objects.get(user=bet.user)
    bet_options = []
    for option in options:
        bet_options.append({'id': option.id, 'name': option.name})

    user_wedger = None
    if user != None:
        try:
            bet_user = BetUser.objects.get(user=user, bet=bet)
            
            user_wedger = {
                'token_wedger': bet_user.token_on_bet,
                'choice': bet_user.bet_option.name
            }
        except:
            bet_user = None

    content = {
        'id': bet.id,
        'title': bet.title,
        'min_token': bet.min_token_allowed,
        'start_at': bet.start_at,
        'end_at': bet.end_at,
        'author': {
            'first_name': details.first_name if details != '' else '',
            'last_name': details.last_name if details != '' else '',
        },
        'options': bet_options,
        'user_wedger': user_wedger
    }
    return content