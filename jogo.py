import random
WIDTH = 800
HEIGHT = 600
TITLE = "Kodland Platformer"

game_state = "menu"
music_on = True

buttons = {
    "start": (WIDTH // 2, HEIGHT // 2 - 50),
    "sound": (WIDTH // 2, HEIGHT // 2 + 10),
    "exit": (WIDTH // 2, HEIGHT // 2 + 70)
}

class Player:
    def __init__(self):
        self.images_idle = ["hero_idle1", "hero_idle2"]
        self.images_run = ["hero_run1", "hero_run2", "hero_run3", "hero_run4"]
        self.image_index = 0
        self.actor = Actor(self.images_idle[0], (100, 500))
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.frame_count = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.move()
        self.animate()

    def move(self):
        keys = keyboard
        self.vx = 0
        if keys.left:
            self.vx = -3
        if keys.right:
            self.vx = 3
        self.actor.x += self.vx

        self.vy += 0.5
        self.actor.y += self.vy

        if self.actor.y >= 500:
            self.actor.y = 500
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if keys.up and self.on_ground:
            self.vy = -10
            if music_on:
                sounds.jump.play()

    def animate(self):
        self.frame_count += 1
        if self.vx != 0:
            if self.frame_count % 6 == 0:
                self.image_index = (self.image_index + 1) % len(self.images_run)
                self.actor.image = self.images_run[self.image_index]
        else:
            if self.frame_count % 15 == 0:
                self.image_index = (self.image_index + 1) % len(self.images_idle)
                self.actor.image = self.images_idle[self.image_index]

class Enemy:
    def __init__(self, x, y):
        self.images = ["enemy1", "enemy2"]
        self.image_index = 0
        self.actor = Actor(self.images[0], (x, y))
        self.direction = 1
        self.frame_count = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.actor.x += self.direction * 2
        if self.actor.x > WIDTH - 50 or self.actor.x < 50:
            self.direction *= -1
        self.animate()

    def animate(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.actor.image = self.images[self.image_index]

player = Player()
enemies = [Enemy(random.randint(200, 700), 500) for _ in range(3)]

def play_music():
    if music_on:
        music.play("background_music")

play_music()

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()

def update():
    if game_state == "game":
        player.update()
        for enemy in enemies:
            enemy.update()

def draw_menu():
    screen.draw.text("KODLAND PLATFORMER", center=(WIDTH // 2, HEIGHT // 2 - 120), fontsize=50, color="white")
    screen.draw.text("Start Game", center=buttons["start"], fontsize=40, color="yellow")
    sound_text = "Sound: ON" if music_on else "Sound: OFF"
    screen.draw.text(sound_text, center=buttons["sound"], fontsize=40, color="yellow")
    screen.draw.text("Exit", center=buttons["exit"], fontsize=40, color="yellow")

def draw_game():
    screen.blit("background", (0, 0))
    player.draw()
    for enemy in enemies:
        enemy.draw()

def on_mouse_down(pos):
    global game_state, music_on
    if game_state == "menu":
        if button_clicked(pos, buttons["start"]):
            game_state = "game"
        elif button_clicked(pos, buttons["sound"]):
            music_on = not music_on
            if music_on:
                play_music()
            else:
                music.stop()
        elif button_clicked(pos, buttons["exit"]):
            exit()

def button_clicked(pos, button_pos):
    bx, by = button_pos
    return bx - 100 < pos[0] < bx + 100 and by - 20 < pos[1] < by + 20
