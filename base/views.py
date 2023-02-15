from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


from .models import Room, Topic, Message, Player, Team, Match
from .forms import RoomForm, TeamForm
import random


def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesn`t exist')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            Player.objects.create(
                name = user.username
            )

            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form':form})

def match(team_pair):
    score_1 = score_2 = 0
    while score_1 < 2 and score_2 < 2:
        coin = random.randrange(0,2,1)
        if coin == 0:
            score_1 += 1
        else:
            score_2 += 1

    if score_2 < score_1:
        return [team_pair[0], score_1, score_2]
    else:
        return [team_pair[0], score_1, score_2]

def tournament(list):

    first_pair = list[0], list[1]
    second_pair = list[2], list[3]

    a = match(first_pair)
    first_match_score = f'{str(a[1])}-{str(a[2])}'
    b = match(second_pair)
    second_match_score = f'{str(b[1])}-{str(b[2])}'


    third_pair = a,b

    c = match(third_pair[0])
    third_match_score = f'{str(c[1])}-{str(c[2])}'

    winners = [a[0],b[0],c[0]]


    scores = [first_match_score, second_match_score, third_match_score]

    return [winners, scores]

def home(request):
    teams = Team.objects.all()
    teams_count = teams.count()


    winners = ['','','']
    scores = []
    team_list = ['','','','']
    
    
    if Team.objects.all().count() == 4:
        team_list = []
        for i in teams:
            team_list.append(i.name)
        random.shuffle(team_list)

        ready = True

        counter = Team.objects.annotate(num_players = Count('members'))
        for i in range(len(counter)):
            if counter[i].num_players != 2:
                ready = False
                break
        
        if ready:
            winners, scores = tournament(team_list)    
        


    all_team_players = Player.objects.all().exclude(team = None)

    context = {
            'teams':teams,
            'teams_count':teams_count,
            'all_team_players': all_team_players,
            'team_list':team_list, 
            'winners':winners, 
            'scores':scores}
    
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def createTeam(request):
    form = TeamForm()
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.save()
            team.members.add(request.user)
            team.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/team_form.html', context)

def team(request, pk):
    team_view = Team.objects.get(id=pk)
    team_members = team_view.members.all()

    if request.method == 'POST':
        if request.POST.get('leaveTeam'):
            Player.objects.filter(name=request.user.username).update(team = None)
            team_view.members.remove(request.user)
        else:
            Player.objects.filter(name=request.user.username).update(team = team_view)
            team_view.members.add(request.user)

        return redirect('team',pk)
    context = {"team_view":team_view, 'team_members':team_members}
    return render(request, 'base/team.html',context)
