class Settings:
    # class to store settings for alien invasion
    def __init__(self):
        # initialize game settings
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 200
        self.bullet_height = 25
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 5

        # alien settings
        self.fleet_drop_speed = 5

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.1

        self.fleet_direction = 1  # 1 represents right, -1 represents left

        # scoring
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points) # if you want to see new point value







