__author__ = "byteme8bit"

# File imports


# Module imports
import tkinter
from random import uniform, choice


def build_passphrase(total_chars=32, caps=True, specials=True):
    max_length = total_chars
    words = [line for line in open('passphrase_words.txt').readlines() if len(line) >= 7]
    passphrase = ''

    for pass_number in range(4):
        select = choice(words)
        words.remove(select)
        select = select.strip().lower()

        if caps:
            if specials:
                passphrase += insert_specials(random_capitals(select))
            else:
                passphrase += random_capitals(select)
        else:
            if specials:
                passphrase += insert_specials(select)
            else:
                passphrase += select

        if pass_number != 3:
            passphrase += ' '

        else:
            pass

    while len(passphrase) > max_length:
        diff = len(passphrase) - max_length

        for e in range(diff):
            index = choice(range(0, len(passphrase)))
            passphrase = passphrase[:index] + passphrase[index + 1:]

    while len(passphrase) < max_length:
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        diff = max_length - len(passphrase)

        for g in range(diff):
            index = choice(range(0, len(passphrase)))
            if caps:
                passphrase = passphrase[:index] + random_capitals(choice(alphabet)) + passphrase[index:]
            else:
                passphrase = passphrase[:index] + choice(alphabet) + passphrase[index:]

    return passphrase


def random_capitals(word):
    poss_capitals = [letter for letter in word]
    cap_word = ''

    for c in range(len(poss_capitals)):
        roll = uniform(0, 1)

        if roll > 0.72:
            poss_capitals[c] = poss_capitals[c].upper()
        else:
            poss_capitals[c] = poss_capitals[c].lower()

        cap_word += poss_capitals[c]

    return cap_word


def insert_specials(word):
    specials = '!@#$%^&*()-_=+`~/?.>,<;:\'"'

    for special_pass in range(len(word) // 2):  # Loops N times where N = half the total length of the word
        index = choice(range(0, len(word)))  # Selects random index of the word to be altered

        '''Splits the word up to the selected index, 
        inserts special character, 
        adds remainder of split word AFTER selected index'''
        word = word[:index] + choice(specials) + word[index:]

    return word  # Spits out altered word


# def run_program(total_runs, char_count=32, caps=True, specials=True):
#     if total_runs > 1:
#         for e in range(total_runs):
#             build_passphrase(total_chars=char_count, caps=caps, specials=specials)
#     else:
#         return build_passphrase(total_chars=char_count, caps=caps, specials=specials)


# ======================================== GUI START ========================================================
# MAIN WINDOW
mainWindow = tkinter.Tk()
mainWindow.title("PPG v 1.0")
mainWindow.geometry('250x250')

# HEADER
header = tkinter.Label(mainWindow, text="Passphrase Generator")  # A label at the top of the root window
header.grid(row=0, column=1, sticky='nsew')  # Sets dimensions
# quitBtn = tkinter.Button(mainWindow, text='Quit', command=mainWindow.quit).grid(row=0, column=2)

# WEIGHTS
mainWindow.rowconfigure(0, weight=10)  # Header
mainWindow.rowconfigure(1, weight=10)  # Options
mainWindow.rowconfigure(2, weight=10)  # Button
mainWindow.rowconfigure(3, weight=100)  # Results
mainWindow.rowconfigure(4, weight=100)  # Results
mainWindow.columnconfigure(0, weight=10)  # Border
mainWindow.columnconfigure(1, weight=100)  # Content
mainWindow.columnconfigure(2, weight=10)  # Border

# OPTIONS FRAME
optionFrame = tkinter.LabelFrame(mainWindow, text='Generator Variables')  # Allows a caption to be added with a border
optionFrame.grid(row=1, column=1, columnspan=2, sticky='nsew')  # Sets dimensions

# WEIGHTS
optionFrame.rowconfigure(0, weight=10)
optionFrame.rowconfigure(1, weight=10)
optionFrame.rowconfigure(2, weight=10)
optionFrame.rowconfigure(3, weight=10)
optionFrame.columnconfigure(0, weight=100)
optionFrame.columnconfigure(1, weight=10)
optionFrame.columnconfigure(2, weight=10)

# TOTAL LENGTH
total_lengthLabel = tkinter.Label(optionFrame, text='Total # of characters').grid(row=0, column=0, sticky='w')
total_length = tkinter.Entry(optionFrame)
total_length.grid(row=0, column=1, columnspan=2, sticky='ne')

# RANDOM CAPS
rcLabel = tkinter.Label(optionFrame, text='Use random caps?').grid(row=1, column=0, sticky='w')
# rcValue = tkinter.IntVar()
# rcValue.set(1)
rcValue = tkinter.BooleanVar(value=True)
rcYes = tkinter.Radiobutton(optionFrame, text='Yes', variable=rcValue, value=True).grid(row=1, column=1)
rcNo = tkinter.Radiobutton(optionFrame, text='No', variable=rcValue, value=False).grid(row=1, column=2)

# SPECIALS
specialsLabel = tkinter.Label(optionFrame, text='Use specials?').grid(row=2, column=0, sticky='w')
# scValue = tkinter.IntVar()
# scValue.set(1)
scValue = tkinter.BooleanVar(value=True)
specialsYes = tkinter.Radiobutton(optionFrame, text='Yes', variable=scValue, value=True).grid(row=2, column=1)
specialsNo = tkinter.Radiobutton(optionFrame, text='No', variable=scValue, value=False).grid(row=2, column=2)

# NUMBER OF PASSWORDS
numPwdLabel = tkinter.Label(optionFrame, text='How many passwords?').grid(row=3, column=0, sticky='w')
numPwd = tkinter.Entry(optionFrame)
numPwd.grid(row=3, column=1, columnspan=2, sticky='ne')

# RESULTS
# resultsBox = tkinter.Text(mainWindow)
# resultsBox.grid(row=3, rowspan=2, column=1, columnspan=2, sticky='nsew')


resultsList = tkinter.Listbox(mainWindow)
resultsList.grid(row=3, rowspan=2, column=1, columnspan=2, sticky='nsew')
listScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=resultsList.yview)
resultsList['yscrollcommand'] = listScroll.set


def run_program():
    total_runs = int(numPwd.get())
    char_count = int(total_length.get())
    resultsList.delete(0, 'end')

    if total_runs > 1:
        for e in range(total_runs):
            resultsList.insert(0, build_passphrase(total_chars=char_count,
                                                   caps=rcValue.get(),
                                                   specials=scValue.get()))
    else:
        resultsList.insert(0, build_passphrase(total_chars=char_count,
                                               caps=rcValue.get(),
                                               specials=scValue.get()))


# GENERATE BUTTON
generateButton = tkinter.Button(mainWindow, text='Generate', command=run_program)
generateButton.grid(row=2, column=1, columnspan=2, sticky='nsew')

mainWindow.mainloop()  # Executes the GUI code and loops until window is closed
