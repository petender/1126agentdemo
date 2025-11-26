#!/usr/bin/env python3
"""
Reflex Shooter Game - Terminal Edition
A terminal-based game that tests your shooting reflexes!
"""

import random
import time
import sys
import os
from threading import Thread, Event
import termios
import tty

# Game Constants
REFLEX_THRESHOLD = 0.6  # 0.6 seconds to win
GRID_WIDTH = 60
GRID_HEIGHT = 20

# ANSI Color codes
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_player_name():
    """Get player name input"""
    clear_screen()
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════╗")
    print("║      REFLEX SHOOTER GAME 🎯           ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    player_name = input(f"{Colors.YELLOW}Enter your name: {Colors.RESET}").strip()
    while not player_name:
        player_name = input(f"{Colors.RED}Please enter a valid name: {Colors.RESET}").strip()
    
    return player_name

def draw_game_screen(shooter_pos, target_pos, show_target=True):
    """Draw the game screen with shooter and target"""
    clear_screen()
    
    # Create grid
    grid = [[' ' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Place shooter at bottom middle
    sx, sy = shooter_pos
    if 0 <= sy < GRID_HEIGHT and 0 <= sx < GRID_WIDTH:
        grid[sy][sx] = '▲'
        if sx > 0:
            grid[sy][sx-1] = '◄'
        if sx < GRID_WIDTH - 1:
            grid[sy][sx+1] = '►'
    
    # Place target
    if show_target:
        tx, ty = target_pos
        if 0 <= ty < GRID_HEIGHT and 0 <= tx < GRID_WIDTH:
            grid[ty][tx] = '⊗'
    
    # Draw border and grid
    print(f"\n{Colors.CYAN}┌{'─' * GRID_WIDTH}┐{Colors.RESET}")
    for row in grid:
        line = ''.join(row)
        # Color the shooter green and target red
        line = line.replace('▲', f'{Colors.GREEN}▲{Colors.CYAN}')
        line = line.replace('◄', f'{Colors.GREEN}◄{Colors.CYAN}')
        line = line.replace('►', f'{Colors.GREEN}►{Colors.CYAN}')
        line = line.replace('⊗', f'{Colors.RED}⊗{Colors.CYAN}')
        print(f"{Colors.CYAN}│{Colors.RESET}{line}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}└{'─' * GRID_WIDTH}┘{Colors.RESET}\n")

def wait_for_spacebar():
    """Wait for spacebar press and return the timestamp"""
    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        # Set terminal to raw mode
        tty.setraw(fd)
        
        while True:
            char = sys.stdin.read(1)
            if char == ' ':
                return time.time()
            elif char == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def show_countdown():
    """Show a countdown before the game starts"""
    for i in range(3, 0, -1):
        clear_screen()
        print(f"\n\n{Colors.YELLOW}{Colors.BOLD}")
        print(f"          GET READY!")
        print(f"             {i}")
        print(f"{Colors.RESET}")
        time.sleep(1)

def play_game(player_name):
    """Main game loop"""
    # Shooter position (bottom middle)
    shooter_pos = (GRID_WIDTH // 2, GRID_HEIGHT - 2)
    
    # Random target position (avoid bottom area and edges)
    target_x = random.randint(5, GRID_WIDTH - 5)
    target_y = random.randint(2, GRID_HEIGHT - 6)
    target_pos = (target_x, target_y)
    
    # Show countdown
    show_countdown()
    
    # Show game screen with target
    draw_game_screen(shooter_pos, target_pos, show_target=True)
    print(f"{Colors.YELLOW}Press SPACEBAR to shoot!{Colors.RESET}")
    
    # Start timing
    target_appear_time = time.time()
    
    # Wait for spacebar
    shoot_time = wait_for_spacebar()
    reaction_time = shoot_time - target_appear_time
    
    # Check if player won
    won = reaction_time < REFLEX_THRESHOLD
    
    return reaction_time, won

def show_result(player_name, reaction_time, won):
    """Display the game result"""
    clear_screen()
    
    print(f"\n{Colors.BOLD}")
    print("╔════════════════════════════════════════╗")
    
    if won:
        print(f"║  {Colors.GREEN}         YOU WIN! 🎉              {Colors.RESET}{Colors.BOLD}║")
        print("╠════════════════════════════════════════╣")
        print(f"║  {Colors.YELLOW}Amazing reflexes, {player_name}!{' ' * (15 - len(player_name))}{Colors.RESET}{Colors.BOLD}║")
    else:
        print(f"║  {Colors.RED}    YOU ARE TOO SLOW 😔           {Colors.RESET}{Colors.BOLD}║")
        print("╠════════════════════════════════════════╣")
        print(f"║  {Colors.YELLOW}Better luck next time, {player_name}!{' ' * (10 - len(player_name))}{Colors.RESET}{Colors.BOLD}║")
    
    print("╠════════════════════════════════════════╣")
    print(f"║  {Colors.CYAN}Reaction Time: {reaction_time:.3f} seconds{' ' * (10 - len(f'{reaction_time:.3f}'))}{Colors.RESET}{Colors.BOLD}║")
    print(f"║  {Colors.CYAN}Target Time:   0.600 seconds           {Colors.RESET}{Colors.BOLD}║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    response = input(f"{Colors.WHITE}Play again? (y/n): {Colors.RESET}").strip().lower()
    return response == 'y'

def main():
    """Main function"""
    try:
        # Get player name
        player_name = get_player_name()
        
        playing = True
        while playing:
            reaction_time, won = play_game(player_name)
            playing = show_result(player_name, reaction_time, won)
        
        clear_screen()
        print(f"\n{Colors.CYAN}Thanks for playing, {player_name}! 👋{Colors.RESET}\n")
    
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.YELLOW}Game interrupted. Thanks for playing! 👋{Colors.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
