## IMPORT STATEMENTS ##
# Explanations:
# random - for randomly selecting items from the question list
# time   - for sleep/delays
# math   - for mathematical functions (floor)
# os     - for filesystem stuff (reading files)
import random
import time
import math
import os

## CLASSES ##


class Question:
    # The question class - store questions
    def __init__(self, t, a, b, c, d, r):
        self.title = t
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.correct = r


class Configuration:
    # The configuration class - stores setup and settings data
    def __init__(self, debug, diff, files):
        self.debug = debug
        self.difficulty = diff
        for item in files:
            self.files.append(item)
    debug = True
    difficulty = False
    files = []


class Responses:
    # The responses class - this data is hard-coded, so the init function is only to initialise it.
    def __init__(self, c, i):
        self.correct = c
        self.incorrect = i
    correct = []
    incorrect = []


## VARIABLES (global) ##

# Array to hold the question objects.
questions = []

# Configuration object with default values (in case none are loaded)
config = Configuration(True, False, [])

# Score of the user.
score = 0
# Previous score of the user (if they repeated).
oldscore = 0
# How many questions the user has attempted.
attempted = 0

# The user's age.
name = ""
# The constant minimum age to play the quiz.
minimumAge = 8

# The object that holds responses.
# It's not defined here, as it relies on the user's name.
responses = None

# If the current quiz session is a repeat.
repeat = False


## FUNCTIONS ##
# Helpers (remove whitespace, punctuation)

def rmPunctuationAndWhitespace(l):
    # Removes both punctuation and whitespace.
    return rmPunctuation(rmWhitespace(l))


def rmWhitespace(l):
    # Removes whitespace and newlines from array items.
    k = []
    for i in l:
        j = i.strip(" \n\r")
        k.append(j)
    return k


def rmPunctuation(l):
    # Removes punctuation from array items.
    k = []
    for i in l:
        j = i.strip(".,/!?~;:-")
        k.append(j)
    return k

# Basic I/O with error handling/catching


def i(t, p):
    # Input function - accepts input from user using a prompt (p argument) and checks it is in correct format (t argument).
    if t == "int":
        # Type: integer
        while True:
            try:
                return int(input(f"{p} "))
            except:
                print("Whoops, that's not a number! Please enter a whole number.")
    elif t == "flt":
        # Type: float
        while True:
            try:
                return float(input(f"{p} "))
            except:
                print("Whoops, that's not a float! Please enter a number.")
    elif t == "str":
        # Type: string
        while True:
            try:
                return str(input(f"{p} "))
            except:
                print("Whoops, that's not a string! Please enter some text.")
    elif t == "mlt":
        # Type: multiple-choice
        while True:
            try:
                s = str(input(f"{p} ")).upper()
                if ((s == "A") or (s == "B") or (s == "C") or (s == "D")):
                    return s
                else:
                    print(
                        "Whoops, that's not a valid option! Please choose A, B, C or D.")
            except:
                print("Whoops, that's not a string! Please enter some text.")
    elif t == "y/n":
        # Type: yes/no
        while True:
            try:
                s = str(input(f"{p} ")).upper()
                if (s[0] == "Y"):
                    return True
                elif (s[0] == "N"):
                    return False
                else:
                    print(
                        "Whoops, that's not a valid option! Please choose Yes or No.")
            except:
                print("Whoops, that's not a string! Please enter some text.")
    else:
        # Unknown data type: show error.
        e(f"invalid data type in i() function: {t}")


def q(q, n):
    # Question asking function - formats and prints question (q) passed to it, with the number (n)
    global score
    global attempted
    attempted = attempted + 1
    print(f"Question {n}:")
    print(f"{q.title}")
    print("")
    print(f"(A): {q.a}")
    print(f"(B): {q.b}")
    print(f"(C): {q.c}")
    print(f"(D): {q.d}")
    print("")
    entry = i("mlt", "Your answer:")
    if (entry == q.correct):
        # User chose correct answer.
        score = score + 1
        print(f"""
{random.choice(responses.correct)}
Your score is now {score} of {len(questions)}.""")
    else:
        print(f"{random.choice(responses.incorrect)}")
        # User chose incorrect answer.
        if (q.correct == "A"):
            print(f"The correct answer was (A) {q.a}.")
        elif (q.correct == "B"):
            print(f"The correct answer was (B) {q.b}.")
        elif (q.correct == "C"):
            print(f"The correct answer was (C) {q.c}.")
        elif (q.correct == "D"):
            print(f"The correct answer was (D) {q.d}.")
        print(f"Your score is now {score} of {len(questions)}.")
    print("")  # Newline to make it easier to read.


