import random
from django.shortcuts import render

from .models import Player, Game, PlayerGameInfo


def show_home(request):
    context = {'str1': '', 'str2': '', 'str3': '', 'form': False}
    if request.method == 'POST':
        game = Game.objects.get(pk=request.session['game_id'])
        game.counts += 1
        game.save()
        number = int(request.POST['number'])
        if number == game.number:
            game.status = 3
            game.save()
            
            context['str1'] = 'Вы угадали число!'
            context['str2'] = f'----------- Попытка {game.counts} -------------'
            context['str3'] = f'Это число {game.number}'
            context['form'] = True

            request.session.pop('game_id')
            return render(request, 'end_game.html', context)
        else:
            world = 'больше' if number < game.number else 'меньше'
            context['str1'] = 'Введите число:'
            context['str2'] = f'----------- Попытка {game.counts + 1} -------------'
            context['str3'] = f'Загаданное число {world} числа {number}'
            context['form'] = True

    else:
        if 'game_id' in request.session:
            player = Player.objects.get(pk=request.session['player_id'])
            if player.is_main:
                game = Game.objects.get(pk=request.session['game_id'])
                if game.status == 3:
                    player.is_main = False
                    player.save()

                    context['str1'] = f'Загаданное число: {game.number}'
                    context['str2'] = f'Ваше число угадали с {game.counts} попытки.'

                    request.session.pop('game_id')
                else:
                    context['str1'] = f'Загаданное число: {game.number}'
                    context['str2'] = 'Второй игрок будет пытаться отгадать его.'
            else:
                print('Что-то пошло не так!!!')
                request.session.pop('game_id')
        else:
            # Сюда попадают новенькие.
            game = Game.objects.filter(status=1).first()
            if game:
                # Пытаемся захватить игру.
                game.status = 2
                game.save()
                get_player(request.session, game, is_chief=False)

                context['str1'] = 'Введите число'
                context['str2'] = f'----------- Попытка {game.counts + 1} -------------'
                context['form'] = True
                
            else:
                # Содаём новую игру. Делаем этого игрока главным.
                game = Game.objects.create(number=random.randint(1,10), status=1)
                get_player(request.session, game, is_chief=True)
                
                context['str1'] = f'Загаданное число: {game.number}'
                context['str2'] = 'Второй игрок будет пытаться отгадать его.'

    return render(request, 'home.html', context)


def get_player(session, game, is_chief=False):
    if 'player_id' not in session:
        player = Player.objects.create(is_main=is_chief)
        session['player_id'] = player.id
    else:
        player = Player.objects.get(pk=session['player_id'])
        if is_chief:
            player.is_main = is_chief
            player.save()
    player.game.add(game)
    session['game_id'] = game.id

