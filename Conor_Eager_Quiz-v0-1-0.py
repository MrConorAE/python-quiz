## VARIABLES ##

questions = []

## CLASSES ##


class Question:
    # The question class, with default values.
    def __init__(self, t, a, b, c, d, r):
        self.title = t
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.correct = r


## FUNCTIONS ##
# Basic I/O with error handling/catching
def i(t):
    # Input function - accepts input from user and checks it is in correct format (t arg).
    if t == "int":
        while True:
            try:
                return int(input("<< "))
            except:
                o("Whoops, that's not a number! Please enter a whole number.")
    elif t == "flt":
        while True:
            try:
                return float(input("<< "))
            except:
                o("Whoops, that's not a float! Please enter a number.")
    elif t == "str":
        while True:
            try:
                return str(input("<< "))
            except:
                o("Whoops, that's not a string! Please enter some text.")
    else:
        e(f"invalid data type in i() function: {t}")


def o(o):
    # Output function - prints value passed to screen.
    print(o)


def e(o):
    # Error output - prints an error to the screen with proper header.
    print(f"[ERR]: {o}")


def d(o):
    # Debug output - prints debug information to the screen, but only if debug mode is enabled.
    if (config.debug):
        print(f"[DBG]: {o}")
    else:
        pass


def importQuestions(f):
    try:
        with open(f) as doc:
            lines = doc.readlines()
            for line in lines:
                split = line.split(";")
                questions.append(
                    Question(split[0], split[1], split[2],
                             split[3], split[4], split[5])
                )
    except:
        e("Could not read question file: invalid format.")
