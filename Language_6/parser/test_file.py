import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | N VP
S -> NP VP | NP VP CP | S Conj S
AP -> Adj | Adj AP | Adj N
NP -> N | Det N | NP PP | Det Adj NP | N PP | Det AP
PP -> P | P NP
VP -> V | V NP | V PP | VP Adv | Adv VP
CP -> Conj S | Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    string_list = nltk.tokenize.word_tokenize(sentence.lower())
    solution_list = []
    for word in string_list:
        if word.isalpha():
            solution_list.append(word)
    return solution_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    solution_list = []
    for branch in scan(tree):
        solution_list.append(branch)

    str_list = [str(tr)[3:-1] for tr in solution_list]
    str_list2 = []
    for term in str_list:
        if "NP" not in term:
            str_list2.append(term)

    kill_list = []
    for term1 in str_list2:
        for term2 in str_list2:
            if term2[1:-1] in term1 and term2 != term1:
                kill_list.append(term2)
    for kill in kill_list:
        str_list2.remove(kill)

    str_list2 = ["(NP" + i + ")" for i in str_list2]

    return_list = [tree.fromstring("(NP" + i + ")") for i in str_list2]

    return return_list


def scan(subtree, np_list=None):
    if np_list is None:
        np_list = []
    for i in range(len(subtree)):
        if len(subtree[i]) > 1:
            scan(subtree[i], np_list)
        if subtree[i].label() == "NP" and subtree[i] not in np_list:
            np_list.append(subtree[i])
    return np_list


if __name__ == "__main__":
    main()
