
def get_username(strategy, details, backend, user=None, *args, **kwargs):
    logged_in_user = strategy.storage.user.get_username(user)

    if not details.get('email'):
        error = "Sorry, but your social network needs to provide us your email"
        return error
    if logged_in_user:
        if logged_in_user.lower() != details.get('email').lower():
            error = "Sorry, but you are already logged in with another account"
            return error

    return {
        'username': details.get('email').lower(),
    }
