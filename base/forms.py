from django.forms import ModelForm
from .models import Room, Team, Player

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['members']

class Player(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['team']