def e(o):
    # Error output - prints an error (o) to the screen with proper header.
    print(f"[ERR]: {o}")


def d(o):
    # Debug output - prints debug information (d) to the screen, but only if debug mode (in config) is enabled.
    if (config.debug):
        print(f"[DBG]: {o}")
    else:
        pass


def scanForFiles():
    # Scans the working directory for question files.
    # If Difficulty is enabled, it will only scan for files named "easy", "medium" or "hard".
    # Returns a list of files found.
    l = []
    # Get the current directory of the program (from Stack Overflow answer https://stackoverflow.com/questions/5137497/#5137509)
    path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(path):
        if filename.upper().endswith(".QDF"):
            d(f"found question file - name: {filename}")
            l.append(filename)
        else:
            continue
    d(f"qdf files found: {len(l)}")
    return l


def importQuestions(f):
    # Imports questions from files, formats them into objects and returns them to be stored.
    l = []
    try:
        if f[-3:].lower() != "qdf":
            e(f"could not read question file: {f} is not a QDF file (.qdf)")
            return False
        else:
            with open(f) as doc:
                lines = rmWhitespace(doc.readlines())
                d(f"questions in this file: {len(lines)}")
                if (lines[0] == "[QDF]\n"):
                    e(f"could not read question file: {f} is not a QDF file (missing header)")
                    return False
                else:
                    lines.pop(0)  # Remove the header - we don't need it
                    for line in lines:
                        split = line.split(";")
                        l.append(
                            Question(split[0], split[1], split[2],
                                     split[3], split[4], split[5])
                        )
                    return l
    except:
        e(f"error while reading question file {f}")
        return []


def importConfig(f):
    global config
    debug = True
    diff = False
    files = []
    try:
        if (f[-3:].lower() != "qcf"):
            e(f"could not read configuration file: {f} is not a QCF file (.qcf)")
            return False
        with open(f) as doc:
            lines = rmWhitespace(doc.readlines())
            if lines[0] != "[QCF]":
                e(f"could not read configuration file: {f} is not a QCF file (missing header)")
                return False
            lines.pop(0)
            for line in lines:
                split = line.split(":")
                key = split[0]
                value = split[1]
                if key == "debug":
                    if value == "yes":
                        debug = True
                    elif value == "no":
                        debug = False
                    else:
                        d(f"unknown value for configuration option {key}: {value} in file {f}")
                elif key == "difficulty":
                    if value == "yes":
                        diff = True
                    elif value == "no":
                        diff = False
                    else:
                        d(f"unknown value for configuration option {key}: {value} in file {f}")
                else:
                    d(f"unknown key for configuration: {key} in file {f}")
        config = Configuration(debug, diff, files)
        return True
    except:
        e(f"error while reading configuration file {f}")
        return False


## MAIN FUNCTIONS ##

def init():
    global config
    global questions
    print("Welcome to the quiz!")
    print("Setting up...")
    print("- Importing configuration...")
    if importConfig("config.qcf"):
        print("OK!")
        print("- Importing questions...")
    else:
        e("error while importing configuration data!")
        exit()
    # Scan the directory for possible files.
    config.files = scanForFiles()

    # If no question files were found, notify the user to add some more.
    if (config.files == []):
        e("no question files. please add some questions!")
        exit()

    # If the user has difficulty mode enabled, ask them to choose a difficulty.
    if (config.difficulty == True):
        print("You have difficulty mode enabled.")
        print("(to disable it, see the README.)")
        print("(A) Easy")
        print("(B) Medium")
        print("(C) Hard")
        print("(D) Never mind, import all")
        print("")
        diff = i("mlt", "Which difficulty would you like?")
        if (diff == "A"):
            questions = importQuestions("easy.qdf")
        elif (diff == "B"):
            questions = importQuestions("medium.qdf")
        elif (diff == "C"):
            questions = importQuestions("hard.qdf")
        elif (diff == "D"):
            for f in ["easy.qdf", "medium.qdf", "hard.qdf"]:
                questions = questions + importQuestions(f)

    # Otherwise, import all the files we found.
    else:
        for f in config.files:
            questions = questions + importQuestions(f)
    if (questions == []):
        # No questions were imported.
        e("no questions imported.")
        print("Oops... no questions were found or could be read. Please make sure you have files, and that they are named and formatted correctly.")
        input("Press [ENTER] to exit the program.")
        exit()
    print("Done!")


