def user_info(request):
    user_info = {}
    if request.user.is_authenticated:
        user_info['user'] = request.user
    return user_info