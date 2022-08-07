# simple game

import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
myWindow = pygame.display.set_mode((WIDTH, HEIGHT))


def calc_dist(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calc_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw(window, bg, space, draw_options, line, ss):
    # window.fill("white")
    bg_pos = (0, 0)
    if ss[1][2] == 0 and ss[1][3] == 0:
        # window.fill("white")
        my_font = pygame.font.SysFont(pygame.font.get_default_font(), 46)
        bg = my_font.render('Game finish!', True, (255, 0, 0))
        bg_pos = (400, 300)
        #  my_font.render_to(window, (40, 350), "Hello World!", (0, 0, 0))
    else:
        # Drawing START
        pygame.draw.rect(bg, GREEN, pygame.Rect(*ss[0]))
        # Drawing END
        pygame.draw.rect(bg, RED, pygame.Rect(*ss[1]))

    window.blit(bg, bg_pos)
    # pygame.display.flip()

    space.debug_draw(draw_options)
    if line:
        color = "black"
        if (calc_dist(*line) * 5) / 14 >= 100:
            color = "red"
        pygame.draw.line(window, color, line[0], line[1], 3)
    pygame.display.update()


def create_boundaries(space, width, height):
    reacts = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)],
    ]
    for pos, size in reacts:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        # shape.mass = 10
        shape.color = SILVER
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


WHITE = (255, 255, 255, 100)
BROWN = (129, 69, 19, 100)
RED = (255, 0, 0, 100)
YELLOW = (255, 255, 0, 100)
MAGENTA = (255, 0, 255, 100)
CYAN = (0, 255, 255, 100)
LIME = (0, 255, 0, 100)
GREEN = (0, 128, 0, 100)
GREEN_GOAL = (204, 255, 229, 80)
BLUE = (0, 0, 255, 100)
SILVER = (192, 192, 192, 100)
DARK = (32, 32, 32, 100)
BLACK = (0, 0, 0, 100)


def create_swinging_ball(space, pos=(300, 300), size=10, color=DARK):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = pos

    body = pymunk.Body()
    body.position = pos
    line_size = 2
    if math.ceil(size / 10) > 2:
        line_size = math.ceil(size / 10)
    line = pymunk.Segment(body, (0, 0), (6 * size, 0), line_size)
    circle = pymunk.Circle(body, size, (6 * size, 0))
    line.friction = 1
    line.elasticity = 1
    line.mass = size * 0.2
    line.color = color
    circle.friction = 1
    circle.elasticity = 0.95
    circle.mass = size * 0.8
    circle.color = color
    rotation_center_body.color = color
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)


def create_ball(space, radius, mass, pos, color=RED):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = color
    space.add(body, shape)
    return shape


def create_box(space, width=1000, height=800, pos=None, mass=30, size=(50, 50), color=DARK, elasticity=0.4,
               friction=0.4, body_type=pymunk.Body.DYNAMIC, radius=2):
    body = pymunk.Body(body_type=body_type)
    if pos is None:
        pos = (100, 100)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size, radius=radius)
    shape.color = color
    shape.mass = mass
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape


def create_structure(space, width=1000, height=800, x_pos=None, color=BROWN):
    if x_pos is None or x_pos > width - 340:
        x_pos = width - 340
    if x_pos < 40:
        x_pos = 40
    reacts = [
        [(x_pos, height - 120), (40, 200), color, 100],  # left
        [(x_pos + 300, height - 120), (40, 200), color, 100],  # right
        [(x_pos + 150, height - 240), (340, 40), color, 150]  # top
    ]
    for pos, size, color, mass in reacts:
        create_box(space, width=width, height=height, pos=pos, mass=mass, size=size, color=color)


