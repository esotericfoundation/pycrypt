import pygame
from pygame import Vector2

from enums.movement_keys import movement_keys
from tickable.renderable.collidable.collidable import Collidable
from tickable.renderable.collidable.entities.projectiles.arrow import Arrow
from tickable.renderable.collidable.entities.living.living_entity import LivingEntity, get_living_entities
from tickable.renderable.collidable.entities.projectiles.sword import Sword


def get_players():
    return list(filter(lambda entity: isinstance(entity, Player), get_living_entities()))

class Player(LivingEntity):
    attack_cooldown = 0.75
    attack_range = 175
    regeneration_rate = 0.5

    def __init__(self, position: tuple[int, int], character: str, size: int, movement_type: int, attack_key: int, game: "Game"):
        super().__init__(position, "players/" + character, size, 100, game)

        self.movement_type = movement_type
        self.attack_key = attack_key

        self.time_since_last_attack = Player.attack_cooldown + 1
        self.time_since_last_regeneration = 0

    def tick(self):
        super().tick()

        self.time_since_last_attack += self.game.dt
        self.time_since_last_regeneration += self.game.dt

        keys = pygame.key.get_pressed()
        if keys[self.attack_key]:
            self.attack()

        if self.time_since_last_regeneration >= Player.regeneration_rate:
            if self.health < self.max_health:
                self.health = min(self.health + 1, self.max_health)
                self.time_since_last_regeneration = 0

        if keys[pygame.K_LALT]:
            self.no_clip = not self.no_clip

    def move(self):
        super().move()

        keys = pygame.key.get_pressed()

        distance_travelled = pygame.Vector2()

        if keys[pygame.K_w if self.movement_type == movement_keys["WASD"] else pygame.K_UP]:
            distance_travelled.y -= 1
        if keys[pygame.K_s if self.movement_type == movement_keys["WASD"] else pygame.K_DOWN]:
            distance_travelled.y += 1
        if keys[pygame.K_a if self.movement_type == movement_keys["WASD"] else pygame.K_LEFT]:
            distance_travelled.x -= 1
        if keys[pygame.K_d if self.movement_type == movement_keys["WASD"] else pygame.K_RIGHT]:
            distance_travelled.x += 1

        if distance_travelled.magnitude() == 0:
            return

        self.velocity += distance_travelled.normalize() * 250 * self.game.dt

        if self.velocity.magnitude() == 0:
            return

        self.velocity = self.velocity.normalize() * min(self.velocity.magnitude(), 25)

    def attack(self):
        if self.time_since_last_attack < Player.attack_cooldown:
            return

        attackable_entities = list(filter(lambda e: not isinstance(e, Player) and self.sees_other(e) and e.sees_other(self), get_living_entities()))

        if len(attackable_entities) == 0:
            return

        closest_entity = None
        for entity in attackable_entities:
            if closest_entity is None:
                closest_entity = entity
                continue

            if Vector2(closest_entity.position).distance_squared_to(self.position) > entity.position.distance_squared_to(self.position):
                closest_entity = entity

        self.attack_entity(closest_entity)

    def sword_attack(self, entity: LivingEntity):
        Sword(entity, self, self.get_center(), self.game)
        pass

    def bow_attack(self, entity: LivingEntity):
        Arrow(entity.get_center(), self.get_center(), 32, self.game)
        pass

    def attack_entity(self, entity: LivingEntity):
        if entity.position.distance_squared_to(self.position) < (Player.attack_range * Player.attack_range) * self.game.current_room.entity_scale * self.game.current_room.entity_scale:
            self.sword_attack(entity)
        else:
            self.bow_attack(entity)

        self.time_since_last_attack = 0

    def damage(self, damage: int):
        super().damage(damage)

        sound = pygame.mixer.Sound('assets/sounds/damage.mp3')
        sound.set_volume(0.125)
        pygame.mixer.Sound.play(sound)

    def die(self):
        super().die()

        if len(get_players()) == 0:
            self.game.end()

    def is_colliding(self, entity: Collidable) -> bool:
        if isinstance(entity, Arrow):
            return False

        if isinstance(entity, Sword):
            return False

        return super().is_colliding(entity)
