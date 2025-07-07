#!/usr/bin/env python3
"""
Planetoids - A recreation of the classic ZX81 space shooter
Inspired by the 1981 Macronics game for Sinclair ZX81
"""

import pygame
import math
import random
import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (ZX81 inspired - black and white with some accent colors)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    PAUSED = 4

class DamageType(Enum):
    ASTEROID = 1
    ALIEN_SHIP = 2
    ALIEN_BULLET = 3
    HYPERSPACE = 4

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

class GameObject:
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.rotation = 0
        self.radius = 10
        self.active = True
    
    def update(self, dt: float):
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Wrap around screen edges
        self.position.x = self.position.x % SCREEN_WIDTH
        self.position.y = self.position.y % SCREEN_HEIGHT
    
    def draw(self, screen):
        pass
    
    def collides_with(self, other) -> bool:
        if not (self.active and other.active):
            return False
        
        distance = math.sqrt((self.position.x - other.position.x)**2 + 
                           (self.position.y - other.position.y)**2)
        return distance < (self.radius + other.radius)

class Ship(GameObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.radius = 8
        self.thrust_power = 200
        self.rotation_speed = 300
        self.max_speed = 300
        self.fuel = 1000  # Strategic fuel management element
        self.max_fuel = 1000
        self.invulnerable_time = 0
        self.hyperspace_cooldown = 0
        self.hit_flash_time = 0  # Timer for flash effect when hit
        self.flash_intensity = 0.0  # Intensity of the flash (0.0 to 1.0)
        self.damage_type = None  # Type of damage for different flash colors
        
        # Health system
        self.max_health = 3
        self.health = self.max_health
        
        # Ship shape (triangle pointing up)
        self.shape = [
            Vector2(0, -10),
            Vector2(-6, 8),
            Vector2(6, 8)
        ]
    
    def update(self, dt: float):
        super().update(dt)
        
        # Update timers
        if self.invulnerable_time > 0:
            self.invulnerable_time -= dt
        if self.hyperspace_cooldown > 0:
            self.hyperspace_cooldown -= dt
        if self.hit_flash_time > 0:
            self.hit_flash_time -= dt
            # Calculate fading flash intensity
            self.flash_intensity = max(0.0, self.hit_flash_time / 1.0)  # Fade over 1 second
        else:
            self.flash_intensity = 0.0
            self.damage_type = None
        
        # Apply drag
        drag = 0.98
        self.velocity = self.velocity * drag
    
    def thrust(self, dt: float):
        if self.fuel <= 0:
            return
            
        # Calculate thrust direction
        thrust_x = math.sin(math.radians(self.rotation)) * self.thrust_power * dt
        thrust_y = -math.cos(math.radians(self.rotation)) * self.thrust_power * dt
        
        self.velocity.x += thrust_x
        self.velocity.y += thrust_y
        
        # Limit max speed
        if self.velocity.magnitude() > self.max_speed:
            normalized = self.velocity.normalize()
            self.velocity = normalized * self.max_speed
        
        # Consume fuel
        self.fuel -= 50 * dt
        if self.fuel < 0:
            self.fuel = 0
    
    def rotate(self, direction: int, dt: float):
        self.rotation += direction * self.rotation_speed * dt
        self.rotation = self.rotation % 360
    
    def hyperspace(self):
        if self.hyperspace_cooldown <= 0:
            # Random teleport with risk
            self.position.x = random.randint(50, SCREEN_WIDTH - 50)
            self.position.y = random.randint(50, SCREEN_HEIGHT - 50)
            self.velocity = Vector2(0, 0)
            self.hyperspace_cooldown = 3.0  # 3 second cooldown
            
            # Small chance of destruction (10%)
            if random.random() < 0.1:
                destroyed = self.take_hit(DamageType.HYPERSPACE, damage=self.health)  # Instant death
                if destroyed:
                    self.active = False
                return False
        return True
    
    def take_hit(self, damage_type: DamageType = DamageType.ASTEROID, damage: int = 1):
        """Called when the ship is hit - triggers flash effect and reduces health"""
        if self.invulnerable_time > 0:
            return False  # No damage during invulnerability
            
        self.health -= damage
        self.hit_flash_time = 1.0  # Flash for 1 second
        self.flash_intensity = 1.0  # Start at full intensity
        self.damage_type = damage_type
        self.invulnerable_time = 2.0  # 2 seconds of invulnerability after hit
        
        # Play hit sound effect
        self.play_hit_sound(damage_type)
        
        # Return True if ship is destroyed
        return self.health <= 0
    
    def play_hit_sound(self, damage_type: DamageType):
        """Play appropriate sound effect for damage type"""
        try:
            # Generate different tones for different damage types
            if damage_type == DamageType.ASTEROID:
                # Low thud sound
                self.generate_sound(200, 0.2)
            elif damage_type == DamageType.ALIEN_SHIP:
                # Sharp crash sound
                self.generate_sound(800, 0.3)
            elif damage_type == DamageType.ALIEN_BULLET:
                # High pitched zap
                self.generate_sound(1200, 0.15)
            elif damage_type == DamageType.HYPERSPACE:
                # Warbling sound
                self.generate_sound(400, 0.4)
        except:
            pass  # Ignore sound errors
    
    def generate_sound(self, frequency: int, duration: float):
        """Generate a simple tone for sound effects"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time_point = float(i) / sample_rate
                wave = 4096 * math.sin(frequency * 2 * math.pi * time_point)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            sound.set_volume(0.1)  # Keep volume low
            sound.play()
        except:
            pass  # Ignore sound generation errors
    
    def get_flash_color(self) -> tuple:
        """Get the appropriate flash color based on damage type and intensity"""
        if self.flash_intensity <= 0:
            return WHITE
        
        # Base colors for different damage types
        damage_colors = {
            DamageType.ASTEROID: (255, 100, 100),    # Red-orange
            DamageType.ALIEN_SHIP: (255, 50, 50),    # Bright red
            DamageType.ALIEN_BULLET: (255, 255, 100), # Yellow-red
            DamageType.HYPERSPACE: (150, 100, 255)   # Purple
        }
        
        base_color = damage_colors.get(self.damage_type, (255, 100, 100))
        
        # Interpolate between base color and white based on intensity
        flash_r = int(WHITE[0] + (base_color[0] - WHITE[0]) * self.flash_intensity)
        flash_g = int(WHITE[1] + (base_color[1] - WHITE[1]) * self.flash_intensity)
        flash_b = int(WHITE[2] + (base_color[2] - WHITE[2]) * self.flash_intensity)
        
        return (flash_r, flash_g, flash_b)
    
    def draw(self, screen):
        if not self.active:
            return
            
        # Don't draw if invulnerable and blinking
        if self.invulnerable_time > 0 and int(self.invulnerable_time * 10) % 2:
            return
        
        # Get appropriate ship color based on damage flash
        ship_color = self.get_flash_color()
        
        # Transform ship shape based on rotation
        transformed_points = []
        for point in self.shape:
            # Rotate point
            cos_r = math.cos(math.radians(self.rotation))
            sin_r = math.sin(math.radians(self.rotation))
            
            rotated_x = point.x * cos_r - point.y * sin_r
            rotated_y = point.x * sin_r + point.y * cos_r
            
            # Translate to ship position
            final_x = rotated_x + self.position.x
            final_y = rotated_y + self.position.y
            
            transformed_points.append((final_x, final_y))
        
        pygame.draw.polygon(screen, ship_color, transformed_points)

class Bullet(GameObject):
    def __init__(self, x: float, y: float, rotation: float):
        super().__init__(x, y)
        self.radius = 2
        self.lifetime = 2.0  # Bullets last 2 seconds
        
        # Set velocity based on rotation
        speed = 400
        self.velocity.x = math.sin(math.radians(rotation)) * speed
        self.velocity.y = -math.cos(math.radians(rotation)) * speed
    
    def update(self, dt: float):
        super().update(dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, WHITE, 
                             (int(self.position.x), int(self.position.y)), 
                             self.radius)

class Asteroid(GameObject):
    def __init__(self, x: float, y: float, size: int = 3):
        super().__init__(x, y)
        self.size = size  # 1=small, 2=medium, 3=large
        self.radius = 10 + (size * 8)
        self.rotation_speed = random.uniform(-180, 180)
        
        # Random velocity
        speed = random.uniform(20, 80)
        angle = random.uniform(0, 360)
        self.velocity.x = math.sin(math.radians(angle)) * speed
        self.velocity.y = -math.cos(math.radians(angle)) * speed
        
        # Generate random asteroid shape
        self.shape = []
        num_points = 8
        for i in range(num_points):
            angle = (360 / num_points) * i
            radius_variation = random.uniform(0.7, 1.3)
            radius = self.radius * radius_variation
            
            x = math.sin(math.radians(angle)) * radius
            y = -math.cos(math.radians(angle)) * radius
            self.shape.append(Vector2(x, y))
    
    def update(self, dt: float):
        super().update(dt)
        self.rotation += self.rotation_speed * dt
    
    def split(self) -> List['Asteroid']:
        if self.size <= 1:
            return []
        
        # Create 2-3 smaller asteroids
        new_asteroids = []
        num_splits = random.randint(2, 3)
        
        for _ in range(num_splits):
            new_asteroid = Asteroid(self.position.x, self.position.y, self.size - 1)
            # Give them different velocities
            speed = random.uniform(40, 120)
            angle = random.uniform(0, 360)
            new_asteroid.velocity.x = math.sin(math.radians(angle)) * speed
            new_asteroid.velocity.y = -math.cos(math.radians(angle)) * speed
            new_asteroids.append(new_asteroid)
        
        return new_asteroids
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Transform asteroid shape
        transformed_points = []
        for point in self.shape:
            # Rotate point
            cos_r = math.cos(math.radians(self.rotation))
            sin_r = math.sin(math.radians(self.rotation))
            
            rotated_x = point.x * cos_r - point.y * sin_r
            rotated_y = point.x * sin_r + point.y * cos_r
            
            # Translate to asteroid position
            final_x = rotated_x + self.position.x
            final_y = rotated_y + self.position.y
            
            transformed_points.append((final_x, final_y))
        
        pygame.draw.polygon(screen, WHITE, transformed_points, 2)

class AlienShip(GameObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.radius = 12
        self.shoot_timer = 0
        self.shoot_interval = random.uniform(1.5, 3.0)
        self.direction_timer = 0
        self.direction_interval = random.uniform(2.0, 4.0)
        
        # Set initial random velocity
        speed = random.uniform(50, 100)
        angle = random.uniform(0, 360)
        self.velocity.x = math.sin(math.radians(angle)) * speed
        self.velocity.y = -math.cos(math.radians(angle)) * speed
    
    def update(self, dt: float):
        super().update(dt)
        
        self.shoot_timer += dt
        self.direction_timer += dt
        
        # Change direction periodically
        if self.direction_timer >= self.direction_interval:
            speed = random.uniform(50, 100)
            angle = random.uniform(0, 360)
            self.velocity.x = math.sin(math.radians(angle)) * speed
            self.velocity.y = -math.cos(math.radians(angle)) * speed
            self.direction_timer = 0
            self.direction_interval = random.uniform(2.0, 4.0)
    
    def should_shoot(self) -> bool:
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot_interval = random.uniform(1.5, 3.0)
            return True
        return False
    
    def get_shoot_angle(self, target_pos: Vector2) -> float:
        # Aim towards target with some inaccuracy
        dx = target_pos.x - self.position.x
        dy = target_pos.y - self.position.y
        angle = math.degrees(math.atan2(dx, -dy))
        
        # Add some inaccuracy
        angle += random.uniform(-30, 30)
        return angle
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Draw simple UFO shape
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.ellipse(screen, WHITE, 
                          (center[0] - 12, center[1] - 6, 24, 12), 2)
        pygame.draw.ellipse(screen, WHITE, 
                          (center[0] - 6, center[1] - 10, 12, 8), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Planetoids - ZX81 Classic Recreation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize sound mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except:
            pass  # Continue without sound if mixer fails
        
        self.state = GameState.MENU
        self.score = 0
        self.lives = 3
        self.level = 1
        
        self.ship = None
        self.bullets = []
        self.asteroids = []
        self.alien_ships = []
        self.alien_bullets = []
        
        self.alien_spawn_timer = 0
        self.alien_spawn_interval = 20.0  # Spawn alien every 20 seconds
        
        self.keys_pressed = set()
    
    def generate_sound(self, frequency: int, duration: float, volume: float = 0.1):
        """Generate a simple tone for sound effects"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time_point = float(i) / sample_rate
                wave = 4096 * math.sin(frequency * 2 * math.pi * time_point)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            sound.set_volume(volume)
            sound.play()
        except:
            pass  # Ignore sound generation errors
    
    def play_shoot_sound(self):
        """Play shooting sound effect"""
        self.generate_sound(600, 0.1, 0.05)
    
    def play_explosion_sound(self, size: int = 1):
        """Play explosion sound effect based on object size"""
        base_freq = 150
        duration = 0.2 + (size * 0.1)
        self.generate_sound(base_freq, duration, 0.08)
        
    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.start_level()
    
    def start_level(self):
        # Create ship
        self.ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.ship.invulnerable_time = 2.0  # 2 seconds of invulnerability
        self.ship.health = self.ship.max_health  # Full health for new level
        
        # Clear all objects
        self.bullets.clear()
        self.alien_ships.clear()
        self.alien_bullets.clear()
        
        # Create asteroids for this level
        self.asteroids.clear()
        num_asteroids = 4 + self.level
        
        for _ in range(num_asteroids):
            # Place asteroids away from ship
            while True:
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                
                # Make sure asteroid is not too close to ship
                distance = math.sqrt((x - self.ship.position.x)**2 + 
                                   (y - self.ship.position.y)**2)
                if distance > 100:
                    self.asteroids.append(Asteroid(x, y, 3))
                    break
        
        self.alien_spawn_timer = 0
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING and self.ship and self.ship.active:
            dt = self.clock.get_time() / 1000.0
            
            # Rotation (8-directional movement support)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.ship.rotate(-1, dt)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.ship.rotate(1, dt)
            
            # Thrust
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.ship.thrust(dt)
            
            # Shooting
            if keys[pygame.K_SPACE]:
                if pygame.K_SPACE not in self.keys_pressed:
                    self.shoot_bullet()
                self.keys_pressed.add(pygame.K_SPACE)
            else:
                self.keys_pressed.discard(pygame.K_SPACE)
            
            # Hyperspace (panic button)
            if keys[pygame.K_h]:
                if pygame.K_h not in self.keys_pressed:
                    if not self.ship.hyperspace():
                        # Ship was destroyed in hyperspace
                        self.lives -= 1
                        if self.lives <= 0:
                            self.state = GameState.GAME_OVER
                        else:
                            self.ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            self.ship.invulnerable_time = 2.0
                            self.ship.health = self.ship.max_health
                self.keys_pressed.add(pygame.K_h)
            else:
                self.keys_pressed.discard(pygame.K_h)
    
    def shoot_bullet(self):
        if self.ship and self.ship.active:
            # Create bullet at ship position with ship rotation
            bullet = Bullet(self.ship.position.x, self.ship.position.y, self.ship.rotation)
            self.bullets.append(bullet)
            self.play_shoot_sound()
    
    def update(self, dt: float):
        if self.state != GameState.PLAYING:
            return
        
        # Update ship
        if self.ship:
            self.ship.update(dt)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not bullet.active:
                self.bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.update(dt)
        
        # Update alien ships
        for alien in self.alien_ships[:]:
            alien.update(dt)
            if not alien.active:
                self.alien_ships.remove(alien)
            elif alien.should_shoot() and self.ship and self.ship.active:
                # Alien shoots at player
                angle = alien.get_shoot_angle(self.ship.position)
                alien_bullet = Bullet(alien.position.x, alien.position.y, angle)
                self.alien_bullets.append(alien_bullet)
        
        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update(dt)
            if not bullet.active:
                self.alien_bullets.remove(bullet)
        
        # Spawn aliens
        self.alien_spawn_timer += dt
        if self.alien_spawn_timer >= self.alien_spawn_interval:
            self.spawn_alien()
            self.alien_spawn_timer = 0
        
        # Check collisions
        self.check_collisions()
        
        # Check level completion
        if not self.asteroids and not self.alien_ships:
            self.level += 1
            self.start_level()
        
        # Check game over
        if self.ship and not self.ship.active:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
            else:
                # Respawn ship with full health
                self.ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.ship.invulnerable_time = 2.0
                self.ship.health = self.ship.max_health
    
    def spawn_alien(self):
        # Spawn alien at edge of screen
        side = random.randint(0, 3)
        if side == 0:  # Top
            x, y = random.randint(0, SCREEN_WIDTH), 0
        elif side == 1:  # Right
            x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
        else:  # Left
            x, y = 0, random.randint(0, SCREEN_HEIGHT)
        
        self.alien_ships.append(AlienShip(x, y))
    
    def check_collisions(self):
        # Player bullets vs asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.collides_with(asteroid):
                    bullet.active = False
                    asteroid.active = False
                    
                    # Score based on asteroid size
                    score_values = {1: 100, 2: 50, 3: 20}
                    self.score += score_values.get(asteroid.size, 20)
                    
                    # Play explosion sound
                    self.play_explosion_sound(asteroid.size)
                    
                    # Split asteroid
                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                    
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    break
        
        # Player bullets vs aliens
        for bullet in self.bullets[:]:
            for alien in self.alien_ships[:]:
                if bullet.collides_with(alien):
                    bullet.active = False
                    alien.active = False
                    self.score += 500  # High score for aliens
                    
                    # Play alien explosion sound
                    self.play_explosion_sound(3)  # Large explosion for aliens
                    
                    self.bullets.remove(bullet)
                    self.alien_ships.remove(alien)
                    break
        
        # Ship vs asteroids
        if (self.ship and self.ship.active and self.ship.invulnerable_time <= 0):
            for asteroid in self.asteroids:
                if self.ship.collides_with(asteroid):
                    destroyed = self.ship.take_hit(DamageType.ASTEROID, damage=1)
                    if destroyed:
                        self.ship.active = False
                    break
        
        # Ship vs aliens
        if (self.ship and self.ship.active and self.ship.invulnerable_time <= 0):
            for alien in self.alien_ships:
                if self.ship.collides_with(alien):
                    destroyed = self.ship.take_hit(DamageType.ALIEN_SHIP, damage=2)  # Aliens do more damage
                    if destroyed:
                        self.ship.active = False
                    alien.active = False
                    break
        
        # Ship vs alien bullets
        if (self.ship and self.ship.active and self.ship.invulnerable_time <= 0):
            for bullet in self.alien_bullets[:]:
                if self.ship.collides_with(bullet):
                    destroyed = self.ship.take_hit(DamageType.ALIEN_BULLET, damage=1)
                    if destroyed:
                        self.ship.active = False
                    bullet.active = False
                    self.alien_bullets.remove(bullet)
                    break
    
    def draw_hud(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))
        
        # Health display
        if self.ship:
            health_text = self.small_font.render(f"Health: {self.ship.health}/{self.ship.max_health}", True, WHITE)
            self.screen.blit(health_text, (10, 130))
            
            # Health bar
            bar_width = 100
            bar_height = 10
            bar_x = 10
            bar_y = 150
            
            health_percent = self.ship.health / self.ship.max_health
            health_color = GREEN if health_percent > 0.6 else (YELLOW if health_percent > 0.3 else RED)
            
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            pygame.draw.rect(self.screen, health_color, 
                           (bar_x + 1, bar_y + 1, int((bar_width - 2) * health_percent), bar_height - 2))
        
        # Fuel gauge
        if self.ship:
            fuel_percent = self.ship.fuel / self.ship.max_fuel
            fuel_color = GREEN if fuel_percent > 0.3 else (RED if fuel_percent > 0.1 else RED)
            
            fuel_text = self.small_font.render(f"Fuel: {int(fuel_percent * 100)}%", True, fuel_color)
            self.screen.blit(fuel_text, (SCREEN_WIDTH - 120, 10))
            
            # Fuel bar
            bar_width = 100
            bar_height = 10
            bar_x = SCREEN_WIDTH - 120
            bar_y = 35
            
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
            pygame.draw.rect(self.screen, fuel_color, 
                           (bar_x + 1, bar_y + 1, int((bar_width - 2) * fuel_percent), bar_height - 2))
        
        # Hyperspace cooldown
        if self.ship and self.ship.hyperspace_cooldown > 0:
            cooldown_text = self.small_font.render(f"Hyperspace: {self.ship.hyperspace_cooldown:.1f}s", True, YELLOW)
            self.screen.blit(cooldown_text, (SCREEN_WIDTH - 180, 55))
        
        # Damage type indicator (for debugging/feedback)
        if self.ship and self.ship.hit_flash_time > 0 and self.ship.damage_type:
            damage_names = {
                DamageType.ASTEROID: "Asteroid Hit!",
                DamageType.ALIEN_SHIP: "Alien Collision!",
                DamageType.ALIEN_BULLET: "Alien Fire!",
                DamageType.HYPERSPACE: "Hyperspace Malfunction!"
            }
            damage_text = self.small_font.render(damage_names.get(self.ship.damage_type, "Hit!"), True, self.ship.get_flash_color())
            damage_rect = damage_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(damage_text, damage_rect)
    
    def draw_menu(self):
        title_text = self.font.render("PLANETOIDS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render("ZX81 Classic Recreation", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        instructions = [
            "Arrow Keys / WASD: Move and Rotate",
            "Space: Shoot",
            "H: Hyperspace (Panic Button)",
            "",
            "Destroy asteroids and alien ships!",
            "Manage your fuel wisely to get home safely.",
            "",
            "Press ENTER to Start"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 20
        for instruction in instructions:
            if instruction:
                text = self.small_font.render(instruction, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        restart_text = self.small_font.render("Press ENTER to Play Again or ESC to Quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            # Draw all game objects
            if self.ship:
                self.ship.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            for asteroid in self.asteroids:
                asteroid.draw(self.screen)
            
            for alien in self.alien_ships:
                alien.draw(self.screen)
            
            for bullet in self.alien_bullets:
                bullet.draw(self.screen)
            
            self.draw_hud()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        if self.state == GameState.MENU:
                            self.reset_game()
                            self.state = GameState.PLAYING
                        elif self.state == GameState.GAME_OVER:
                            self.reset_game()
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_p and self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_p and self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
            
            # Handle continuous input
            self.handle_input()
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
