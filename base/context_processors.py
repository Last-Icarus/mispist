from .models import Player

def extras(request):
    if request.user.is_authenticated:
        player = Player.objects.get(name=request.user.username)
    else:
        player = None

    extras = {'player':player}
    return extras