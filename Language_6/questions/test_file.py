import os
import nltk
import string
from nltk.corpus import stopwords
directory = "corpus"

data_list = [elem for elem in os.listdir(directory)
             if elem[-4:] == '.txt']
file_contents = open(os.path.join(directory, data_list[5]), "r")
document = file_contents.read()

string_list = nltk.tokenize.word_tokenize(document.lower())
solution_list = []
for word in string_list:
    if word in string.punctuation or word in stopwords.words("english"):
        continue
    elif word.islower():
        solution_list.append(word)
solution_list = solution_list[2:]
print(solution_list)
