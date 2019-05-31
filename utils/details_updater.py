
def user_details(strategy, details, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if not user:
        return
    if details.get('fullname'):
        details['name'] = details.get('fullname')
    changed = False  # flag to track changes
    protected = ('username', 'id', 'pk', 'email') + \
        tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

    for name, value in details.items():
        if value is None or not hasattr(user, name) or name in protected:
            continue

        current_value = getattr(user, name, None)
        if current_value == value:
            continue
        changed = True
        setattr(user, name, value)

    if changed:
        strategy.storage.user.changed(user)
