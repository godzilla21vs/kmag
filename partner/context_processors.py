# mag/context_processors.py

def user_info(request):
    user_info = {}
    if request.user.is_authenticated:
        user_info['user'] = request.user
        user_info['author_name'] = request.user.username  # Utilisez le nom d'utilisateur comme nom d'auteur
    return user_info
