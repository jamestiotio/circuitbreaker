# coding: utf-8
# Store a pool of stages to choose randomly from for the main game
# Created by James Raphael Tiovalen (2020)

import secrets
import random
import json
import copy
from libdw import sm
import curses
from curses import textpad

# Store enemy data
with open('data.json') as f:
    data = json.load(f)


# First variant: Turn-based Pokemon-like TUI RPG
class Pokemon():

    options = ["ATTACK", "DEFEND", "HEAL"]
    enemy_options = ["ATTACK", "HEAL"]

    # Define state machine
    class BattleEngine(sm.SM):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Define player statistics
            self.health = 2000
            self.crit_rate = 0.05
            self.crit_mult = 3
            self.defense = 15
            self.def_mult = 3
            self.attack = 60
            self.heal = 25

            # Randomly choose an enemy for the encounter and define their statistics
            self.enemy = secrets.choice(data["characters"])
            for key, value in self.enemy.items():
                self.enemy_name = key
                self.enemy_stats = value

            self.enemy_hp = float(self.enemy_stats["hp"])
            self.enemy_crit_rate = float(self.enemy_stats["crit_rate"])
            self.enemy_crit_mult = float(self.enemy_stats["crit_mult"])
            self.enemy_attack_list = self.enemy_stats["attack_list"]
            self.enemy_quotes = self.enemy_stats["quotes"]
            self.enemy_graphics = self.enemy_stats["artwork"]
            self.enemy_heal = 20

            # Player starts first
            self.start_state = "PLAYER"

        # Input/output format: [Player's HP, Player's Def, Enemy's HP, Enemy's Quote, Enemy's Attack Name, Intended Action]
        def get_next_values(self, state, inp):
            output = inp

            if state == "PLAYER":
                next_state = "ENEMY"

                if inp[-1] == "ATTACK":
                    output[1] = self.defense
                    if random.random() >= 1 - self.crit_rate:
                        attack_val = self.attack * \
                            self.crit_mult + random.randint(2, 20)
                    else:
                        attack_val = self.attack + random.randint(6, 28)

                    output[2] -= attack_val

                elif inp[-1] == "DEFEND":
                    output[1] = self.defense * self.def_mult

                elif inp[-1] == "HEAL":
                    output[1] = self.defense
                    if self.health - output[0] >= self.heal:
                        output[0] += self.heal

            elif state == "ENEMY":
                next_state = "PLAYER"
                output[3] = secrets.choice(self.enemy_quotes)

                if inp[-1] == "ATTACK":
                    attack_choice = secrets.choice(self.enemy_attack_list)
                    for key, value in attack_choice.items():
                        output[4] = key
                        enemy_att_val = value

                    if random.random() >= 1 - self.enemy_crit_rate:
                        enemy_att_val *= self.enemy_crit_mult

                    attack_factor = enemy_att_val + \
                        random.randint(20, 70) - output[1]

                    if attack_factor > 0:
                        output[0] -= attack_factor

                elif inp[-1] == "HEAL":
                    if self.enemy_hp - output[2] >= self.enemy_heal:
                        output[2] += self.enemy_heal

            output[-1] = ""
            return (next_state, output)

    # Define helper printing functions
    def print_screen(self, stdscr, selected_row_idx, enemy_name, health, full_health, defense, enemy_hp, full_enemy_hp, quote, artwork, attack_name):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Draw title
        stdscr.addstr(0, 0, "Circuit Breaker".ljust(w), curses.A_REVERSE)

        # Draw menu
        textpad.rectangle(stdscr, h - 6, 3, h - 2, w - 3)
        for idx, row in enumerate(self.options):
            x = w//2 - len(row)//2 + ((idx - 1) * w // 4)
            y = h - 4
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        # Draw player's stats
        textpad.rectangle(stdscr, h - 13, 3, h - 7, 22)
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(h - 13, 3, "Player")
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(
            h - 11, 4, f"HP: {round(health)} / {round(full_health)}")
        stdscr.addstr(h - 9, 4, f"Def: {defense}")

        # Draw enemy's stats
        textpad.rectangle(stdscr, 5, 3, 11, 55)
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(5, 3, f"{enemy_name}")
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(
            7, 4, f"HP: {round(enemy_hp)} / {round(full_enemy_hp)}")
        stdscr.addstr(9, 4, f"Att: {attack_name}")

        # Draw enemy's quote
        textpad.rectangle(stdscr, 7, w - 72, 11, w - 3)
        stdscr.addstr(8, w - 71, f"{quote}")

        # Draw enemy's sprite
        for i in range(len(artwork)):
            stdscr.addstr(
                13 + i, 0, artwork[i].center(w))

        stdscr.refresh()

    # Define main looping draw function
    def main(self, stdscr):
        # Initial settings
        curses.curs_set(0)
        stdscr.nodelay(1)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        current_option = 0
        ending = False

        # Initialize encounter
        encounter = self.BattleEngine()
        encounter.start()

        # Define an identical set of statistics
        health = copy.deepcopy(encounter.health)
        defense = copy.deepcopy(encounter.defense)
        enemy_hp = copy.deepcopy(encounter.enemy_hp)
        enemy_name = copy.deepcopy(encounter.enemy_name)
        quote = ""
        attack_name = ""

        scrheight, scrwidth = stdscr.getmaxyx()

        # Create game boxes
        self.print_screen(stdscr, current_option, enemy_name, health, encounter.health,
                          defense, enemy_hp, encounter.enemy_hp, quote, encounter.enemy_graphics, attack_name)

        while not ending:
            if (scrheight <= 40 or scrwidth <= 166):
                stdscr.erase()
                stdscr.addstr(
                    0, 0, "Sorry, but a terminal size of 166x40 or larger is required. Try resizing your terminal. Thank you!")
                stdscr.refresh()
            else:
                # Blocking input
                key = stdscr.getch()

                if key == ord('q') or key == 27:
                    ending = True

                if key == curses.KEY_RESIZE:
                    scrheight, scrwidth = stdscr.getmaxyx()

                # Process menu action
                if key == curses.KEY_LEFT and current_option > 0:
                    current_option -= 1
                elif key == curses.KEY_RIGHT and current_option < len(self.options)-1:
                    current_option += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    # Player's turn
                    health, defense, enemy_hp, quote, attack_name, _ = encounter.step(
                        [health, defense, enemy_hp, "", "", self.options[current_option]])
                    # Enemy's turn
                    health, defense, enemy_hp, quote, attack_name, _ = encounter.step(
                        [health, defense, enemy_hp, "", "", secrets.choice(self.enemy_options)])

                self.print_screen(stdscr, current_option, enemy_name, health, encounter.health,
                                  defense, enemy_hp, encounter.enemy_hp, quote, encounter.enemy_graphics, attack_name)

                # Win condition
                if enemy_hp <= 0:
                    ending = True
                    return "WIN"

                # Lose condition
                elif health <= 0:
                    ending = True
                    return "LOSE"


# TODO: Future work would add more variants here
