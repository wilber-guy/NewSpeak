from tkinter import *
import newspeak as ns



def retrieve_input(textBox, num):
    # reads in textBox as sting type
    inputValue=textBox.get("1.0","end-1c")
    # converts to Spacy Doc Type
    doc = ns.string_to_Spacy_doc(inputValue)


    if num == 0:
        display_readability(doc)

    if num == 1:
        display_keywords(doc)


def display_readability(doc):
    # takes in Spacy doc and prints to tkinter GUI the overage average readability
    sentences = list(doc.sents)
    sentence_score = 0
    count = 0

    total_sentences = len(sentences)
    print(total_sentences, " total_sentences")

    for sentence in sentences:
        readability = ns.get_readability(str(sentence))
        sentence_score += readability
        count+=1

        '''
        # update progress bar
        print("Running ", int((count/total_sentences)*100))
        # max score 100
        read_bar['value']= int((count/total_sentences)*100)
        '''

    avg_readability = sentence_score/count
    print("average sentence difficulty: ", avg_readability)

    # Change value of reability label in GUI
    readability_lbl.configure(text=str(round(avg_readability, 2)))

def display_keywords(doc):
    keywords = ns.get_key_terms(doc)
    word=""
    rating=""

    for words in keywords:
        word += (str(words[0])+'\n')
        rating += (str(round(words[1]*100, 4))+'\n')

    keywords_lbl.configure(text=word)
    rating_lbl.configure(text=rating)

# Creates nessicary Tkinter object and positions and makes calls to functions

# Set up window, title and size
root=Tk()
root.title("NewSpeak")
root.geometry('1200x900')

# Contents of tkinter window
# Welcome Header
header=Label(root, text='Welcome to NewSpeak: Enter Text', font=('Arial Bold', 18))
header.grid(column=0, row=0)


# Input text box
textBox=Text(root, height=35, width=90)
textBox.grid(column=0, row=1)

'''
# Not useful in this exact use case but runs

from tkinter.ttk import Progressbar
read_bar = Progressbar(root, length=100, mode='determinate')
read_bar.grid(column=0, row=2)
'''

# Readability button
readability_btn=Button(root, height=1, width=10, text="Readability",
                    command=lambda: retrieve_input(textBox, 0))
#command=lambda: retrieve_input() >>> just means do this when i press the button
readability_btn.grid(column=0, row=2)
# Readability Label
readability_lbl=Label(root)
readability_lbl.grid(column=0, row=3)


keywords_btn=Button(root, height=1, width=10, text="Keywords",
                    command=lambda: retrieve_input(textBox, 1))
keywords_btn.grid(column=1, row=2)

# Keyword Measage
keywords_lbl=Message(root)
keywords_lbl.grid(column=1, row=3)

rating_lbl=Message(root)
rating_lbl.grid(column=2, row=3)
#


root.mainloop()
