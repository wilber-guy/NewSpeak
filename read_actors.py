from docx import Document # used for reading docx file types
import spacy
import newspeak
import re


file_name = input("What file to open? ")

filter_chars = ['(', ')', '“','”']

actor_dict = {'(': 'Narrator',
              'C': 'Child',
              'N': 'Nature',
              'A': 'Attendent',
              'B': 'Business Man',
              'E': 'Elderly Couple Man',
              'F': 'Elderly Couple Woman',
              'S': 'Scholarly Woman',
              'D': 'Family Man',
              'M': 'Family Woman',
              'K': 'Family Child',
              'T': 'Self Taught Man',
              'O': 'Outcast',
              'R': 'Rebel / Back of Train',
              }

def getText(file_name):
    doc = Document(file_name)
    fullText = []
    for para in doc.paragraphs:
        if para.text != '':
            fullText.append(para.text)

    # returns a list of paragraphs
    return fullText



def split_actors(list_of_para):
    # Takes in a list of character marked paragraphs
    # seperates the characters sentences and print their lines
    # along with readability for each character
    actors = {}
    avg_readability = {}
    char_count = {}
    questions = []

    # Load the  English NLP model
    nlp = spacy.load('en')


    for para in list_of_para:
        f_para = ''.join([c for c in para if c not in filter_chars])
        # remove character keys in text
        filter_para = re.sub('.:', '', f_para)

        # Sentences
        doc = nlp(para)
        sentences = [sent.string.strip() for sent in doc.sents]


        # Append All questions and actor to the list
        for sentence in sentences:
            if sentence[-1] == "?":
                questions.append((para[0] + ': ' + sentence))


        # Paragraph
        # read for first sentece of character
        if para[0] not in actors:
            # updates the actors dict to have a string of just their connect sentces
            # the translate removes the character keys and other symbols
            actors.update({para[0]: filter_para})

            readability = newspeak.get_readability(filter_para)
            avg_readability.update({para[0]: readability})

            char_count.update({para[0]: 1})

            print("\n", "%%"*20,'\n', filter_para, '\n\nREADABILITY: ', readability, '\n\n')

        # if character already in dict
        elif para[0] in actors:
            old_vals = actors.get(para[0])
            actors.update({para[0]: (old_vals + ' ' + filter_para)})

            readability = newspeak.get_readability(filter_para)
            old_readability = avg_readability.get(para[0])
            avg_readability.update({para[0]: (old_readability + readability)})

            char_num = char_count.get(para[0])
            char_count.update({para[0]: (char_num + 1)})

            print("\n", "%%"*20,'\n', filter_para, '\n\nREADABILITY: ', readability, '\n\n')



    for actor in actors.keys():
        print('\n\n\n', actor_dict.get(actor), '\n\n\n')

        print(actors.get(actor))

        print("\nActor Avg Readability: ", round(avg_readability.get(actor) / char_count.get(actor), 2) )


    print('\n\nKEYS: ', actors.keys())


    print('\n\nQUESTIONS: ')

    for question in questions:
        print(question)


    return actors



string = getText(file_name)

actors = split_actors(string)
