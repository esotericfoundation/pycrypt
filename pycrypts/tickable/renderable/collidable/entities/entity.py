from math import sqrt
from typing import TYPE_CHECKING

from pygame import Vector2

from ..collidable import Collidable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class Entity(Collidable):
    def __init__(self, position: tuple[int, int] | Vector2, character: str, size: int, game: "PyCrypts", room: "Room"):
        super().__init__(game, room)

        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)

        self.game = game

        self.image = self.game.get_asset("./assets/images/entities/" + character)

        self.base_image = self.image

        self.absolute_size = size
        self.size = size

        self.no_clip = False

        self.set_scale(room.entity_scale)

        self.base_image = self.image

    def render(self):
        self.game.screen.blit(self.image, self.position)

    def tick(self):
        self.move()
        self.render()

    def move(self):
        self.move_without_collision(self.velocity)
        self.velocity *= 0.1

        if self.velocity.magnitude_squared() < 0.1:
            self.velocity = Vector2(0, 0)

        pass

    def move_without_collision(self, distance_travelled: Vector2, speed_factor: float = 1):
        magnitude_squared = distance_travelled.magnitude_squared()

        if magnitude_squared == 0:
            return

        collidables = self.room.get_collidables()

        distance_travelled = (distance_travelled / sqrt(magnitude_squared)) * 250 * self.game.current_room.movement_factor * speed_factor * self.game.dt

        filtered = list(filter(lambda c: c != self, collidables))

        self.position.x += distance_travelled.x
        collision_x = any(self.is_colliding(collidable) or collidable.is_colliding(self) for collidable in filtered)
        if collision_x:
            self.position.x -= distance_travelled.x

        self.position.y += distance_travelled.y
        collision_y = any(self.is_colliding(collidable) or collidable.is_colliding(self) for collidable in filtered)
        if collision_y:
            self.position.y -= distance_travelled.y

    def move_towards(self, entity: "Entity", speed_factor: float = 1):
        self.move_towards_location(entity.position, speed_factor)

    def move_towards_location(self, location: Vector2, speed_factor: float = 1):
        distance = location - self.position
        self.move_without_collision(distance, speed_factor)

    def move_away_from(self, entity: "Entity", speed_factor: float = 1):
        distance = entity.position - self.position
        distance *= -1
        self.move_without_collision(distance, speed_factor)

    def is_colliding(self, entity: Collidable) -> bool:
        if self.no_clip:
            return False

        if isinstance(entity, Entity):
            return self.position.distance_squared_to(entity.position) < ((self.size / 2 + entity.size / 2) ** 2)

        from ..walls.wall import Wall
        if isinstance(entity, Wall):
            return entity.is_colliding(self)
        return False

    def set_scale(self, scale: float):
        self.size = self.absolute_size * scale
        self.image = self.game.pygame.transform.scale(self.base_image, (self.size, self.size))

    def get_radius(self):
        return self.size / 2.0

    def get_center(self):
        return self.position

    def get_actual_center(self):
        return self.position + (self.size / 2, self.size / 2)

    def get_top_left(self):
        return self.position

    def get_bottom_right(self):
        return self.position + 2 * Vector2(self.get_radius(), self.get_radius())

    def get_top_right(self):
        return self.position + 2 * Vector2(self.get_radius(), 0)

    def get_bottom_left(self):
        return self.position + 2 * Vector2(0, self.get_radius())

    def get_points(self):
        return [self.get_top_left(), self.get_bottom_right(), self.get_top_right(), self.get_bottom_left()]

    def sees_other(self, other: "Entity") -> bool:
        walls = self.room.get_walls()
        center = self.get_actual_center()

        distance = other.get_actual_center() - center
        direction = distance.normalize() * 10

        current_position = center + direction
        while (current_position - center).magnitude_squared() < distance.magnitude_squared():
            for wall in walls:
                if wall.contains_point(current_position):
                    return False

            current_position += direction

        return True
