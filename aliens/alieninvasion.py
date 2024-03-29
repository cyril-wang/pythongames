import sys
from time import sleep
import pygame

from aliensettings import Settings
# import settings from other file
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button, Scoreboard

class AlienInvasion:
    # overall class to manage game assets and behavior
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # initialize the game and create game resources
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # create instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # set background color
        self.bg_color = (230, 230, 230)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # creates group
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # make play button
        self.play_button = Button(self, "PLAY")

    def _create_fleet(self):
        # create alien, find number of aliens in a row
        # spacing between is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2*alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_aliens_x = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (3 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # create alien and place it in the row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed # lowers fleet by 1 row
        self.settings.fleet_direction *= -1 # changes direction

    def run_game(self):
        # start the main loop for the game
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos) # restricts only for the play button

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: # checks if overlap
            self.settings.initialize_dynamic_settings() # resets speed settings
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update position of bullets
        self.bullets.update() # updates everything in group

        # get rid of bullets that disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check for bullets that hit aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False,
                                                True)
        # creates a dictionary, returns key-value pair to it
        # Trues delete the objects that collided

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens: # empty group would return False
            # destroy existing bullets, create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        # when ship is hit
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # clear board to everything
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # look for collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        # redraw screen during each pass through loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        # draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make most recent drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

