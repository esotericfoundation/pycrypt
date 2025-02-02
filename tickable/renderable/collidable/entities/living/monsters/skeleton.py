import pygame

from tickable.renderable.collidable.entities.entity import Entity
from tickable.renderable.collidable.entities.living.monsters.ai.goals.back_off_from_target import BackOffFromTargetGoal
from tickable.renderable.collidable.entities.living.monsters.ai.goals.random_wander import RandomWanderGoal
from tickable.renderable.collidable.entities.living.monsters.ai.goals.walk_to_target import WalkToTargetGoal
from tickable.renderable.collidable.entities.projectiles.fireball import Fireball
from tickable.renderable.collidable.entities.living.living_entity import LivingEntity
from tickable.renderable.collidable.entities.living.monsters.monster import Monster


class Skeleton(Monster):
    wander_duration = 1.5
    wander_cooldown = 1.0
    randomness = 0.35

    def __init__(self, position: tuple[int, int], size: int, game: "Game"):
        super().__init__(position, "skeleton", size, 50, game)

    def register_goals(self):
        self.goals.append(RandomWanderGoal(
            self, 2, self.game, 0.35, Skeleton.wander_duration, Skeleton.wander_cooldown, Skeleton.randomness))
        self.goals.append(WalkToTargetGoal(
            self, 1, self.game, 0.6))
        self.goals.append(BackOffFromTargetGoal(
            self, 0, self.game, 0.7, 200))

    def attack_entity(self, entity: LivingEntity):
        Fireball(entity.get_center(), (self.position.x, self.position.y), 32, self.game, 1.2)

    def is_colliding(self, entity: Entity) -> bool:
        if isinstance(entity, Fireball):
            return False

        return super().is_colliding(entity)

    def damage(self, damage):
        super().damage(damage)

        if not self.is_alive():
            return

        sound = pygame.mixer.Sound('assets/sounds/skeleton_damage.mp3')
        sound.set_volume(0.125)
        pygame.mixer.Sound.play(sound)

    def die(self):
        super().die()

        sound = pygame.mixer.Sound('assets/sounds/skeleton_death.mp3')
        sound.set_volume(0.125)
        pygame.mixer.Sound.play(sound)
