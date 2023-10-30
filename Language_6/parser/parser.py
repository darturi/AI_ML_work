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
    # Tokenize a lowercase version of the string 'sentence'
    string_list = nltk.tokenize.word_tokenize(sentence.lower())
    solution_list = []
    # Iterate through each element of the sentence in its tokenized (and
    # therefore list) form
    for word in string_list:
        # If the element has letters add it to the solution list
        if word.islower():
            solution_list.append(word)
    return solution_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Use the scan() function to create a list of all branches headed
    # by an NP marker
    solution_list = []
    for branch in scan(tree):
        solution_list.append(branch)

    # Convert list of branches to strings for manipulation
    # Remove first NP from string representations of branches
    str_list = [str(tr)[3:-1] for tr in solution_list]
    str_list2 = []
    # Iterate through stripped string representations of branches
    for term in str_list:
        # If there are no NP's left in the string it means that the branch
        # does not contain any noun phrases as subtrees
        if "NP" not in term:
            str_list2.append(term)

    kill_list = []
    # Iterates through str_list2
    for term1 in str_list2:
        # In order to compare elements of the list to other
        # elements within the same list
        for term2 in str_list2:
            # Checks if term1 contains term2 without being the same term
            if term2[1:-1] in term1 and term2 != term1:
                kill_list.append(term2)
    # Remove all terms that were subcategories of other terms
    for kill in kill_list:
        str_list2.remove(kill)

    # Replace the NP tag and parenthesis that were removed earlier
    str_list2 = ["(NP" + i + ")" for i in str_list2]
    # Convert from string back to a list of trees
    return_list = [tree.fromstring("(NP" + i + ")") for i in str_list2]

    return return_list


def scan(subtree, np_list=None):
    # Avoid errors springing from having an empty list as the default
    # parameter value using the below if statement
    if np_list is None:
        np_list = []
    # iterate i times where i is the number of items directly below the subtree
    for i in range(len(subtree)):
        # If there is more than one item (the word from the sentence) below
        # a particular item below the subtree originally passed in recursively
        # call scan again this time passing in np_list to continue modifying it
        if len(subtree[i]) > 1:
            scan(subtree[i], np_list)
        # If the label is "NP" and it hasn't already been counted add the
        # subtree headed by the "NP" to np_list
        if subtree[i].label() == "NP" and subtree[i] not in np_list:
            np_list.append(subtree[i])
    return np_list


if __name__ == "__main__":
    main()