def agecheck():
    age = i("int", "What's your age?")
    if (age < minimumAge):
        print("Sorry, you're not old enough to take these quizzes.")
        print(f"Come back in {minimumAge-age} years!")
        return False
    else:
        print(f"Cool! You're old enough for these quizzes. Let's get started!")
        return True


init()

##### MAIN LOOP #####
print('''
  ___        _     _
 / _ \ _   _(_)___| |
| | | | | | | |_  | |
| |_| | |_| | |/ /|_|
 \__\_\\\__,_|_/___(_)
''')
if agecheck():  # Check their age (function returns true/false if they pass/fail the check)
    # Print welcome messages.
    print(f"""
Welcome to the quiz!

You've got {len(questions)} questions, from {len(config.files)} file(s) coming up!
Are you ready?
    """)
    # Get the user's name.
    name = i("str", "Before we begin, what's your name?")
    # "Ready" check
    input(f"Alright, {name}! Press [ENTER] to start the quiz!")

    # Responses list. Defined here because it needs the user's name.
    responses = Responses(["Excellent!", "Well done!", "Correct!", "Good job!", "Nice!",
                           f"Excellent, {name}!", f"Well done, {name}!", f"Correct, {name}!", f"Good job, {name}!", f"Nice, {name}!"],
                          ["Whoops, that's wrong.", "Oops, that's not correct.", "Hmm, not quite.", "Nope, that's not it.", f"Whoops, {name}, that's wrong.", f"Oops {name}, that's not correct.", f"Hmm, not quite.", f"Nope, that's not it.", f"Sorry, {name}... that's wrong."])

    # This is the start of the loop used if they choose to replay the quiz.
    while True:
        score = 0
        print("Shuffling the questions...")
        # Shuffle the question list (in place).
        random.shuffle(questions)
        print("Here we go...\n")

        # THE IMPORTANT BIT
        # Iterate over each question in the questions list, and pass it to the q (question-asker) function.
        for question in range(0, len(questions)):
            q(questions[question], question + 1)

        print("...aaand we're done!\n")
        # Print the user's score and percentage.
        print(
            f"Your score is {score} out of {len(questions)}! That's {math.floor((score/len(questions))*100)}%.")

        # Depending on the percentage the user gets, display a special message.
        percentage = math.floor((score/len(questions))*100)
        if (percentage == 0):
            # 0%
            print(f"Oh dear. Better luck next time, {name}.")
        elif (percentage > 1 and percentage <= 50):
            # 1% to 50%
            print(
                f"Great start! Keep working at it {name}, and soon you'll be getting 100% every time.")
        elif (percentage > 50 and percentage <= 75):
            # 51% to 75%
            print(f"Well done, {name}! That was great.")
        elif (percentage > 75 and percentage < 100):
            # 76% to 99%
            print(f"Excellent, {name}! That was spectacular.")
        elif (percentage == 100):
            # 100%
            print(f"Outstanding! Perfect score, {name}!")

        # If this isn't the user's first time playing the quiz, comment on the improvement/degradation of their skills.
        if (repeat == True):
            print(f"Your previous score from last game was {oldscore}.")
            if (oldscore > score):  # Worse this time
                print(
                    f"Hrm... that's a {math.floor(((oldscore/len(questions))/(score/len(questions)))*100)}% reduction.")
            elif (oldscore < score):  # Better this time
                print(
                    f"Well done - that's a {math.floor(((score/len(questions))/(oldscore/len(questions)))*100)}% improvement!")
            else:  # Same score
                print(
                    f"Maintianing the status quo... that's OK.")

        # Ask the user if they would like to play the quiz again.
        choice = i("y/n", f"{name}, do you want to play this quiz again?")
        if (choice == True):  # They want to play again
            print("OK!")
            oldscore = score
            repeat = True
        elif (choice == False):  # They do not want to play again
            print(f"""
    ---------- POST-GAME SUMMARY: ----------
    Attempted:           {attempted}
    Games:               {attempted/len(questions)}
    Correct:             {score}
    Accuracy:            {math.floor((score/attempted)*100)}%

    Questions:           {len(questions)}
    Files:               {len(config.files)}
    ----------------------------------------

    Thanks for playing, {name}!
    """)
            input("Press [ENTER] to exit the program. ")
            exit()
else:
    input("Press [ENTER] to exit the program. ")
    exit()
