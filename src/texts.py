# coding: utf-8
# Store text sequences
# Created by James Raphael Tiovalen (2020)

import time
import curses

WHITE = 0
RED = 1
GREEN = 2
BLUE = 3
YELLOW = 4

title = [
    "   ____  _                    _  _     ____                     _               ",
    "  / ___|(_) _ __  ___  _   _ (_)| |_  | __ )  _ __  ___   __ _ | | __ ___  _ __ ",
    " | |    | || '__|/ __|| | | || || __| |  _ \ | '__|/ _ \ / _` || |/ // _ \| '__|",
    " | |___ | || |  | (__ | |_| || || |_  | |_) || |  |  __/| (_| ||   <|  __/| |   ",
    "  \____||_||_|   \___| \__,_||_| \__| |____/ |_|   \___| \__,_||_|\_\\___||_|   "
]

intro_texts = [
    "The year is 2020.",
    "Due to the COVID-19 outbreak, Singapore has decided to implement what they call the Circuit Breaker period.",
    "Streets became emptier. Non-essential businesses closed down. Healthcare workers toiled day and night.",
    "Other workers engaged in Work-From-Home schemes. Mostly.",
    "Educational institutions like SUTD implemented Home-Based-Learning for all of its students.",
    "As instructors and students struggled together to cope with these new measures, this might be what the students felt...",
    "Particularly those students from class 19F07..."
]

help_text = [
    "Defeat the enemy by strategically choosing to attack",
    "them or heal the player.",
    "",
    "The enemy and the player will take turns, starting",
    "with the player.",
    "",
    "Press left and right arrow keys to select the player's",
    "option when engaging the enemy in an encounter.",
    "",
    "Press the Enter key to select the highlighted option."
]
