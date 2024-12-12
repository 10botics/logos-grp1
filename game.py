import pygame
import sys
import time
from enum import Enum
import random
import cv2  # Add this import at the top instead of moviepy

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
BUTTON_SIZE = 200
BUTTON_SPACING = 40
SCORE_FONT_SIZE = 72  # New constant for score font size
TICK_FONT_SIZE = 36   # Also adding tick font size for consistency

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

class GameState(Enum):
    SONG_SELECT = 1
    COUNTDOWN = 2
    PLAYING = 3
    GAME_OVER = 4

class RhythmGame:
    def __init__(self):
        # Start with a default size, will be updated when video loads
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Rhythm Game")
        
        self.state = GameState.SONG_SELECT
        self.score = 0
        self.songs = [
            {"title": "APT - ROSÉ & Bruno Mars", "video": "songs/song1.mp4", "audio": "songs/song1.wav", "pattern": []},
            {"title": "Song 2", "video": "songs/song2.mp4", "audio": "songs/song2.wav", "pattern": []},
            {"title": "Song 3", "video": "songs/song3.mp4", "audio": "songs/song3.wav", "pattern": []}
        ]
        self.current_song = None
        
        # Initialize empty button lists
        self.buttons = []
        self.button_states = []
        
        self.tick = 0
        self.clock = pygame.time.Clock()
        self.FPS = 60  # Will be updated when video loads
        
        self.video = None
        self.video_frame = None
        self.frame_count = 0

    def initialize_buttons(self):
        self.buttons = []
        
        # Left side buttons (forming right arrow)
        left_center_x = 150
        left_center_y = self.screen.get_height() // 2
        self.buttons.append(pygame.Rect(left_center_x, left_center_y, BUTTON_SIZE, BUTTON_SIZE))  # Center
        self.buttons.append(pygame.Rect(left_center_x + BUTTON_SIZE, left_center_y - BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE))  # Right-top
        self.buttons.append(pygame.Rect(left_center_x + BUTTON_SIZE, left_center_y + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE))  # Right-bottom
        
        # Right side buttons (forming left arrow)
        right_center_x = self.screen.get_width() - 150 - BUTTON_SIZE
        right_center_y = self.screen.get_height() // 2
        self.buttons.append(pygame.Rect(right_center_x, right_center_y, BUTTON_SIZE, BUTTON_SIZE))  # Center
        self.buttons.append(pygame.Rect(right_center_x - BUTTON_SIZE, right_center_y - BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE))  # Left-top
        self.buttons.append(pygame.Rect(right_center_x - BUTTON_SIZE, right_center_y + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE))  # Left-bottom
        
        # Reset button states
        self.button_states = [False] * 6  # False = not lit, True = lit

    def run(self):
        while True:
            if self.state == GameState.SONG_SELECT:
                self.song_select_screen()
            elif self.state == GameState.COUNTDOWN:
                self.countdown_screen()
            elif self.state == GameState.PLAYING:
                self.game_screen()
            elif self.state == GameState.GAME_OVER:
                self.game_over_screen()

    def song_select_screen(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle song selection
                for i, song in enumerate(self.songs):
                    text = pygame.font.Font(None, 72).render(song["title"], True, WHITE)
                    text_rect = text.get_rect(center=(self.screen.get_width()//2, 300 + i*100))
                    if text_rect.collidepoint(mouse_pos):
                        self.current_song = song
                        self.state = GameState.COUNTDOWN

        self.screen.fill(BLACK)
        
        # Draw title
        title_font = pygame.font.Font(None, 100)  # Larger font for title
        title_text = title_font.render("Song Selection", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw song list with hover effect
        for i, song in enumerate(self.songs):
            # Create text rect for hover detection
            normal_font = pygame.font.Font(None, 72)
            hover_font = pygame.font.Font(None, 86)  # Bigger font for hover
            
            text_rect = normal_font.render(song["title"], True, WHITE).get_rect(center=(self.screen.get_width()//2, 300 + i*100))
            
            if text_rect.collidepoint(mouse_pos):
                # Hover effect: bigger font and yellow color
                text = hover_font.render(song["title"], True, YELLOW)
                text_rect = text.get_rect(center=(self.screen.get_width()//2, 300 + i*100))
                
                # Draw highlight rectangle
                highlight_rect = text_rect.inflate(40, 20)  # Make highlight slightly bigger than text
                pygame.draw.rect(self.screen, GRAY, highlight_rect)
            else:
                # Normal state
                text = normal_font.render(song["title"], True, WHITE)
                text_rect = text.get_rect(center=(self.screen.get_width()//2, 300 + i*100))
            
            # Draw the text
            self.screen.blit(text, text_rect)
            
        pygame.display.flip()

    def countdown_screen(self):
        # Skip countdown for testing
        self.state = GameState.PLAYING
        
        # Countdown code kept for later use
        """
        for i in range(3, 0, -1):
            self.screen.fill(BLACK)
            text = pygame.font.Font(None, 72).render(str(i), True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
            pygame.display.flip()
            time.sleep(1)
        
        self.state = GameState.PLAYING
        # Start playing music
        # pygame.mixer.music.load(self.current_song["file"])
        # pygame.mixer.music.play()
        """

    def game_screen(self):
        # Initialize video and audio if not already done
        if self.video is None:
            try:
                # First try to initialize video
                self.video = cv2.VideoCapture(self.current_song["video"])
                if not self.video.isOpened():
                    raise Exception("Could not open video file")
                
                # Get video properties
                self.FPS = int(self.video.get(cv2.CAP_PROP_FPS))
                width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(f"Video FPS: {self.FPS}, Resolution: {width}x{height}")
                
                # Resize window to match video
                self.screen = pygame.display.set_mode((width, height))
                
                # Initialize buttons after window size is set
                self.initialize_buttons()
                
                # Initialize audio with WAV-friendly settings
                pygame.mixer.quit()
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
                pygame.mixer.music.load(self.current_song["audio"])
                pygame.mixer.music.play()
                
            except Exception as e:
                print(f"Error loading video/audio: {e}")
                pygame.quit()
                sys.exit(1)
        
        # Control frame rate
        self.clock.tick(self.FPS)
        
        # Read video frame
        ret, frame = self.video.read()
        if ret:
            # Convert frame from BGR to RGB and create pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0, 1)
            self.video_frame = pygame.surfarray.make_surface(frame)
        else:
            # If video ends, restart it
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            pygame.mixer.music.play()  # Restart audio too
        
        # Increment frame count
        self.frame_count += 1
        
        # Increment tick
        self.tick += 1
        
        # Randomly light up buttons (adjust probability based on actual FPS)
        if self.FPS > 0:  # Prevent division by zero
            button_probability = 0.06 / self.FPS  # Adjust this ratio to control frequency
        else:
            button_probability = 0.001  # Default fallback value
        
        for i in range(len(self.button_states)):
            if not self.button_states[i] and random.random() < button_probability:
                self.button_states[i] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.video is not None:
                    self.video.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if self.video is not None:
                        self.video.release()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                mouse_pos = event.pos
                for i, button in enumerate(self.buttons):
                    # Calculate distance from mouse to button center
                    distance = ((mouse_pos[0] - button.centerx) ** 2 + 
                              (mouse_pos[1] - button.centery) ** 2) ** 0.5
                    # Check if click is within button radius
                    if distance <= BUTTON_SIZE // 2:
                        if self.button_states[i]:  # Only score if button is lit
                            self.score += 100
                            self.button_states[i] = False  # Turn off the button light

        # Draw video frame as background
        self.screen.fill(BLACK)
        if self.video_frame is not None:
            self.screen.blit(self.video_frame, (0, 0))
        
        # Draw buttons with lighting
        for i, button in enumerate(self.buttons):
            # Draw black trim (outer circle)
            pygame.draw.circle(self.screen, BLACK, button.center, BUTTON_SIZE // 2)
            # Draw inner button (slightly smaller)
            inner_color = YELLOW if self.button_states[i] else WHITE
            pygame.draw.circle(self.screen, inner_color, button.center, int(BUTTON_SIZE * 0.45))  # 90% of the size for inner circle
        
        # Draw score (top left, bigger font)
        score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        score_text = score_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Draw tick counter (top right)
        tick_font = pygame.font.Font(None, TICK_FONT_SIZE)
        tick_text = tick_font.render(f"Tick: {self.tick}", True, WHITE)
        tick_rect = tick_text.get_rect()
        tick_rect.topright = (self.screen.get_width() - 20, 20)
        self.screen.blit(tick_text, tick_rect)
        
        pygame.display.flip()

    def game_over_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.score = 0
                    self.state = GameState.SONG_SELECT
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        self.screen.fill(BLACK)
        text = pygame.font.Font(None, 48).render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, self.screen.get_height()//2))
        
        instructions = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(instructions, (self.screen.get_width()//2 - instructions.get_width()//2, self.screen.get_height()//2 + 50))
        
        pygame.display.flip()

    def __del__(self):
        if self.video is not None:
            self.video.release()

if __name__ == "__main__":
    game = RhythmGame()
    game.run()
