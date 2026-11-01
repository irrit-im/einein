import json
import os
import secrets

from faker import Faker

""" General gameplay constants """
LEVELS = 10
MAX_MISTAKES = 3

""" Initialize random answer generator """
SEED_BITCOUNT = 32
Faker.seed(secrets.randbits(SEED_BITCOUNT))
FAKE = Faker()

""" Question building and question types """
QUESTION_TEMPLATE = "What {} am I thinking of? "
QUESTIONS = [
    ("number from 1 to 10", lambda: str(1 + secrets.randbelow(10))),
    ("color", FAKE.color_name),
    ("name", FAKE.first_name),
    ("word", FAKE.word)
]

""" Save file constant"""
FILE_DIR = os.path.abspath(os.path.dirname(__file__))
SAVE_FILE = os.path.join(FILE_DIR, ".psychic_save.json")
CONTINUE_QUESTION = "Would you like to continue {}'s saved game?"

def questions_in_level(level):
    """Calculates how many questions a level should have

    Args:
        level (int): a level number

    Returns:
        int: the number of questions the level should have
    """
    return 10 ** level

def ask_game_question():
    """ Asks the player a question for the game

    Returns:
        bool: True if the player answered correctly, False otherwise
    """
    guess_type, generator = secrets.choice(QUESTIONS)
    question = QUESTION_TEMPLATE.format(guess_type)
    correct = generator().lower()
    answer = input(question).strip().lower()
    if answer == correct:
        print("Correct!")
        return True
    else:
        print(f"Incorrect! The answer was {correct}")
        return False

def play_level(level):
    """Handles a level's gameplay

    Args:
        level (int): The level being played

    Returns:
        bool: True if the player beat the level, False otherwise
    """
    questions = questions_in_level(level)
    mistakes_left = MAX_MISTAKES
    print(f"Level {level}:\n\t{questions} questions\n\t{mistakes_left} mistakes left")
    for _ in range(questions_in_level(level)):
        if not ask_game_question():
            mistakes_left -= 1
            if mistakes_left == 0:
                return False
            print(f"You have {mistakes_left} mistakes left")    
    return True

def save_progress(name, level):
    """Saves a player's progress to the save file

    Args:
        name (str): the name of the player. Used for Identification.
        level (int): the level to which the player reached.
    """
    progress_dict = {
        "name": name,
        "level": level
    }
    with open(SAVE_FILE, 'w') as save_file:
        json.dump(progress_dict, save_file)

def check_save_file():
    """ Checks the existence and validity of a save file

    Returns:
        str (optional): the player's name if a valid save was found,
            or None otherwise
    """
    try:
        # check the save file is valid
        with open(SAVE_FILE, 'r') as save_file:
            progress_dict = json.load(save_file)
        level = progress_dict["level"]
        name = progress_dict["name"]
        
        # If a player finished the game, don't reload the save
        if level < LEVELS:
            return name 
    except FileNotFoundError:
        # first playthough - no saves
        pass
    except Exception:
        print("Bad save file!")
    
    return None

def get_saved_level():
    """ Gets the level from the save file.

    Returns:
        int: the level saved in the save file
    """
    with open(SAVE_FILE, 'r') as save_file:
        progress_dict = json.load(save_file)
    return progress_dict["level"]

def ask_binary_question(question):
    """ Asks a question with a binary (yes/no) answer.
    
    Answer is considered positive if it contains the letter 'y',
    and doesn't contain the letter 'n'.

    Args:
        question (str): The question being asked

    Returns:
        bool: the answer to the given question
    """
    print(question)
    answer = input("Reply with 'y' for yes and 'n' for no: ").lower()
    if 'y' in answer and 'n' not in answer:
        return True
    return False

""" The main game """
if __name__ == '__main__':    
    try:
        # handle loading saves
        name = check_save_file()
        if name is not None and ask_binary_question(CONTINUE_QUESTION.format(name)):
            level = get_saved_level()
        else:
            level = 0
            name = input("What is your name? ")
            
        # main game loop
        while level < LEVELS:
            save_progress(name, level)
            if play_level(level):
                print(f"\n[*] You completed level {level} ({questions_in_level(level)} questions) [*]\n")
                level += 1
            else:
                print("Level failed, try again!")
        
        print("You win!!!")
    except KeyboardInterrupt:
        print("Goodbye!")