def set_level(width, height, level=1):
    space = pymunk.Space()
    space.gravity = (0, 981)
    ss = None
    lives = 2
    bg = pygame.Surface((width, height))
    bg.fill("white")

    create_boundaries(space, width, height)
    if level == 1:
        create_structure(space, width, height, x_pos=(width - 320))
        ss = [
            (60, height - 120, 100, 100),
            (width - 200, height - 70, 50, 50)
        ]
    elif level == 2:
        create_structure(space, width, height, x_pos=(width - 320))
        create_swinging_ball(space, pos=(450, 550), size=25)
        ss = [
            (60, height - 120, 100, 100),
            (width - 200, height - 70, 50, 50)
        ]
    elif level == 3:
        reacts = [
            [(180, height - 30), (20, 20), BLUE, 20], [(200, height - 30), (20, 20), BLUE, 20],
            [(220, height - 30), (20, 20), BLUE, 20], [(240, height - 30), (20, 20), BLUE, 20],
            [(180, height - 50), (20, 20), BLUE, 20], [(200, height - 50), (20, 20), BLUE, 20],
            [(220, height - 50), (20, 20), BLUE, 20], [(240, height - 50), (20, 20), BLUE, 20],
            [(180, height - 70), (20, 20), BLUE, 20], [(200, height - 70), (20, 20), BLUE, 20],
            [(220, height - 70), (20, 20), BLUE, 20], [(240, height - 70), (20, 20), BLUE, 20],
            [(180, height - 90), (20, 20), BLUE, 20], [(200, height - 90), (20, 20), BLUE, 20],
            [(220, height - 90), (20, 20), BLUE, 20], [(240, height - 90), (20, 20), BLUE, 20],
        ]
        for pos, size, color, mass in reacts:
            create_box(space, width=width, height=height, pos=pos, mass=mass, size=size, color=color, radius=0)
        create_box(space, width=width, height=height, pos=(120, 600), mass=50, size=(200, 50), color=SILVER,
                   body_type=pymunk.Body.STATIC, radius=0)
        create_swinging_ball(space, pos=(500, 600), size=25)
        ss = [
            (width - 200, height - 70, 50, 50),
            (60, height - 120, 100, 100)
        ]
        lives = 1
    elif level == 4:
        reacts = [
            [(380, height - 30), (20, 20), BLUE, 20], [(400, height - 30), (20, 20), GREEN, 30],
            [(420, height - 30), (20, 20), BLUE, 20], [(440, height - 30), (20, 20), GREEN, 30],
            [(380, height - 50), (20, 20), BLUE, 20], [(400, height - 50), (20, 20), GREEN, 30],
            [(420, height - 50), (20, 20), BLUE, 20], [(440, height - 50), (20, 20), GREEN, 30],
            [(380, height - 70), (20, 20), BLUE, 20], [(400, height - 70), (20, 20), GREEN, 30],
            [(420, height - 70), (20, 20), BLUE, 20], [(440, height - 70), (20, 20), GREEN, 30],
            [(380, height - 90), (20, 20), BLUE, 20], [(400, height - 90), (20, 20), GREEN, 30],
            [(420, height - 90), (20, 20), BLUE, 20], [(440, height - 90), (20, 20), GREEN, 30],
            [(380, height - 110), (20, 20), BLUE, 20], [(400, height - 110), (20, 20), GREEN, 30],
            [(420, height - 110), (20, 20), BLUE, 20], [(440, height - 110), (20, 20), GREEN, 30],
            [(380, height - 130), (20, 20), BLUE, 20], [(400, height - 130), (20, 20), GREEN, 30],
            [(420, height - 130), (20, 20), BLUE, 20], [(440, height - 130), (20, 20), GREEN, 30],
            [(380, height - 150), (20, 20), BLUE, 20], [(400, height - 150), (20, 20), GREEN, 30],
            [(420, height - 150), (20, 20), BLUE, 20], [(440, height - 150), (20, 20), GREEN, 30],
        ]
        for pos, size, color, mass in reacts:
            create_box(space, width=width, height=height, pos=pos, mass=mass, size=size, color=color, radius=0)
        create_box(space, width=width, height=height, pos=(120, 600), mass=50, size=(200, 50), color=SILVER,
                   body_type=pymunk.Body.STATIC, radius=0)
        ss = [
            (width - 200, height - 70, 50, 50),
            (60, height - 120, 100, 100)
        ]
        lives = 1
    else:
        ss = [
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ]

    return space, bg, ss, lives


def check_intersect(circle=None, rectangle=None, point=None):
    x1, x2, y1, y2, bx, by = None, None, None, None, None, None
    if rectangle:
        x1 = rectangle[0]
        x2 = x1 + rectangle[2]
        y1 = rectangle[1]
        y2 = y1 + rectangle[3]
        radio = 0
        if circle:
            radio = 10
            bx = circle.body.position.x
            by = circle.body.position.y
        elif point:
            bx = point[0]
            by = point[1]
        else:
            return False
        if x1 < bx + radio and x2 > bx - radio and \
                y1 < by + radio and y2 > by - radio:
            return True
    return False


def run(window, width, height):
    running = True
    clock = pygame.time.Clock()
    fps = 60

    draw_options = pymunk.pygame_util.DrawOptions(window)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    # | pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

    pressed_pos = None
    ball = None
    lvl = 1
    space, bg, ss, lives = set_level(width, height, level=lvl)

    while running:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]
        if check_intersect(ball, ss[1]):
            if ball:
                space.remove(ball, ball.body)
                ball = None
            lvl += 1
            space, bg, ss, lives = set_level(width, height, level=lvl)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball and check_intersect(None, ss[0], pygame.mouse.get_pos()):
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 10, 10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calc_angle(*line)
                    force = calc_dist(*line) * 50
                    if force > 14000:
                        force = 10
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                elif ball:
                    space.remove(ball, ball.body)
                    ball = None
                    lives -= 1
                    if lives <= 0:
                        space, bg, ss, lives = set_level(width, height, level=lvl)
        if lvl > 4:
            pygame.display.set_caption('THE END')
        draw(window, bg, space, draw_options, line, ss)
        space.step(1.0 / fps)
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    print('start')
    run(myWindow, WIDTH, HEIGHT)
    print('end')
