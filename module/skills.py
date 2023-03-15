from abc import ABC, abstractmethod


class Skill(ABC):
    def __init__(self):
        self.user = None
        self.target = None
        self.was_enough_skill_stamina = True

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def use(self, user, target) -> str:
        """
        Implements the application of the ability
        with subsequent validation
        """
        self.user = user
        self.target = target

        if self.user.stamina > self.stamina:
            self.was_enough_skill_stamina = True

            return self.skill_effect()

        self.was_enough_skill_stamina = False
        return f'{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости.'


class DamageSkill(ABC):
    @property
    @abstractmethod
    def damage(self):
        pass


class HealSkill(ABC):
    @property
    @abstractmethod
    def heal(self):
        pass


class DamageSkillEffect(DamageSkill, Skill, ABC):
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage

        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'


class HealSkillEffect(HealSkill, Skill, ABC):
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.user.hp += self.heal

        return f'{self.user.name} использует {self.name} и восстанавливает {self.heal} здоровья.'


class StrongBeat(DamageSkillEffect):
    name = 'Сильный удар'
    stamina = 15
    damage = 20


class InsidiousBlow(DamageSkillEffect):
    name = 'Коварный удар'
    stamina = 10
    damage = 15


class Healing(HealSkillEffect):
    name = 'Исцеление'
    stamina = 5
    heal = 15
