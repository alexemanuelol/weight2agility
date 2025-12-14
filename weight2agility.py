#!/usr/bin/env python3

import math
import json
import os
from pathlib import Path

CONFIG_FILE = Path('config.json')
MIN_LEVEL = 1
MAX_LEVEL = 99

def load_config() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)

    print('No config found. Lets set it up.\n')

    start_weight = float(input('Enter start weight (kg): '))
    goal_weight = float(input('Enter goal weight (kg): '))

    config = {
        'start_weight': start_weight,
        'goal_weight': goal_weight,
    }

    with CONFIG_FILE.open('w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

    print('\nConfig saved to config.json\n')
    return config

def get_xp_from_level(level: int) -> int:
    """ Get XP based on level """
    xp = 0
    for i in range(1, level):
        xp += math.floor(i + 300 * 2 ** (i / 7))
    return math.floor(xp / 4)

def get_xp_from_weight(current_weight: float, start_weight: float, goal_weight: float) -> int:
    """ Get XP based on weight"""
    current_weight = max(min(current_weight, start_weight), goal_weight)

    xp_level_99 = get_xp_from_level(MAX_LEVEL)
    progress = (start_weight - current_weight) / (start_weight - goal_weight)

    return math.floor(progress * xp_level_99)

def agility_level_from_xp(total_xp: int) -> int:
    """ Get agility level based on xp """
    for level in range(MIN_LEVEL, MAX_LEVEL + 1):
        if total_xp < get_xp_from_level(level):
            return level - 1
    return MAX_LEVEL

def fmt(n: int) -> str:
    """ Format number with spaces for thousands grouping """
    return f'{n:,}'.replace(',', ' ')

def format_float(n: float) -> str:
    """ Remove decimal if n is .0 """
    if n.is_integer():
        return str(int(n))
    return str(n)

def main():
    config = load_config()

    start_weight = config['start_weight']
    goal_weight = config['goal_weight']

    print(f'Start Weight: {int(start_weight)} kg')
    print(f'Goal Weight:  {int(goal_weight)} kg\n')

    weight = float(input('Enter current weight (kg): '))

    total_xp = get_xp_from_weight(weight, start_weight, goal_weight)
    level = agility_level_from_xp(total_xp)

    print('\n=== Agility ===')
    print(f'Level:         {level}')
    print(f'XP:            {fmt(total_xp)}')
    print(f'XP to 99:      {fmt(get_xp_from_level(MAX_LEVEL) - total_xp)}')
    print(f'Weight left:   {format_float(weight - goal_weight)} kg')

    if os.name == 'nt':
        input('\nPress Enter to exit...')

main()
