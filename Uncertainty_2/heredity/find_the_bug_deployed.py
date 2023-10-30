people = ["Harry", "Lily", "James"]

probabilities = {
    person: {
        "gene": {
            2: 0,
            1: 0,
            0: 0
        },
        "trait": {
            True: 0,
            False: 0
        }
    }
    for person in people
}

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for sub_category in probabilities[person]:
            abnormal_sum = sum(list(probabilities[person][sub_category].values()))
            print(".values()", list(probabilities[person][sub_category].values()))
            print("IV", list(probabilities[person][sub_category]))
    return probabilities

normalize(probabilities)