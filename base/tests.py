from django.test import TestCase
from .models import Player, Team
from .views import *
from django.contrib.auth.models import User


class caseTest(TestCase):

    # Проверка запросов на создание команд и успешного выполнения метода tournament(), требующего ровно 4 команды на входе
    def test_team_quantity(self):

        teams = ['Team_1', 'Team_2','Team_3', 'Team_4']

        team_list = []
        for name in teams:
            team_list.append(Team.objects.create(name = name))

        self.assertEqual(len(teams), len(team_list))
        tournament(team_list)

        
    # Проверка
    def test_player_quantity(self):

        teams = ['Team_1','Team_2','Team_3','Team_4']

        player1 = User.objects.create(username = 'Testuser')
        player2 = User.objects.create(username = 'Testuser2')


        team_list = []
        for name in teams:
            team = Team.objects.create(name = name)

            # Добавление игрков в команды
            # На практике, интерфейс не позволит игроку зарегестрироваться в нескольких командах, но для теста заполненности
            # команд можно сделать и так
            team.members.add(player1)
            team.members.add(player2)

            team_list.append(team)

        winners,scores = tournament(team_list)

        ready = True

        counter = Team.objects.annotate(num_players = Count('members'))
        for i in range(len(counter)):
            if counter[i].num_players != 2:
                print(counter[i].num_players)
                ready = False
                break

        if not ready:
            print('Мало игроков')
            raise IndexError
    
    # Тестирование создания пользователя с разным набором символов в нике
    def test_input(self):
        player_names = [123, 'abc','abc123','abc_!!@#$%^&*']
        for name in player_names:
            Player.objects.create(name = name)

        self.assertEqual(Player.objects.all().count(),len(player_names))

        
