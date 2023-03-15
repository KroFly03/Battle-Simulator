from flask import Blueprint, render_template, request, redirect, url_for

from module.arena import Arena
from module.classes import unit_classes
from module.equipment import Equipment
from module.unit import PlayerUnit, EnemyUnit

index = Blueprint('main_page', __name__, template_folder='templates')
prep = Blueprint('preparation', __name__, template_folder='templates')
fight = Blueprint('fight', __name__, template_folder='templates', url_prefix='/fight')

arena = Arena()

heroes = {
    'player': ...,
    'enemy': ...,
}


def init_preparation():
    """
    Fills out the form with the relevant data
    """
    equipment = Equipment()
    header = 'Выберите героя'
    weapons = equipment.get_weapon_names()
    armors = equipment.get_armor_names()
    result = {
        'header': header,
        'weapons': weapons,
        'armors': armors,
        'classes': unit_classes
    }

    return result


def create_player_hero(data):
    name = data['name']
    weapon_name = data['weapon']
    armor_name = data['armor']
    unit_class_name = data['unit_class']

    player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))
    player.equip_armor(Equipment().get_armor(armor_name))
    player.equip_weapon(Equipment().get_weapon(weapon_name))

    return player


def create_enemy_hero(data):
    name = data['name']
    weapon_name = data['weapon']
    armor_name = data['armor']
    unit_class_name = data['unit_class']

    enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))
    enemy.equip_armor(Equipment().get_armor(armor_name))
    enemy.equip_weapon(Equipment().get_weapon(weapon_name))

    return enemy


@index.route('/')
def menu_page():
    return render_template('index.html')


@prep.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    match request.method:
        case 'GET':
            result = init_preparation()

            return render_template('preparation.html', result=result)

        case 'POST':
            heroes['player'] = create_player_hero(request.form)

            return redirect(url_for('preparation.choose_enemy'))


@prep.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    match request.method:
        case 'GET':
            result = init_preparation()

            return render_template('preparation.html', result=result)
        case 'POST':
            heroes['enemy'] = create_enemy_hero(request.form)

            return redirect(url_for('fight.start_fight'))


@fight.route("/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)


@fight.route("/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@fight.route("/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@fight.route("/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@fight.route("/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)
