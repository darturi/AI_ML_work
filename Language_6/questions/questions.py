import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Create a list of files to look through excluding any non .txt files
    data_list = [elem for elem in os.listdir(directory)
                 if elem[-4:] == '.txt']

    # Create an empty dictionary to add to and eventually return
    return_dict = {}
    # Loop through .txt files
    for filename in data_list:
        # Open each file, read it into a string and add it to a dictionary
        # with the file name as the key
        file_contents = open(os.path.join(directory, filename), "r")
        return_dict[filename] = file_contents.read()
    return return_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize a lowercase version of the document string
    string_list = nltk.tokenize.word_tokenize(document.lower())
    solution_list = []
    # Loop through tokenized document
    for word in string_list:
        # If the item in the list is punctuation or a stopword do not
        # do anything with that value
        if word in string.punctuation or \
                word in nltk.corpus.stopwords.words("english"):
            continue
        # If the item in the list contains lowercase letters and therefore
        # has text add it to the solution list
        elif word.islower():
            solution_list.append(word)
    return solution_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Create a list of every word in the corpus
    all_words = []
    for i in documents.values():
        all_words += i
    # Create a new list like the one previously created but without any
    # duplicate words
    all_words2 = set(all_words)

    idf_dict = {}
    # Loop through all unique words in the corpus
    for word in all_words2:
        doc_count = 0
        # Loop through all the text of the documents
        for doc in documents.values():
            # If the unique word is in the text of the document
            # increment doc_count to reflect that
            if word in doc:
                doc_count += 1
        # Compute the idf and add it to the idf_dict using the word as a key
        idf_dict[word] = math.log(len(documents) / doc_count)
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # Create a dictionary with the names of files as keys and integers as vals
    ans_dict = {key: 0 for key in files}
    # Loop through keys of the files dict (the names of all the files
    # in the corpus)
    for file in files:
        # Loop through the words in the query
        for word in query:
            # If the word from the query can be found in the contents of the
            # specified file (specified by filename iteration)
            if word in files[file]:
                # Modify ans_dict to have the tf-idf value computed by
                # multiplying the idf value fetched from the dict (computed
                # earlier) and the instances of the query word in the file
                ans_dict[file] += files[file].count(word) * idfs[word]
    # Convert the dict to a list and sort according to tf-idf value
    ans2 = list(sorted(ans_dict.items(), key=lambda item: item[1]))

    # Return the specified number (n) of files with the greatest if-idf values
    return [i[0] for i in ans2[-n:]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    """
    Compute IDF values for each sentence
    """
    ans_dict = {}
    # Loop through sentences (the keys in the sentences dict)
    for sentence in sentences.keys():
        terms_calculated = []
        # Loop through terms in the query
        for term in query:
            # Loop through each word in the tokenized version of the sentence
            # (Accessed as the value of the sentence in question)
            for word in sentences[sentence]:
                # If the word in the sentence is the same as the term in the
                # query update ans_dict with the addition of that word's
                # idf value to reflect that.
                if word == term and word not in terms_calculated:
                    terms_calculated.append(word)
                    if sentence not in ans_dict:
                        ans_dict[sentence] = idfs[word]
                    else:
                        ans_dict[sentence] += idfs[word]

    """
    Compute term density values for each sentence
    """
    # Loop through the keys of ans_dict (sentences)
    for key in ans_dict:
        dense_count = 0
        # tokenize the sentence to split it up
        split_sentence = nltk.tokenize.word_tokenize(key.lower())
        # Iterate through the words in query
        for word in query:
            # Increment dense count as a measure of how many times
            # query terms appear in each given sentence
            dense_count += split_sentence.count(word)
        # Compute term density given the number of words in the sentence and
        # the count of the instances of the query words and update ans_dict
        # so that the value for a given sentence is a list of its idf
        # value and its term density value
        ans_dict[key] = [ans_dict[key], dense_count / len(key.split())]

    """
    Sort sentences according to idf values with term density as a tiebreaker
    """
    # Turn ans_dict into a list of lists where each sublist is made up of:
    # [the sentence, the idf value, the term density value]
    ans_dict = [[key, ans_dict[key][0], ans_dict[key][1]] for key in ans_dict]
    # Sort by idf value with term density as a tiebreaker
    ans_dict.sort(key=lambda x: (x[1], x[2]))
    # Return the specified number (n) of best fitting sentences
    return [ans_dict[i][0]
            for i in range(len(ans_dict) - 1, len(ans_dict) - 1 - n, -1)]


if __name__ == "__main__":
    main()
