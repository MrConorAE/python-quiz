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
    title = "What is the answer to Life, the Universe and Everything?"
    a = "420"
    b = "69"
    c = "0"
    d = "42"
    correct = "d"


# FUNCTIONS ##

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
