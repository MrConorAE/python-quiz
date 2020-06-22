## IMPORT STATEMENTS ##
import random
import time

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
    name = ""
    age = 0


class Responses:
    # The responses class - this data is hard-coded, so no init function.
    correct = ["Excellent!", "Well done!", "Correct!", "Good job!", "Nice!"]
    incorrect = ["Whoops, that's wrong.", "Oops, that's not correct.",
                 "Hmm, not quite.", "Nope, that's not it."]


## VARIABLES (global) ##

questions = []

config = Configuration(True, False, [])

score = 0
oldscore = 0

responses = Responses()

repeat = False


## FUNCTIONS ##
# Helpers (remove whitespace, punctuation)

def rmPunctuationAndWhitespace(l):
    return rmPunctuation(rmWhitespace(l))


def rmWhitespace(l):
    k = []
    for i in l:
        j = i.strip(" \n\r")
        k.append(j)
    return k


def rmPunctuation(l):
    k = []
    for i in l:
        j = i.strip(".,/!?~;:-")
        k.append(j)
    return k

# Basic I/O with error handling/catching


def i(t, p):
    # Input function - accepts input from user and checks it is in correct format (t arg).
    if t == "int":
        while True:
            try:
                return int(input(f"{p} "))
            except:
                print("Whoops, that's not a number! Please enter a whole number.")
    elif t == "flt":
        while True:
            try:
                return float(input(f"{p} "))
            except:
                print("Whoops, that's not a float! Please enter a number.")
    elif t == "str":
        while True:
            try:
                return str(input(f"{p} "))
            except:
                print("Whoops, that's not a string! Please enter some text.")
    elif t == "mlt":
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
        e(f"invalid data type in i() function: {t}")


def q(q, n):
    global score
    # Question asking function - formats and prints question (q) passed to it, with the number (n)
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
        score = score + 1
        print(f"""
{random.choice(responses.correct)}
Your score is now {score}/{len(questions)}.""")
    else:
        print(f"""
{random.choice(responses.incorrect)}
Your score is now {score}/{len(questions)}.""")


def e(o):
    # Error output - prints an error (o) to the screen with proper header.
    print(f"[ERR]: {o}")


def d(o):
    # Debug output - prints debug information (d) to the screen, but only if debug mode is enabled.
    if (config.debug):
        print(f"[DBG]: {o}")
    else:
        pass


def importQuestions(f):
    # Imports questions from a listed file, formats them into objects and returns them to be stored.
    l = []
    try:
        if f[-3:].lower() != "qdf":
            e("could not read question file: not a QDF file (.qdf)")
            return False
        else:
            with open(f) as doc:
                lines = rmWhitespace(doc.readlines())
                if (lines[0] == "[QDF]\n"):
                    e("could not read question file: not a QDF file (missing header)")
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
        e("error while reading question file")
        return []


def importConfig(f):
    global config
    debug = True
    diff = False
    files = []
    try:
        if (f[-3:].lower() != "qcf"):
            e("could not read configuration file: not a QCF file (.qcf)")
            return False
        with open(f) as doc:
            lines = rmWhitespace(doc.readlines())
            if lines[0] != "[QCF]":
                e("could not read configuration file: not a QCF file (missing header)")
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
                        d(f"unknown value for configuration option {key}: {value}")
                elif key == "difficulty":
                    if value == "yes":
                        diff = True
                    elif value == "no":
                        diff = False
                    else:
                        d(f"unknown value for configuration option {key}: {value}")
                elif key == "files":
                    for f in value.split(","):
                        files.append(f)
                else:
                    d(f"unknown key for configuration: {key}")
        config = Configuration(debug, diff, files)
        return True
    except:
        e("error while reading configuration file")
        return False


## MAIN FUNCTIONS ##

def init():
    global config
    global questions
    print("welcome to the quiz!")
    print("setting up")
    print("- importing configuration...")
    if importConfig("config.qcf"):
        print("ok")
        print("- importing questions...")
    else:
        e("error while importing configuration data!")
        exit()
    if (config.files == []):
        e("no question files. please add some questions!")
        exit()
    if (config.difficulty == True):
        easy = importQuestions(config.files[0])
        medium = importQuestions(config.files[1])
        hard = importQuestions(config.files[2])
    else:
        for f in config.files:
            questions = questions + importQuestions(f)
    print("done!")


init()
print('''
  ___        _     _
 / _ \ _   _(_)___| |
| | | | | | | |_  | |
| |_| | |_| | |/ /|_|
 \__\_\\\__,_|_/___(_)
''')
print(f"""
Welcome to the quiz!

You've got {len(questions)} question, from {len(config.files)} files coming up!
Are you ready?
""")
input("Press [ENTER] to start!")
while True:
    print("Shuffling the questions...")
    random.shuffle(questions)
    print("Here we go...")
    for question in range(0, len(questions)):
        q(questions[question], question+1)
    print("...aaand we're done!")
    print(f"""
    Your score is {score} out of {len(questions)}! That's {(score/len(questions))*100}%.""")
    if (repeat == True):
        if (oldscore > score):
            print(f"""
            Your previous score was {oldscore}. Hrm... that's a {(oldscore/score)*100}% reduction.""")
        elif (score > oldscore):
            print(f"""
            Your previous score was {oldscore}. Well done - that's a {(score/oldscore)*100}% improvement!""")
    notchosen = True
    while notchosen:
        choice = i("y/n", "Do you want to play it again?")
        if (choice == True):  # They want to play again
            print("OK!")
            repeat = True
        if (choice == False):  # They do not want to play again
            print(f"""
Post-game summary:
""")
