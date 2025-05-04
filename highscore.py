import os

HIGHSCORE_FILE = "highscores.txt"


def read_highscores():
    """Read highscores from the file."""
    if not os.path.exists(HIGHSCORE_FILE):
        return []  # Return an empty list if the file doesn't exist

    with open(HIGHSCORE_FILE, "r") as file:
        highscores = [int(line.strip()) for line in file.readlines()]
    return highscores


def write_highscore(score):
    """Write a new highscore to the file."""
    highscores = read_highscores()
    highscores.append(score)
    highscores = sorted(highscores, reverse=True)[
        :10]

    with open(HIGHSCORE_FILE, "w") as file:
        for highscore in highscores:
            file.write(f"{highscore}\n")
