import time

import pygame
from pygame import Vector2, Surface

from enums.movement_keys import movement_keys
from rooms.entrance_zone import EntranceZone
from rooms.surface_zone import SurfaceZone
from tickable.renderable.collidable.entities.living.players.player import Player, get_players
from tickable.renderable.collidable.walls.wall import Wall
from tickable.renderable.display.health_bar import HealthBar
from tickable.tickable import Tickable


def load_icon(window_name: str, icon_name: str):
    pygame.display.set_caption(window_name)

    icon = pygame.image.load(f'assets/{icon_name}.png')
    pygame.display.set_icon(icon)


class Game:
    def __init__(self):
        self.screen: Surface = pygame.display.set_mode((1280, 720))
        load_icon("Dungeon Crawler", "big-skeleton-face")

        self.debug = True

        self.clicked_positions: [Vector2, Vector2] = [None, None]

        self.past = time.time()
        self.dt = 0

        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.bottom_left = Vector2(0, self.height)
        self.bottom_right = Vector2(self.width, self.height)
        self.top_left = Vector2(0, 0)
        self.top_right = Vector2(self.width, 0)
        self.center = Vector2(self.width / 2, self.height / 2)

        self.current_room = None
        self.entrance_zone = None
        self.surface_zone = None

        self.over = False

    def init(self):
        rizzler = Player((0, 0), "rizzler", 64, movement_keys["WASD"], pygame.K_LSHIFT, self)
        player = Player((0, 0), "pro", 64, movement_keys["ARROW"], pygame.K_RSHIFT, self)

        HealthBar(rizzler, (self.screen.get_width() - 100 - 300, self.screen.get_height() - 140), 300, 40, self)
        HealthBar(player, (100, self.screen.get_height() - 140), 300, 40, self)

        self.current_room = self.surface_zone = SurfaceZone(self)
        self.entrance_zone = EntranceZone(self)

        self.surface_zone.load()

        players = get_players()
        i = 0

        for player in players:
            i += 1
            if i == 1:
                player.position = self.current_room.spawn_1
            else:
                player.position = self.current_room.spawn_2
            player.set_scale(self.current_room.entity_scale)

    def tick(self):
        if not self.over:
            present = time.time()
            self.dt = present - self.past
            self.past = present

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.screen.fill((0, 0, 0))

        if self.over:
            font_1 = pygame.font.Font(None, 150)

            text_1 = font_1.render("Game Over!", True, (255, 0, 0))
            text_1_rect = text_1.get_rect(center=self.center)

            self.screen.blit(text_1, text_1_rect)

            font_2 = pygame.font.Font(None, 50)

            text_2 = font_2.render("Press ESC to exit", True, (200, 0, 0))
            text_2_rect = text_2.get_rect(center=(self.center.x, self.center.y + 100))

            self.screen.blit(text_2, text_2_rect)

        if not self.over:
            for tickable in Tickable.tickables:
                tickable.tick()

        pygame.display.flip()
        return True

    def handle_debug_mouse_click(self):
        pos = pygame.mouse.get_pos()
        print(f'POSITION SELECTED: ({pos[0]}, {pos[1]})')

        print(f'skeleton = Skeleton(({pos[0]}, {pos[1]}), 32)')

        debug_pos_1 = self.clicked_positions[0]
        debug_pos_2 = self.clicked_positions[1]

        if debug_pos_1 is None:
            self.clicked_positions[0] = Vector2(pos)
            return

        if debug_pos_2 is None:
            self.clicked_positions[1] = pos
            debug_pos_2 = pos

        print(debug_pos_1)
        print(debug_pos_2)

        wall = Wall(debug_pos_1, debug_pos_2, self)
        print(wall.to_string())

        self.clicked_positions = [None, None]

    def end(self):
        self.over = True
        self.current_room.unload()

        for tickable in Tickable.tickables:
            tickable.unload()

if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.init()

    while game.tick():
        pass

    pygame.quit()
