import pygame
import os
import random
import time
from sprite import *
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.image_list = self.load_images("images")
        self.current_image_index = 0
        self.load_and_split_image(self.image_list[self.current_image_index])
        self.tiles = []


    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[(x + y * GAME_SIZE + 1, x, y) for x in range(GAME_SIZE)] for y in range(GAME_SIZE)]
        grid[-1][-1] = (0, GAME_SIZE - 1, GAME_SIZE - 1)  # Make the bottom-right tile empty
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    # Add boundary checks here
                    if col < GAME_SIZE - 1 and tile.right():
                        possible_moves.append(("right", row, col))
                    if col > 0 and tile.left():
                        possible_moves.append(("left", row, col))
                    if row > 0 and tile.up():
                        possible_moves.append(("up", row, col))
                    if row < GAME_SIZE - 1 and tile.down():
                        possible_moves.append(("down", row, col))
                    break
            if possible_moves:
                break

        if not possible_moves:
            return  # No moves possible, exit the function

        # Choose a random move from the possible moves
        choice, row, col = random.choice(possible_moves)
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

        # After shuffling, redraw tiles
        self.draw_tiles()
        
    def draw_tiles(self):
        for sprite in self.all_sprites:
            sprite.kill()

        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                tile_value, orig_x, orig_y = self.tiles_grid[row][col]
                if tile_value != 0:
                    image_tile = self.image_tiles[orig_y][orig_x]
                    self.tiles[row][col] = Tile(self, col, row, str(tile_value), image_tile, (orig_x, orig_y))
                else:
                    self.tiles[row][col] = Tile(self, col, row, "empty", None, (GAME_SIZE - 1, GAME_SIZE - 1))

        self.all_sprites.update()

    def load_and_split_image(self, image_path):
        full_image = pygame.image.load(image_path)
        full_image = pygame.transform.scale(full_image, (TILESIZE * GAME_SIZE, TILESIZE * GAME_SIZE))
        self.image_tiles = []
        for row in range(GAME_SIZE):
            self.image_tiles.append([])
            for col in range(GAME_SIZE):
                tile_surface = pygame.Surface((TILESIZE, TILESIZE))
                tile_surface.blit(full_image, (0, 0), (col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE))
                self.image_tiles[row].append(tile_surface)

    def swap_image(self):
        # Assuming you have a list of image paths
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.load_and_split_image(self.image_list[self.current_image_index])
        self.draw_tiles()
    
    def load_images(self, directory):
        images = []
        for filename in os.listdir(directory):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(directory, filename)
                images.append(path)
        return images

    def new(self):
        self.all_sprites = pygame.sprite.Group()

        # Initialize the tiles grid
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()

        # Initialize self.tiles as a 2D list
        self.tiles = [[None for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]

        # Now it's safe to call draw_tiles
        self.draw_tiles()

        # Initialize other attributes
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "Swap", WHITE, BLACK))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            # Check if the empty tile is adjacent and swap
                            if col < GAME_SIZE - 1 and self.tiles[row][col + 1].text == "empty":
                                self.swap_tiles(row, col, row, col + 1)
                            elif col > 0 and self.tiles[row][col - 1].text == "empty":
                                self.swap_tiles(row, col, row, col - 1)
                            elif row > 0 and self.tiles[row - 1][col].text == "empty":
                                self.swap_tiles(row, col, row - 1, col)
                            elif row < GAME_SIZE - 1 and self.tiles[row + 1][col].text == "empty":
                                self.swap_tiles(row, col, row + 1, col)

                # Check for button clicks
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        elif button.text == "Reset":
                            self.new()
                        elif button.text == "Swap":
                            self.swap_image()

    def swap_tiles(self, row1, col1, row2, col2):
        # Swap the positions of the tiles in the grid
        self.tiles_grid[row1][col1], self.tiles_grid[row2][col2] = self.tiles_grid[row2][col2], self.tiles_grid[row1][col1]
        # Swap the tile objects themselves
        self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1]
        # Update the positions of the tiles
        self.tiles[row1][col1].x, self.tiles[row1][col1].y = col1, row1
        self.tiles[row2][col2].x, self.tiles[row2][col2].y = col2, row2
        # Redraw the tiles
        self.draw_tiles()
        

game = Game()
while True:
    game.new()
    game.run()