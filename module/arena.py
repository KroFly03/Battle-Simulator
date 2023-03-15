from typing import Optional

from module.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        Determines the status of the game
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self._battle_result = 'Ничья'

        if self.player.hp <= 0:
            self._battle_result = 'Противник победил'

        if self.enemy.hp <= 0:
            self._battle_result = 'Игрок победил'

        return self._end_game()

    def _check_health_limit(self):
        if self.player.hp > self.player.unit_class.max_health:
            self.player.hp = self.player.unit_class.max_health

        if self.enemy.hp > self.enemy.unit_class.max_health:
            self.enemy.hp = self.enemy.unit_class.max_health

    def _stamina_regeneration(self) -> None:
        units = (self.player, self.enemy)

        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> Optional[str]:
        """
        Ends the turn and allows the opponent to
        take some action, followed by a validation
        to check the health of all heroes
        """
        result = self._check_players_hp()
        if result is not None:
            return result

        if self.game_is_running:
            result = self.enemy.hit(self.player)

            self._check_health_limit()
            self._stamina_regeneration()

            if self.player.hp < 0:
                result = self._check_players_hp()

            return result

    def _end_game(self) -> str:
        self._instances = {}
        self.game_is_running = False

        return self._battle_result

    def player_hit(self) -> str:
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()

        return f'{result}<br>{turn_result}'

    def player_use_skill(self) -> str:
        result = self.player.use_skill(self.enemy)

        self._check_health_limit()
        turn_result = self.next_turn()

        return f'{result}<br>{turn_result}'
