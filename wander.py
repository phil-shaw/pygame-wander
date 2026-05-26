import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Vehicle:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 2
        self.acceleration = pygame.Vector2(0, 0)

        # Behavior constraints
        self.max_speed = 3
        self.max_force = 0.05

        # Wander configuration
        self.wander_ring_distance = 100
        self.wander_ring_radius = 50
        self.wander_angle = 0
        self.angle_change_range = 0.25  # Maximum radians to turn per frame

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration each frame
        self.edges()

    def apply_force(self, force):
        self.acceleration += force

    def wander(self):
        # 1. Project circle ahead
        circle_center = self.velocity.copy()
        if circle_center.length() > 0:
            circle_center.scale_to_length(self.wander_ring_distance)
        circle_center += self.position

        # 2. Update heading displacement angle
        self.wander_angle += random.uniform(-self.angle_change_range, self.angle_change_range)

        # 3. Calculate target position on the circle circumference
        displacement = pygame.Vector2(
            self.wander_ring_radius * math.cos(self.wander_angle),
            self.wander_ring_radius * math.sin(self.wander_angle)
        )
        target = circle_center + displacement

        # 4. Standard seek behavior towards target
        desired_velocity = (target - self.position).normalize() * self.max_speed
        steering_force = desired_velocity - self.velocity

        if steering_force.length() > self.max_force:
            steering_force.scale_to_length(self.max_force)

        self.apply_force(steering_force)

        # Draw the debugging guides
        self.draw_debug(circle_center, target)

    def edges(self):
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def draw_debug(self, center, target):
        # Draw projection line
        pygame.draw.line(screen, (100, 100, 100), self.position, center, 1)
        # Draw wander circle radius perimeter
        pygame.draw.circle(screen, (0, 255, 0), (int(center.x), int(center.y)), self.wander_ring_radius, 1)
        # Draw target hub point
        pygame.draw.circle(screen, (255, 0, 0), (int(target.x), int(target.y)), 4)

    def draw(self):
        # Draw the agent triangle facing the velocity vector
        angle = math.atan2(self.velocity.y, self.velocity.x)
        size = 8
        p1 = self.position + pygame.Vector2(size * 2, 0).rotate(math.degrees(angle))
        p2 = self.position + pygame.Vector2(-size, -size // 2).rotate(math.degrees(angle))
        p3 = self.position + pygame.Vector2(-size, size // 2).rotate(math.degrees(angle))
        pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3])


# Create agent instance
agent = Vehicle(WIDTH // 2, HEIGHT // 2)

# Main Application Loop
running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    agent.wander()
    agent.update()
    agent.draw()

    pygame.display.flip()

pygame.quit()
