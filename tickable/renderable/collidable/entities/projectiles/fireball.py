import random

from pygame import Vector2

from tickable.renderable.collidable.entities.entity import Entity
from tickable.renderable.collidable.entities.living.living_entity import LivingEntity


class Fireball(Entity):

    def __init__(self, target: tuple[int, int], position: tuple[int, int], size: int, game: "Game", speed = 1, character = "fireball"):
        super().__init__(position, character, size, game)
        self.target = Vector2(target)
        self.speed = speed
        self.strong = random.randint(0, 1) == 0

    def move(self):
        distance = self.target - self.position
        if distance.magnitude_squared() < 16:
            self.unload()
            return
        self.move_without_collision(distance, self.speed)
        self.game.current_room.other_entities.append(self)

    def is_colliding(self, entity: Entity) -> bool:
        if isinstance(entity, Entity) and entity.no_clip:
            return False

        from tickable.renderable.collidable.entities.living.monsters.skeleton import Skeleton
        if isinstance(entity, Skeleton) or isinstance(entity, Fireball):
            return False

        is_colliding = super().is_colliding(entity)

        if is_colliding:
            self.unload()
            if isinstance(entity, LivingEntity):
                entity.damage(10)
                return False
            return True

        return False
