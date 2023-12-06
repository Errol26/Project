import pygame
import os
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
WIDTH, HEIGHT = 1320, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))

FRUIT_COLORS = {
    "apple": (255, 0, 0),
}

# Hunger Bar
HUNGER_BAR_WIDTH = 200
HUNGER_BAR_HEIGHT = 20
HUNGER_BAR_COLOR = (255, 0, 0)
hunger_level = 100  # Initial hunger level

# Number of apples caught
apples_caught = 0

# Load eating sound
EATING_SOUND = pygame.mixer.Sound(os.path.join("assets", "apple.wav"))

def draw_hunger_bar(hunger_level):
    pygame.draw.rect(WIN, HUNGER_BAR_COLOR, (10, 10, HUNGER_BAR_WIDTH, HUNGER_BAR_HEIGHT))
    pygame.draw.rect(WIN, (0, 255, 0), (10, 10, (hunger_level / 100) * HUNGER_BAR_WIDTH, HUNGER_BAR_HEIGHT))

    # Render the label "HUNGER"
    label_font = pygame.font.SysFont("Bauhaus 93", 18)
    label_text = label_font.render("HUNGER", 1, (255, 255, 255))
    WIN.blit(label_text, (10 + HUNGER_BAR_WIDTH // 2 - label_text.get_width() // 2, 10 + HUNGER_BAR_HEIGHT + 5))

def show_another_tab(hunger_level):
    # Create a new tab with a background and trees

    new_tab_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))

    # Resize the apple tree image
    apple_tree_img = pygame.image.load(os.path.join("assets", "apple.png"))
    apple_tree_width = 600 # Set your desired width
    apple_tree_height = 700  # Set your desired height
    apple_tree_img = pygame.transform.scale(apple_tree_img, (apple_tree_width, apple_tree_height))
    apple_tree_pos = (WIDTH // 2 - apple_tree_width // 2, HEIGHT // 2 - apple_tree_height // 2)

    apple_code_label = "Apple"

    apple_button_rect = pygame.Rect(apple_tree_pos[0] + apple_tree_width // 2 - 100, apple_tree_pos[1] + apple_tree_height + -60, 200, 30)

    run_tab = True
    show_main_menu = False
    show_game = False

    while run_tab:
        WIN.blit(new_tab_bg, (0, 0))
        WIN.blit(apple_tree_img, apple_tree_pos)

        # Draw button with fruit color
        pygame.draw.rect(WIN, (255, 0, 0), apple_button_rect)  # Red color for apple

        # Display code label as text on button with different fonts
        apple_label = pygame.font.SysFont("Bauhaus 93", 18).render(apple_code_label, 1, (255, 255, 255))
        WIN.blit(apple_label, (apple_button_rect.centerx - apple_label.get_width() // 2, apple_button_rect.centery - apple_label.get_height() // 2))

        draw_hunger_bar(hunger_level)  # Draw the hunger bar

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_tab = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if apple_button_rect.collidepoint(event.pos):
                    print("Apple button clicked!")
                    show_game = True
                    run_tab = False  # Exit the loop to start the game

    return show_main_menu, show_game

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the basket image
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "basket.png")), (150, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 30)

    def update(self):
        # Move the basket with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class Fruit(pygame.sprite.Sprite):
    def __init__(self, fruit_type):
        super().__init__()
        # Load the apple image
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "apple1.png")), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = 0
        self.speed = random.randint(5, 10)

    def update(self):
        global apples_caught, hunger_level  # Use the global variables

        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(50, WIDTH - 50)

        # Check for collisions between the basket and fruits
        collisions = pygame.sprite.spritecollide(basket, fruits, True)
        for collision in collisions:
            if isinstance(collision, Fruit) and collision.image.get_rect().size == (30, 30):  # Check if it's an apple
                apples_caught += 1  # Increment the count of caught apples
                print(f"Apples caught: {apples_caught}")

