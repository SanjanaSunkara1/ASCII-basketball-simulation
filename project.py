import math
import sys
import time
import os
from random import SystemRandom
import platform
import subprocess

try:
    import select
except ImportError:
    select = None  

# Fancy ASCII intro borders
print("+" + "=" * 46 + "+")
print("|{:^46}|".format("\U0001F3C0 ASCII Basketball Simulator \U0001F3C0"))
print("+" + "=" * 46 + "+")
print("|{:^46}|".format("Welcome to the ultimate ASCII court!"))
print("|{:^46}|".format("You have 5 shots to score points."))
print("|{:^46}|".format("Each shot needs an angle (1-90°)"))
print("|{:^46}|".format("and power (1-30)."))
print("|{:^46}|".format("You have 10 seconds to enter each value."))
print("|{:^46}|".format("Adjust your shot and aim carefully!"))
print("+" + "=" * 46 + "+")
print("|{:^46}|".format("Press Enter to start..."))
print("+" + "=" * 46 + "+")
input()

# Constants
COURT_WIDTH = 40
COURT_HEIGHT = 15
HOOP_Y = 5
BALL_CHAR = 'o'
HOOP_CHAR = '#'
EMPTY_CHAR = ' '
MAX_SHOTS = 5  
TIME_LIMIT = 10  
GRAVITY = 9.8

sys_random = SystemRandom()

# Hoop horizontal position 
HOOP_MIN_X = 20
HOOP_MAX_X = COURT_WIDTH - 4

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_court(hoop_x, ball_pos=None, score=0, shots_left=MAX_SHOTS, timer=TIME_LIMIT):
    court = []
    for y in range(COURT_HEIGHT):
        row = []
        for x in range(COURT_WIDTH):
            if y == HOOP_Y and (x == hoop_x or x == hoop_x + 1 or x == hoop_x + 2):
                row.append(HOOP_CHAR)
            elif ball_pos and int(round(ball_pos[0])) == x and int(round(ball_pos[1])) == y:
                row.append(BALL_CHAR)
            else:
                row.append(EMPTY_CHAR)
        court.append(row)

    border = '+' + '-' * COURT_WIDTH + '+'
    print(border)
    for y in range(COURT_HEIGHT):
        print('|' + ''.join(court[y]) + '|')
    print(border)

    print(f"Score: {score}  Shots Left: {shots_left}  Time per shot: {timer} sec")

def get_input_with_timeout(prompt, min_val, max_val, timeout):
    print(f"{prompt} ({min_val}-{max_val}): You have {timeout} seconds.")

    if select:
        start_time = time.time()
        input_str = ''
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input_str = sys.stdin.readline().strip()
                if input_str.isdigit():
                    val = int(input_str)
                    if min_val <= val <= max_val:
                        return val
                    else:
                        print(f"Input must be between {min_val} and {max_val}. Try again.")
                else:
                    print("Please enter a valid integer.")
            if time.time() - start_time > timeout:
                print("\nTime's up! No input received.")
                return None
            time.sleep(0.1)
    else:
        try:
            val = input()
            if val.isdigit():
                val_int = int(val)
                if min_val <= val_int <= max_val:
                    return val_int
            print(f"Invalid input. Input must be integer between {min_val} and {max_val}.")
        except:
            pass
        return None

def calculate_trajectory(angle_deg, power, time_step=0.1, max_time=5):
    angle_rad = math.radians(angle_deg)
    velocity_x = power * math.cos(angle_rad)
    velocity_y = power * math.sin(angle_rad)

    positions = []
    t = 0.0
    while t < max_time:
        x = velocity_x * t
        y = COURT_HEIGHT - 1 - (velocity_y * t - 0.5 * GRAVITY * t ** 2)
        if y > COURT_HEIGHT - 1:
            break
        if x > COURT_WIDTH - 1:
            break
        if y < 0:
            y = 0
        positions.append((x, y))
        t += time_step
    return positions

def check_score(positions, hoop_x):
    for pos in positions:
        x, y = int(round(pos[0])), int(round(pos[1]))
        if y == HOOP_Y and hoop_x <= x <= hoop_x + 2:
            return True
    return False

def shoot_ball(angle, power, hoop_x):
    positions = calculate_trajectory(angle, power)
    for pos in positions:
        clear_screen()
        draw_court(hoop_x, ball_pos=pos)
        time.sleep(0.07)
    clear_screen()
    draw_court(hoop_x)
    scored = check_score(positions, hoop_x)
    if scored:
        print("\U0001F389 Nice shot! You scored!")
    else:
        print("\u274C Missed! Better luck next time.")
    time.sleep(1.5)
    return scored

def play_sound(file_path):
    """Play a .wav file with cross-platform support."""
    system_name = platform.system()
    try:
        if system_name == "Windows":
            import winsound
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
        elif system_name == "Darwin":  # macOS
            subprocess.run(["afplay", file_path])
        else:  # Linux and others
            subprocess.run(["aplay", file_path])
    except Exception as e:
        print(f"Could not play sound: {e}")

def main():
    score = 0
    shots_left = MAX_SHOTS
    hoop_x = sys_random.randint(HOOP_MIN_X, HOOP_MAX_X)

    while shots_left > 0:
        clear_screen()
        draw_court(hoop_x, score=score, shots_left=shots_left, timer=TIME_LIMIT)
        angle = get_input_with_timeout("Enter shot angle", 1, 90, TIME_LIMIT)
        if angle is None:
            print("No angle entered in time or invalid input. Shot forfeited.")
            shots_left -= 1
            time.sleep(1)
            hoop_x = sys_random.randint(HOOP_MIN_X, HOOP_MAX_X)
            continue

        power = get_input_with_timeout("Enter shot power", 1, 30, TIME_LIMIT)
        if power is None:
            print("No power entered in time or invalid input. Shot forfeited.")
            shots_left -= 1
            time.sleep(1)
            hoop_x = sys_random.randint(HOOP_MIN_X, HOOP_MAX_X)
            continue

        scored = shoot_ball(angle, power, hoop_x)
        if scored:
            score += 1
        shots_left -= 1
        hoop_x = sys_random.randint(HOOP_MIN_X, HOOP_MAX_X)

    clear_screen()
    print("+" + "*" * 48 + "+")
    print("|{:^48}|".format("Game over!"))
    print("|{:^48}|".format(f"Your final score: {score} / {MAX_SHOTS}"))
    if score >= 3:
        print("|{:^48}|".format("\U0001F3C6 Great shooter!"))
        play_sound("cheer.wav")  # Make sure this file exists in the same folder!
    elif score >= 1:
        print("|{:^48}|".format("\U0001F44D Not bad, keep practicing!"))
    else:
        print("|{:^48}|".format("\U0001F605 Better luck next time!"))
    print("+" + "*" * 48 + "+")

    print("\nThanks for playing ASCII Basketball Shootout!")

if __name__ == "__main__":
    main()
