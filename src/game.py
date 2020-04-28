# coding: utf-8
# Circuit Breaker
# Created by James Raphael Tiovalen (2020)

# Check existence of libraries
import sys
import verifier
print("Beginning to check existence of libraries necessary to run the game properly...\n")
validated = verifier.check()
if not validated:
    print("You do not have the necessary libraries required for the game to be played. Apologies!\n")
    print("Quitting the game...")
    sys.exit(0)

# Import libraries
import random
import time
import curses
from curses.textpad import rectangle

# Import custom modules
import texts
import stages
from audio import playaudio, stopaudio

# Define global variables
scrwidth = -1
scrheight = -1
endgame = False
outcome = None

# Instantiate all stage variants and randomize order
pokemon = stages.Pokemon()

variants = [pokemon]
random.shuffle(variants)


# Define helper drawing functions
def draw_help_bar(window, message):
    window.addstr(scrheight - 1, 0,
                  message.ljust(scrwidth - 1), curses.A_REVERSE)


def draw_dialog_bg(window, top, left, height, width):
    window.attron(curses.A_REVERSE)
    for y in range(height):
        window.addstr(top + y, left, " " * width)
    rectangle(window, top, left, top + height - 1, left + width - 1)
    window.attroff(curses.A_REVERSE)


def draw_help_dialog(window):
    draw_dialog_bg(window, 2, 15, 20, 58)
    window.addstr(3, 16, "How to play the game".center(56))
    for i in range(0, len(texts.help_text)):
        window.addstr(5 + i, 16, texts.help_text[i], curses.A_REVERSE)
    window.addstr(20, 16, "Press any key to continue".center(56))


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


# Define main game screen
class MainScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def render(self):
        self.stdscr.clear()

        self.stdscr.addstr(0, 0,
                           "Circuit Breaker".ljust(scrwidth), curses.A_REVERSE)

        for i in range(len(texts.intro_texts)):
            self.stdscr.addstr(
                8 + i * 2, 0, texts.intro_texts[i].center(scrwidth))

        if curses.has_colors():
            attr = curses.color_pair(texts.RED) | curses.A_BOLD
        else:
            attr = 0
        for i in range(len(texts.title)):
            self.stdscr.addstr(2 + i, 0,
                               texts.title[i].center(scrwidth), attr)
        self.stdscr.addstr(36, 0,
                           "James Raphael Tiovalen".center(scrwidth))
        if curses.has_colors():
            attr = curses.color_pair(texts.BLUE)
        else:
            attr = 0
        self.stdscr.addstr(38, 0,
                           "Crafted using Python 3".center(scrwidth), attr)

        draw_help_bar(self.stdscr,
                      "[N]ew Game [H]elp [Q]uit")

        self.stdscr.refresh()

    def handle_key(self, key, alias):
        global endgame, outcome

        if key == ord('q') or key == 27:
            endgame = True
        elif key == ord('n'):
            try:
                if sys.platform == "win32":
                    stopaudio(alias)
            except Exception as e:
                pass

            playaudio("music/galeem_dharkon.mp3", block=False)

            # Add overall game sequence here
            for variant in variants:
                self.stdscr.erase()
                outcome = curses.wrapper(variant.main)
                if outcome == "LOSE":
                    break

            endgame = True
            self.stdscr.erase()
        elif key == ord('h'):
            draw_help_dialog(self.stdscr)
            self.stdscr.getch()
        else:
            curses.flash()  # This might cause seizures (accessibility consideration)


# Main curses game sequence
def main(stdscr):
    global scrheight, scrwidth, outcome
    scrheight, scrwidth = stdscr.getmaxyx()

    # Disable blinking cursor
    curses.curs_set(0)

    if (scrheight <= 40 or scrwidth <= 166):
        raise RuntimeError(
            "Sorry, but a terminal size of 166x40 or larger is required. Try resizing your terminal. Thank you!")

    main_screen = MainScreen(stdscr)
    if sys.platform == "win32":
        # Play audio asynchronously
        alias = playaudio("music/mesos.mp3", block=False)
    else:
        alias = None

    while not endgame:
        if (scrheight <= 40 or scrwidth <= 166):
            stdscr.erase()
            stdscr.addstr(
                0, 0, "Sorry, but a terminal size of 166x40 or larger is required. Try resizing your terminal. Thank you!")
            stdscr.refresh()
        else:
            main_screen.render()
        key = stdscr.getch()

        if key == curses.KEY_RESIZE:
            scrheight, scrwidth = stdscr.getmaxyx()
        else:
            main_screen.handle_key(key, alias)

    stdscr.erase()

    if outcome:

        if outcome == "WIN":
            print_center(stdscr, "Congratulations! You have won the game!")
        elif outcome == "LOSE":
            print_center(
                stdscr, "I'm sorry, but you have lost the game... Better luck next time.")

        time.sleep(5)

    print("Thank you for playing Circuit Breaker!")


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except RuntimeError as e:
        print(e)