def main_game():
    global running, all_sprites, fruits, basket, apples_caught, apples_display_surface, apples_display_rect, hunger_level
    running = True  # Declare running as a global variable

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    fruits = pygame.sprite.Group()

    # Create basket object
    basket = Basket()
    all_sprites.add(basket)

    # Get the number of fruits to catch from the user
    num_fruits_to_catch = None
    font = pygame.font.Font(None, 36)
    input_text = ""

    # Load eating sound
    EATING_SOUND = pygame.mixer.Sound(os.path.join("assets", "apple.wav"))

    # Create Eat button
    eat_button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 40)

    # Game loop
    clock = pygame.time.Clock()

    apples_display_surface = pygame.Surface((230, 50))  # Define and initialize apples_display_surface
    apples_display_rect = apples_display_surface.get_rect(topright=(WIDTH - 10, 10))  # Adjust position to the top-right

    clock = pygame.time.Clock()
    time_since_last_eat = 0

    game_over = False
    while running and not game_over:
        dt = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

        time_since_last_eat += dt
        if time_since_last_eat >= 2:  # Adjust the time interval 
            hunger_level -= 5  # Decrease hunger over time
            if hunger_level < 0:
                hunger_level = 0  # Cap the hunger level at 0
                game_over = True  # Set game_over to True when hunger is zero
            time_since_last_eat = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        num_fruits_to_catch = int(input_text)
                        # Create fruit objects based on user input
                        for _ in range(num_fruits_to_catch):
                            fruit = Fruit(random.choice(list(FRUIT_COLORS.keys())))
                            all_sprites.add(fruit)
                            fruits.add(fruit)
                        input_text = ""  # Reset the input text after capturing the value
                    except ValueError:
                        print("Please enter a valid number.")
                        input_text = ""  # Reset the input text even if an error occurs
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isnumeric():
                    input_text += event.unicode

            ## Check for mouse click on the Eat button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if eat_button_rect.collidepoint(event.pos):
                    EATING_SOUND.play()
                    if apples_caught > 0:
                        apples_caught -= 1
                        hunger_level += 10  # Increase hunger when eating
                        if hunger_level > 100:
                            hunger_level = 100  # Cap the hunger level at 100


        # Update the apples display surface
        apples_display_surface.fill((0, 0, 0))  # Clear the surface
        apples_label = font.render(f"Apples caught: {apples_caught}", 1, (255, 255, 255))
        apples_display_surface.blit(apples_label, (0, 0))

        # Update sprites and check for collisions
        all_sprites.update()  # Make sure to call update for all sprites

        # Check for collisions between the basket and fruits
        collisions = pygame.sprite.spritecollide(basket, fruits, True)
        for collision in collisions:
            if isinstance(collision, Fruit) and collision.image.get_rect().size == (30, 30):  # Check if it's an apple
                apples_caught += 1  # Increment the count of caught apples
                # Increase hunger level when an apple is caught
                hunger_level += 10  # You can adjust this value based on your preference
                if hunger_level > 100:
                    hunger_level = 100  # Cap the hunger level at 100
                print(f"Apples caught: {apples_caught}")

         # Draw everything
        WIN.blit(BG, (0, 0))
        all_sprites.draw(WIN)

        # Draw a background for the input box
        input_box_width, input_box_height = 300, 40
        input_box_rect = pygame.Rect(10, HEIGHT - input_box_height - 10, input_box_width, input_box_height)
        pygame.draw.rect(WIN, (200, 200, 200), input_box_rect)

        # Draw Eat button
        pygame.draw.rect(WIN, (0, 255, 0), eat_button_rect)  # Green color for the button
        eat_label = font.render("Eat", 1, (0, 0, 0))
        WIN.blit(eat_label, (eat_button_rect.centerx - eat_label.get_width() // 2, eat_button_rect.centery - eat_label.get_height() // 2))

        # Display apples caught on the top-right and draw the hunger bar below it
        WIN.blit(apples_display_surface, apples_display_rect.topleft)
        draw_hunger_bar(hunger_level)  # Draw the hunger bar

        # Draw the input box with light blue color
        pygame.draw.rect(WIN, (173, 216, 230), (10, HEIGHT - 50, 300, 40))

        # Draw the input text
        input_surface = font.render(input_text, True, (0, 0, 0))
        WIN.blit(input_surface, (20, HEIGHT - 40))  # Adjust the position as needed
        pygame.display.flip()

    show_game_over_screen()

def reset_game():
    global hunger_level, apples_caught
    hunger_level = 100
    apples_caught = 0

def show_game_over_screen():
    title_font = pygame.font.SysFont("Bauhaus 93", 70)
    button_font = pygame.font.SysFont("Bauhaus 93", 40)

    run=True
    while run:
        game_over_bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
        title_label = title_font.render("Game Over", 1, (255, 0, 0))
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - title_label.get_height() // 2))

        retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(WIN, (255, 0, 0), retry_button)

        retry_label = button_font.render("Retry", 1, (0, 0, 0))
        WIN.blit(retry_label, (WIDTH // 2 - retry_label.get_width() // 2, HEIGHT // 2 + 55))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return_to_main_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    run = False  # Exit the loop to return to the main menu
                    return_to_main_menu = True

        pygame.display.update()

    if return_to_main_menu:
        reset_game() # Reset the game
        main_menu()  # Call the main_menu function to return to the main menu


def main_menu():
    title_font = pygame.font.SysFont("Bauhaus 93", 70)
    button_font = pygame.font.SysFont("Bauhaus 93", 40)

    run = True
    button_radius = 50
    show_main_menu = True  # Initialize to show the main menu

    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Apple in the Basket", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 250))

        if show_main_menu:
            play_button = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
            exit_button = pygame.Rect(WIDTH // 2 - 100, 420, 200, 50)

            pygame.draw.rect(WIN, (135, 206, 235), play_button)
            pygame.draw.rect(WIN, (255, 0, 0), exit_button)

            play_label = button_font.render("Play", 1, (0, 0, 0))
            exit_label = button_font.render("Exit", 1, (0, 0, 0))

            WIN.blit(play_label, (WIDTH // 2 - play_label.get_width() // 2, 355))
            WIN.blit(exit_label, (WIDTH // 2 - exit_label.get_width() // 2, 430))

            draw_hunger_bar(100)  # Pass the initial hunger level
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        show_main_menu, show_game = show_another_tab(100)  # Switch to the other tab
                        if show_game:
                            main_game()  # Call the main_game function
                    elif exit_button.collidepoint(event.pos):
                        run = False
        else:
            show_main_menu, show_game = show_another_tab(100)
            if show_game:
                main_game()  # Call the main_game function

    pygame.quit()

# Call the main_menu function to start the program
main_menu()