from dataclasses import dataclass

from module.skills import StrongBeat, InsidiousBlow, Healing, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name='Воин',
    max_health=60.0,
    max_stamina=40.0,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
    skill=StrongBeat()
)

ThiefClass = UnitClass(
    name='Вор',
    max_health=50.0,
    max_stamina=35.0,
    attack=1.5,
    stamina=1.2,
    armor=1.0,
    skill=InsidiousBlow()
)

PriestClass = UnitClass(
    name='Жрец',
    max_health=40.0,
    max_stamina=60.0,
    attack=0.7,
    stamina=1.2,
    armor=1.0,
    skill=Healing()
)

unit_classes = {
    WarriorClass.name: WarriorClass,
    ThiefClass.name: ThiefClass,
    PriestClass.name: PriestClass
}
