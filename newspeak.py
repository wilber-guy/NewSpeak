__author__ = "Gabe Wilberscheid"
__date__ = "January 4th, 2019"


import spacy
import textacy.extract
import textacy.keyterms
# https://chartbeat-labs.github.io/textacy/api_reference.html
from docx import Document
import textstat
# https://github.com/shivam5992/textstat
from nltk.corpus import wordnet
from gensim.models import KeyedVectors

"""

class NewSpeak():
    ''' NewSpeak is used to help understand complicated and tricky English '''

    def __init__(self, file_name="textfile.docx"):
        # Load in English Language
        self.__nlp = spacy.load('en')
        self.__doc = self.string_to_Spacy_doc(getText(file_name))


speak = NewSpeak()

semi_struct(speak)

"""


def string_to_Spacy_doc(text):
    # takes in string text and returns spacy Document

    # Load the  English NLP model
    nlp = spacy.load('en_core_web_lg')

    # Parse the document with spaCy
    doc = nlp(text)

    return doc


def getText(file_name):
    # Reads in a docx file and returns connected string
    doc = Document(file_name)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)

    return '\n'.join(fullText)





def get_readability(text):
    # takes in a string sentece and returns a int of rating
#    print(text, '\n')
    # returns a score 120 to negative infinity. Higher scores are easier to read
    rating = textstat.flesch_reading_ease(text)
#    print(rating, '\n')
    # returns grade level to comprehend the text, many different methods varify results
#    print(textstat.text_standard(text, float_output=False), '\n \n')
    return rating



def get_key_terms(doc):
    # Extracts the Spacy Doc and returns keywords in document
    keyterms = textacy.keyterms.textrank(doc, normalize='lemma', n_keyterms=10)
    return keyterms





def noun_chunk(doc):
    # Extract noun chunks that appear
    noun_chunks = textacy.extract.noun_chunks(doc, min_freq=3)

    # Convert noun chunks to lowercase strings
    noun_chunks = map(str, noun_chunks)
    noun_chunks = map(str.lower, noun_chunks)

    # Print out any nouns that are at least 2 words long
    for noun_chunk in set(noun_chunks):
        if len(noun_chunk.split(" ")) > 1:
            print(noun_chunk)




def get_synonym(word):
    # Use NLTK's WordNet
    # takes in a single string word and returns a list of synonyms
    # in this use a spacy.token is passed in and used the .text attribute
    synonyms = []
    for syn in wordnet.synsets(word.text):
        for lm in syn.lemmas():
                 synonyms.append(lm.name())

    print('original word: ', word, '\n\nsynonyms: ', synonyms, '\n')




def semi_struct(doc, keyword="people"):
    # Extract semi-structured statements
    # *requires* doc (textacy.Doc or spacy.Doc)
    # *requires* entity (str) – a noun or noun phrase of some sort
    #            (e.g. “President Obama”, “global warming”, “Python”)
    # *optional* cue (str) – verb lemma with which entity is associated (e.g. “talk about”, “have”, “write”)

    statements = textacy.extract.semistructured_statements(doc, keyword)

    for statement in statements:
        subject, verb, fact = statement
        print(f" - {fact}")



def get_similarities(ob1, ob2):
    # Determine semantic similarities of both words and sentences
    doc1 = nlp(ob1)
    doc2 = nlp(ob2)
    similarity = doc1.similarity(doc2)
    print(doc1.text ," : ", doc2.text, "simularity: ", similarity, '\n')

    # TODO: CREATE CHECKER TO ENSURE REPLACEABLE SENTENCE
    # https://radimrehurek.com/gensim/models/keyedvectors.html#what-can-i-do-with-word-vectors



def get_related(word):
    # returns Spacy related terms
    # Spacy token is passed in and used .text attribute to get string
    #word = nlp(token.text)
    #https://github.com/explosion/spaCy/issues/276
    # this link talks about using Brown cluster as well as searching word vec simularity

    print(word.vocab.strings)
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    for word in queries:
        print(word)
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:10]




'''
LSTM GENERATOR

https://radimrehurek.com/gensim/models/fasttext.html#usage-examples

'''










def test():
    # Uses testfile.docx and calls and displays every function call
    print("\n\n*** TEST STARTING ***\n\n")

    # Load the  English NLP model
    nlp = spacy.load('en')

    # Load vectors directly from the file Gensim and Google News 3.2 GB file
    model_filename = 'data/GoogleNews-vectors-negative300.bin'
    # need to use limit keyword to prevent memory overflow
    model = KeyedVectors.load_word2vec_format(model_filename, binary=True,  limit=10 ** 5)


    import gensim.downloader as api
    word_vectors = api.load("glove-wiki-gigaword-200")  # load pre-trained word-vectors from gensim-data


    from spacy.lang.en.stop_words import STOP_WORDS

    print("--"*20, "STOP WORDS\n\n", STOP_WORDS)
    print(type(STOP_WORDS))

    # Large String returns
    doc = nlp(getText("testfile.docx"))

    print("\n","--"*20, "\n\n\nKEY TERMS\n\n\n")
    key_terms = get_key_terms(doc)
    for term in key_terms:
        print(term)


    print("\n","--"*20, "\n\n\nNOUN CHUNK\n\n\n")
    noun_chunk(doc)

    print("\n","--"*20,"\n\n\nSemi_STRUCTURE\n\n\n")
    semi_struct(doc, "Donald Trump")


    print("--"*20,"\n\n\nREADABILITY\n\n\n")
    sentences = list(doc.sents)
    sentence_score = 0
    count = 0
    for sentence in sentences:
        readability = get_readability(str(sentence))
        sentence_score += readability
        count+=1
        print("Sentence: ", sentence, "\nReadbility: ", readability,"\n\n")
        # If the sentence is difficult to read, show syns
        if readability < 80:
            for word in sentence:
                # these words are Spacy Tokens
                # ------------------------------
                # https://spacy.io/api/token
                # ------------------------------
                # only print synonyms for non stop words and not puncuations
                if not word.is_stop and not word.is_punct and not word.is_space and not word.is_quote:

                    print("--"*20,"\n\n\nSpacy Token Attributes\n\n\n")
                    print(word.text, word.lemma_, word.pos_, word.tag_, word.dep_,
                          word.shape_, word.is_alpha, word.is_stop, '\n\n')

                    print("--"*20, "\n\n\nNLTK SYNONYM\n\n\n")
                    get_synonym(word)

                    # NEEDS TO BE FIXXED Does not let unregonized words pass
                    print("--"*20, "\n\n\nGENSIM VECTORS\n\n\n")
                    print( model.most_similar(word.text))
                    print("\n2nd Gensim Model: \n")
                    print(word_vectors.most_similar(word.lower_))

                    '''
                    BROKE AND UNABLE TO FIND SOLUTION

                    # NEEDS TO BE FIXXED
                    print("--"*20,"\n\n\nSpacy SYNONYM\n\n\n")
                    print ([w.lower_ for w in get_related(nlp.vocab[word.text])])
                    '''

    print("average sentence difficulty: ", sentence_score/count)











    # get similaries of all possible senteces
    print("--"*20,"\n\n\nSentence SIMILARITIES\n\n\n")
    for sent1 in sentences:
        for sent2 in sentences:

            get_similarities(str(sent1), str(sent2))


if __name__ == "__main__":
    test()
