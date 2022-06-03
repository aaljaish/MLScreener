import re
import string

# Apply a first round of text cleaning techniques
def clean_text_step1(text):
    '''Make text lowercase, remove text in square or round brackets, keep punctuation for now, remove
    numbers, remove and remove words containing numbers.'''
    text = text.lower() # Make text lowercase
    text = re.sub('\[.*?\]', ' ', text) #remove text in square
    text = re.sub('\(.*?\)', ' ', text) #remove text in round brackets
    text = re.sub('\w*\d\w*', ' ', text) #remove words with numbers
    text = re.sub(" \d+", " ", text) #remove digits
    text = re.sub(r'\s+',' ', text) #remove new lines
    text =  re.sub(r"\b[a-zA-Z]\b", " ", text) #remove single letter words (e.g. "a", "k", etc.)
    text =  re.sub("  ", "", text) #replace double spaces with a single space
    text =  re.sub("randomis", "randomiz", text) #replace the word randomis with randomiz
    text =  re.sub("centre.?[- ]", "centre ", text) #replace the word centre with center
    return text
    
# Apply a second round of text cleaning techniques
def clean_text_step2(text):
    '''remove all text starting at the "conclusion" or "discussion" sections.'''
    sub1 =re.compile("(conclusions:.*|discussion:.*)stopnow", 
                    re.IGNORECASE)
    text =  re.sub(sub1,"", text) #remove discussion and conclusion test
    text =  re.sub("  ", "", text) #replace double spaces with a single space
    return text
    
def clean_text_step3(text):
    '''Remove punctuation.'''
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text) #remove punctuations
    text = re.sub(r'\W',' ', text) #remove one character that is not a word character
    return text