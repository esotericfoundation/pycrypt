from typing import TYPE_CHECKING

import pygame
from pygame import Vector2, Rect

from ..collidable import Collidable
from ..entities.entity import Entity
from ....tickable import Tickable

if TYPE_CHECKING:
    from .....game import PyCrypts
    from .....rooms.room import Room


class Wall(Collidable):
    points: list[  # list of
        tuple[  # pair of
            tuple[int, int],  # top left 
            tuple[int, int]  # bottom right
        ]
    ] = []

    def __init__(self, top_left: tuple[int, int], bottom_right: tuple[int, int], game: "PyCrypts", room: "Room"):
        super().__init__(game, room)
        self.top_left = Vector2(top_left)
        self.bottom_right = Vector2(bottom_right)
        self.game = game

    def get_center(self):
        return (self.top_left + self.bottom_right) / 2.0

    def get_width(self):
        return self.bottom_right.x - self.top_left.x

    def get_height(self):
        return self.bottom_right.y - self.top_left.y

    def tick(self):
        self.render()

    def render(self):
        width = self.bottom_right.x - self.top_left.x
        height = self.bottom_right.y - self.top_left.y

        pygame.draw.rect(self.game.screen, (65, 65, 65), Rect(self.top_left, (width, height)))
        pass

    def is_colliding(self, other: Collidable) -> bool:
        if isinstance(other, Entity):
            if other.no_clip:
                return False

            points = other.get_points()

            for point in points:
                if self.contains_point(point):
                    return True
        return False

    def contains_point(self, point: Vector2) -> bool:
        return self.top_left.x <= point.x <= self.bottom_right.x and self.top_left.y <= point.y <= self.bottom_right.y

    def to_string(self):
        return f'wall = Wall({self.top_left}, {self.bottom_right})'
