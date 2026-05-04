import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spacecraft vs Asteroids - Fire & Destroy!")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 70, 220)
ORANGE = (255, 150, 50)
CYAN = (0, 200, 255)

# Game states
PLAYING = "playing"
GAME_OVER = "game_over"
MENU = "menu"

class Spacecraft:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100
        self.speed = 6
        self.color = BLUE
        self.health = 100
        self.max_health = 100
        self.ammo = 50
        self.max_ammo = 50
        self.reload_time = 0
        self.weapon_cooldown = 0
        self.weapon_level = 1  # 1: single shot, 2: double shot, 3: triple shot
        
    def draw(self):
        # Draw the spacecraft (a detailed triangle with weapons)
        points = [
            (self.x + self.width // 2, self.y),  # Top point
            (self.x, self.y + self.height),      # Bottom left
            (self.x + self.width, self.y + self.height)  # Bottom right
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw a cockpit
        pygame.draw.circle(screen, CYAN, 
                          (self.x + self.width // 2, self.y + 15), 8)
        
        # Draw engines
        pygame.draw.rect(screen, RED, 
                        (self.x + 5, self.y + self.height - 10, 12, 15))
        pygame.draw.rect(screen, RED, 
                        (self.x + self.width - 17, self.y + self.height - 10, 12, 15))
        
        # Draw weapon ports based on weapon level
        if self.weapon_level >= 1:
            # Center weapon
            pygame.draw.rect(screen, ORANGE, 
                           (self.x + self.width // 2 - 4, self.y - 5, 8, 10))
        
        if self.weapon_level >= 2:
            # Left weapon
            pygame.draw.rect(screen, ORANGE, 
                           (self.x + 10, self.y + 5, 8, 10))
            # Right weapon
            pygame.draw.rect(screen, ORANGE, 
                           (self.x + self.width - 18, self.y + 5, 8, 10))
        
        if self.weapon_level >= 3:
            # Additional weapons
            pygame.draw.rect(screen, ORANGE, 
                           (self.x + self.width // 4 - 4, self.y, 8, 10))
            pygame.draw.rect(screen, ORANGE, 
                           (self.x + 3 * self.width // 4 - 4, self.y, 8, 10))
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def fire(self, projectiles):
        if self.ammo > 0 and self.weapon_cooldown <= 0:
            if self.weapon_level == 1:
                # Single shot from center
                projectiles.append(Projectile(self.x + self.width // 2 - 2, self.y, 1))
                self.ammo -= 1
                
            elif self.weapon_level == 2:
                # Double shot from sides
                projectiles.append(Projectile(self.x + 10, self.y + 10, 1))
                projectiles.append(Projectile(self.x + self.width - 18, self.y + 10, 1))
                self.ammo -= 2
                
            elif self.weapon_level >= 3:
                # Triple shot
                projectiles.append(Projectile(self.x + self.width // 2 - 2, self.y, 1))
                projectiles.append(Projectile(self.x + 10, self.y + 10, 1))
                projectiles.append(Projectile(self.x + self.width - 18, self.y + 10, 1))
                self.ammo -= 3
            
            self.weapon_cooldown = 10  # Cooldown in frames
            
            # Play fire sound (uncomment if you have sound)
            # pygame.mixer.Sound.play(fire_sound)
    
    def upgrade_weapon(self):
        if self.weapon_level < 3:
            self.weapon_level += 1
            return True
        return False
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def get_rect(self):
        # Return a slightly smaller rectangle for collision detection
        return pygame.Rect(self.x + 5, self.y + 5, 
                          self.width - 10, self.height - 10)
    
    def update(self):
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= 1
        
        # Auto-reload ammo
        if self.reload_time > 0:
            self.reload_time -= 1
        elif self.ammo < self.max_ammo:
            self.ammo += 1
            self.reload_time = 30  # Reload 1 ammo every 30 frames

class Projectile:
    def __init__(self, x, y, damage=1):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 10
        self.damage = damage
        self.color = YELLOW
        
    def draw(self):
        # Draw the projectile with a glowing effect
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, ORANGE, 
                        (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
        
        # Draw a small glow effect
        glow_radius = 3
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 100, 100), 
                          (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (self.x + self.width // 2 - glow_radius, 
                                  self.y + self.height // 2 - glow_radius))
    
    def update(self):
        self.y -= self.speed
        return self.y < -self.height
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Asteroid:
    def __init__(self, size=None):
        self.size = size if size else random.randint(30, 60)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(2, 8)
        self.health = max(1, self.size // 20)  # Larger asteroids have more health
        self.max_health = self.health
        self.color = (random.randint(150, 220), 
                     random.randint(100, 180), 
                     random.randint(100, 180))
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
    def draw(self):
        # Save the current transformation
        original_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Draw asteroid on the temporary surface
        pygame.draw.circle(original_surface, self.color, 
                          (self.size // 2, self.size // 2), 
                          self.size // 2)
        
        # Add crater details
        for _ in range(3):
            crater_x = random.randint(5, self.size - 5)
            crater_y = random.randint(5, self.size - 5)
            crater_size = random.randint(3, 8)
            pygame.draw.circle(original_surface, 
                              (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30), 
                              (crater_x, crater_y), crater_size)
        
        # Rotate the asteroid
        rotated_surface = pygame.transform.rotate(original_surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.size // 2, 
                                                        self.y + self.size // 2))
        
        # Draw the rotated asteroid
        screen.blit(rotated_surface, rotated_rect.topleft)
        
        # Draw health bar for damaged asteroids
        if self.health < self.max_health:
            health_width = 40
            health_height = 6
            health_x = self.x + self.size // 2 - health_width // 2
            health_y = self.y - 10
            
            # Background
            pygame.draw.rect(screen, (50, 50, 50), 
                            (health_x, health_y, health_width, health_height))
            
            # Health fill
            health_percentage = self.health / self.max_health
            fill_width = int(health_width * health_percentage)
            
            if health_percentage > 0.5:
                health_color = GREEN
            elif health_percentage > 0.25:
                health_color = YELLOW
            else:
                health_color = RED
                
            pygame.draw.rect(screen, health_color, 
                            (health_x, health_y, fill_width, health_height))
    
    def update(self):
        self.y += self.speed
        self.rotation += self.rotation_speed
        return self.y > HEIGHT
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25
        self.speed = 3
        self.type = random.choice(["ammo", "health", "weapon"])
        self.colors = {
            "ammo": YELLOW,
            "health": GREEN,
            "weapon": PURPLE
        }
        self.color = self.colors[self.type]
        self.pulse = 0
        self.pulse_speed = 0.1
        
    def draw(self):
        self.pulse += self.pulse_speed
        pulse_offset = math.sin(self.pulse) * 3
        
        # Draw the power-up with pulsing effect
        pygame.draw.circle(screen, self.color, 
                          (int(self.x + self.size // 2), 
                           int(self.y + self.size // 2 + pulse_offset)), 
                          self.size // 2)
        
        # Draw icon based on type
        if self.type == "ammo":
            # Bullet icon
            pygame.draw.rect(screen, BLACK, 
                            (self.x + 8, self.y + 7, 9, 15))
            pygame.draw.rect(screen, ORANGE, 
                            (self.x + 9, self.y + 8, 7, 13))
        elif self.type == "health":
            # Heart icon
            points = [
                (self.x + self.size // 2, self.y + 5),
                (self.x + 5, self.y + self.size - 5),
                (self.x + self.size // 2, self.y + self.size - 2),
                (self.x + self.size - 5, self.y + self.size - 5)
            ]
            pygame.draw.polygon(screen, BLACK, points)
            pygame.draw.polygon(screen, RED, [
                (self.x + self.size // 2, self.y + 6),
                (self.x + 6, self.y + self.size - 6),
                (self.x + self.size // 2, self.y + self.size - 3),
                (self.x + self.size - 6, self.y + self.size - 6)
            ])
        elif self.type == "weapon":
            # Star icon
            star_points = []
            for i in range(5):
                angle = math.pi / 2 + i * 2 * math.pi / 5
                outer_radius = self.size // 2 - 2
                inner_radius = outer_radius // 2
                
                # Outer point
                x_outer = self.x + self.size // 2 + outer_radius * math.cos(angle)
                y_outer = self.y + self.size // 2 + outer_radius * math.sin(angle)
                star_points.append((x_outer, y_outer))
                
                # Inner point
                angle += math.pi / 5
                x_inner = self.x + self.size // 2 + inner_radius * math.cos(angle)
                y_inner = self.y + self.size // 2 + inner_radius * math.sin(angle)
                star_points.append((x_inner, y_inner))
            
            pygame.draw.polygon(screen, BLACK, star_points)
            pygame.draw.polygon(screen, CYAN, [
                (point[0] + (1 if point[0] < self.x + self.size // 2 else -1),
                 point[1] + (1 if point[1] < self.y + self.size // 2 else -1))
                for point in star_points
            ])
    
    def update(self):
        self.y += self.speed
        return self.y > HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont(None, 36)
        
    def draw(self):
        # Draw button with hover effect
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        # Draw text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.growth_rate = 2
        self.color = ORANGE
        self.active = True
        
    def draw(self):
        if self.active:
            # Draw explosion with multiple circles for effect
            pygame.draw.circle(screen, self.color, 
                              (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, YELLOW, 
                              (int(self.x), int(self.y)), self.radius - 5)
            pygame.draw.circle(screen, RED, 
                              (int(self.x), int(self.y)), self.radius - 10)
    
    def update(self):
        self.radius += self.growth_rate
        if self.radius > self.max_radius:
            self.active = False
        return not self.active

class Game:
    def __init__(self):
        self.state = MENU
        self.spacecraft = Spacecraft()
        self.asteroids = []
        self.projectiles = []
        self.powerups = []
        self.explosions = []
        self.score = 0
        self.game_over_time = 0
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.spawn_delay = 40
        self.level = 1
        self.asteroids_destroyed = 0
        
        # Create buttons
        button_width = 180
        button_height = 50
        button_x = WIDTH // 2 - button_width // 2
        
        self.play_button = Button(button_x, HEIGHT // 2 - 70, 
                                 button_width, button_height, 
                                 "Start Mission", GREEN, (30, 200, 80))
        self.exit_button = Button(button_x, HEIGHT // 2 + 10, 
                                 button_width, button_height, 
                                 "Exit Game", RED, (200, 30, 30))
        self.restart_button = Button(button_x, HEIGHT // 2 + 40, 
                                    button_width, button_height, 
                                    "New Mission", BLUE, (30, 100, 200))
        
        # Load font for UI
        self.ui_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 72)
        self.score_font = pygame.font.SysFont(None, 48)
    
    def reset(self):
        self.spacecraft = Spacecraft()
        self.asteroids = []
        self.projectiles = []
        self.powerups = []
        self.explosions = []
        self.score = 0
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.spawn_delay = 40
        self.level = 1
        self.asteroids_destroyed = 0
        self.state = PLAYING
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == MENU:
                self.play_button.check_hover(mouse_pos)
                self.exit_button.check_hover(mouse_pos)
                
                if self.play_button.is_clicked(mouse_pos, event):
                    self.reset()
                
                if self.exit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
            
            elif self.state == GAME_OVER:
                self.restart_button.check_hover(mouse_pos)
                self.exit_button.check_hover(mouse_pos)
                
                if self.restart_button.is_clicked(mouse_pos, event):
                    self.reset()
                
                if self.exit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
            
            elif self.state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = MENU
                    elif event.key == pygame.K_SPACE:
                        # Fire projectiles
                        self.spacecraft.fire(self.projectiles)
                
                # Continuous fire when holding space
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.spacecraft.fire(self.projectiles)
    
    def update(self):
        if self.state == PLAYING:
            # Update spacecraft
            self.spacecraft.update()
            
            # Handle spacecraft movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.spacecraft.move("left")
            if keys[pygame.K_RIGHT]:
                self.spacecraft.move("right")
            
            # Spawn asteroids
            self.asteroid_spawn_timer += 1
            if self.asteroid_spawn_timer >= self.spawn_delay:
                self.asteroids.append(Asteroid())
                self.asteroid_spawn_timer = 0
                # Gradually increase difficulty
                self.spawn_delay = max(20, self.spawn_delay - 0.05)
                
                # Level up every 10 asteroids
                if len(self.asteroids) % 10 == 0:
                    self.level += 1
            
            # Spawn powerups occasionally
            self.powerup_spawn_timer += 1
            if self.powerup_spawn_timer >= 300:  # Every 5 seconds at 60 FPS
                if random.random() < 0.3:  # 30% chance
                    x = random.randint(50, WIDTH - 50)
                    self.powerups.append(PowerUp(x, -30))
                self.powerup_spawn_timer = 0
            
            # Update asteroids
            for asteroid in self.asteroids[:]:
                if asteroid.update():
                    self.asteroids.remove(asteroid)
            
            # Update projectiles
            for projectile in self.projectiles[:]:
                if projectile.update():
                    self.projectiles.remove(projectile)
            
            # Update powerups
            for powerup in self.powerups[:]:
                if powerup.update():
                    self.powerups.remove(powerup)
            
            # Update explosions
            for explosion in self.explosions[:]:
                if explosion.update():
                    self.explosions.remove(explosion)
            
            # Check projectile-asteroid collisions
            for projectile in self.projectiles[:]:
                projectile_rect = projectile.get_rect()
                for asteroid in self.asteroids[:]:
                    if projectile_rect.colliderect(asteroid.get_rect()):
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)
                        
                        # Create explosion
                        self.explosions.append(Explosion(
                            asteroid.x + asteroid.size // 2,
                            asteroid.y + asteroid.size // 2
                        ))
                        
                        # Damage asteroid
                        if asteroid.take_damage(projectile.damage):
                            # Asteroid destroyed
                            self.asteroids.remove(asteroid)
                            self.score += asteroid.size
                            self.asteroids_destroyed += 1
                            
                            # Chance to spawn powerup
                            if random.random() < 0.2:  # 20% chance
                                self.powerups.append(PowerUp(
                                    asteroid.x + asteroid.size // 2 - 12,
                                    asteroid.y + asteroid.size // 2 - 12
                                ))
                        
                        break
            
            # Check spacecraft-asteroid collisions
            spacecraft_rect = self.spacecraft.get_rect()
            for asteroid in self.asteroids[:]:
                if spacecraft_rect.colliderect(asteroid.get_rect()):
                    # Create explosion
                    self.explosions.append(Explosion(
                        asteroid.x + asteroid.size // 2,
                        asteroid.y + asteroid.size // 2
                    ))
                    
                    # Damage spacecraft
                    damage = asteroid.size // 10
                    if self.spacecraft.take_damage(damage):
                        self.state = GAME_OVER
                        self.game_over_time = pygame.time.get_ticks()
                    
                    # Remove asteroid
                    self.asteroids.remove(asteroid)
                    break
            
            # Check spacecraft-powerup collisions
            for powerup in self.powerups[:]:
                if spacecraft_rect.colliderect(powerup.get_rect()):
                    # Apply powerup effect
                    if powerup.type == "ammo":
                        self.spacecraft.ammo = min(self.spacecraft.max_ammo, 
                                                  self.spacecraft.ammo + 20)
                    elif powerup.type == "health":
                        self.spacecraft.health = min(self.spacecraft.max_health, 
                                                    self.spacecraft.health + 30)
                    elif powerup.type == "weapon":
                        if self.spacecraft.upgrade_weapon():
                            # Show weapon upgrade message
                            pass
                    
                    # Create collection effect
                    self.explosions.append(Explosion(
                        powerup.x + powerup.size // 2,
                        powerup.y + powerup.size // 2
                    ))
                    
                    # Remove powerup
                    self.powerups.remove(powerup)
    
    def draw_ui(self):
        # Draw health bar
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20
        
        # Health bar background
        pygame.draw.rect(screen, (50, 50, 50), 
                        (health_x, health_y, health_width, health_height))
        
        # Health fill
        health_percentage = self.spacecraft.health / self.spacecraft.max_health
        fill_width = int(health_width * health_percentage)
        
        if health_percentage > 0.5:
            health_color = GREEN
        elif health_percentage > 0.25:
            health_color = YELLOW
        else:
            health_color = RED
            
        pygame.draw.rect(screen, health_color, 
                        (health_x, health_y, fill_width, health_height))
        
        # Health text
        health_text = self.ui_font.render(f"Shield: {int(self.spacecraft.health)}%", 
                                         True, WHITE)
        screen.blit(health_text, (health_x, health_y + 25))
        
        # Draw ammo indicator
        ammo_width = 200
        ammo_height = 20
        ammo_x = 20
        ammo_y = 60
        
        # Ammo bar background
        pygame.draw.rect(screen, (50, 50, 50), 
                        (ammo_x, ammo_y, ammo_width, ammo_height))
        
        # Ammo fill
        ammo_percentage = self.spacecraft.ammo / self.spacecraft.max_ammo
        fill_width = int(ammo_width * ammo_percentage)
        pygame.draw.rect(screen, YELLOW, 
                        (ammo_x, ammo_y, fill_width, ammo_height))
        
        # Ammo text
        ammo_text = self.ui_font.render(f"Ammo: {self.spacecraft.ammo}/{self.spacecraft.max_ammo}", 
                                       True, WHITE)
        screen.blit(ammo_text, (ammo_x, ammo_y + 25))
        
        # Draw score
        score_text = self.ui_font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 20))
        
        # Draw level
        level_text = self.ui_font.render(f"Level: {self.level}", True, CYAN)
        screen.blit(level_text, (WIDTH - 150, 50))
        
        # Draw asteroids destroyed
        destroyed_text = self.ui_font.render(f"Asteroids Destroyed: {self.asteroids_destroyed}", 
                                           True, GREEN)
        screen.blit(destroyed_text, (WIDTH - 250, 80))
        
        # Draw weapon level
        weapon_text = self.ui_font.render(f"Weapon: Level {self.spacecraft.weapon_level}", 
                                         True, ORANGE)
        screen.blit(weapon_text, (WIDTH - 180, 110))
        
        # Draw controls help
        controls_text = self.ui_font.render("Controls: ← → Move, SPACE Fire, ESC Menu", 
                                          True, (150, 150, 200))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 30))
    
    def draw(self):
        screen.fill(BLACK)
        
        # Draw stars in the background
        for i in range(150):
            x = (pygame.time.get_ticks() // 50 + i * 97) % WIDTH
            y = (i * 83) % HEIGHT
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
        
        if self.state == PLAYING:
            # Draw game elements
            for explosion in self.explosions:
                explosion.draw()
            
            for powerup in self.powerups:
                powerup.draw()
            
            for projectile in self.projectiles:
                projectile.draw()
            
            for asteroid in self.asteroids:
                asteroid.draw()
            
            self.spacecraft.draw()
            
            # Draw UI
            self.draw_ui()
        
        elif self.state == GAME_OVER:
            # Draw game over screen
            current_time = pygame.time.get_ticks()
            
            # Show "Game Over" for 2 seconds
            if current_time - self.game_over_time < 2000:
                game_over_text = self.title_font.render("MISSION FAILED", True, RED)
                screen.blit(game_over_text, 
                           (WIDTH // 2 - game_over_text.get_width() // 2, 
                            HEIGHT // 2 - 100))
                
                # Draw final score
                final_score = self.score_font.render(f"Final Score: {self.score}", True, YELLOW)
                screen.blit(final_score, 
                           (WIDTH // 2 - final_score.get_width() // 2, 
                            HEIGHT // 2 - 30))
                
                # Draw asteroids destroyed
                destroyed = self.ui_font.render(f"Asteroids Destroyed: {self.asteroids_destroyed}", 
                                              True, GREEN)
                screen.blit(destroyed, 
                           (WIDTH // 2 - destroyed.get_width() // 2, 
                            HEIGHT // 2 + 10))
            else:
                # Show buttons after 2 seconds
                game_over_text = self.title_font.render("MISSION FAILED", True, RED)
                screen.blit(game_over_text, 
                           (WIDTH // 2 - game_over_text.get_width() // 2, 
                            HEIGHT // 2 - 180))
                
                # Draw final stats
                final_score = self.score_font.render(f"Final Score: {self.score}", True, YELLOW)
                screen.blit(final_score, 
                           (WIDTH // 2 - final_score.get_width() // 2, 
                            HEIGHT // 2 - 120))
                
                destroyed = self.ui_font.render(f"Asteroids Destroyed: {self.asteroids_destroyed}", 
                                              True, GREEN)
                screen.blit(destroyed, 
                           (WIDTH // 2 - destroyed.get_width() // 2, 
                            HEIGHT // 2 - 80))
                
                level_reached = self.ui_font.render(f"Level Reached: {self.level}", 
                                                   True, CYAN)
                screen.blit(level_reached, 
                           (WIDTH // 2 - level_reached.get_width() // 2, 
                            HEIGHT // 2 - 50))
                
                # Draw buttons
                self.restart_button.draw()
                self.exit_button.draw()
        
        elif self.state == MENU:
            # Draw title with glow effect
            title = self.title_font.render("ASTEROID ANNIHILATOR", True, CYAN)
            title_shadow = self.title_font.render("ASTEROID ANNIHILATOR", True, BLUE)
            
            # Draw shadow
            screen.blit(title_shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 103))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            
            # Draw subtitle
            subtitle_font = pygame.font.SysFont(None, 36)
            subtitle = subtitle_font.render("Destroy Asteroids, Collect Power-ups, Survive!", True, YELLOW)
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 180))
            
            # Draw instructions
            instr_font = pygame.font.SysFont(None, 28)
            instr1 = instr_font.render("CONTROLS:", True, GREEN)
            instr2 = instr_font.render("← → ARROWS : Move Spacecraft", True, WHITE)
            instr3 = instr_font.render("SPACEBAR   : Fire Lasers", True, WHITE)
            instr4 = instr_font.render("ESC        : Pause/Menu", True, WHITE)
            
            screen.blit(instr1, (WIDTH // 2 - 150, 240))
            screen.blit(instr2, (WIDTH // 2 - 150, 270))
            screen.blit(instr3, (WIDTH // 2 - 150, 300))
            screen.blit(instr4, (WIDTH // 2 - 150, 330))
            
            # Draw power-up info
            powerup_title = instr_font.render("POWER-UPS:", True, PURPLE)
            ammo_info = instr_font.render("YELLOW : Ammo Refill", True, YELLOW)
            health_info = instr_font.render("GREEN  : Shield Repair", True, GREEN)
            weapon_info = instr_font.render("PURPLE : Weapon Upgrade", True, PURPLE)
            
            screen.blit(powerup_title, (WIDTH // 2 - 150, 380))
            screen.blit(ammo_info, (WIDTH // 2 - 150, 410))
            screen.blit(health_info, (WIDTH // 2 - 150, 440))
            screen.blit(weapon_info, (WIDTH // 2 - 150, 470))
            
            # Draw buttons
            self.play_button.draw()
            self.exit_button.draw()
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()