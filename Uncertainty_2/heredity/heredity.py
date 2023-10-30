import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

"""
Represents the (in this case) 1% chance of a parent passing on the opposite
gene to the one they possess (a parent with two genes passing none, or
the inverse, a parent with no copies of the gene passing one)
"""
zero_one = PROBS["mutation"]

"""
Represents the (in this case) 99% chance of a parent passing on the
gene they possess (a parent with two genes passing one, or
the inverse, a parent with no copies of the gene passing none).
It is the 100% chance that the expected happens minus the chance
of mutation.
"""
nine_nine = 1 - PROBS["mutation"]

"""
A dictionary that uses the target number of genes for a given person,
and the number of genes possessed by each respective parent of that
individual as keys to navigate to a given value. That value is the
multiplicative representation of the chance of the target number of
genes for a given person given the genes of their parents, as represented
using zero_one and nine_nine
"""
gene_dict = {
        2: {  # 2 Genes
            2: {  # Mother has 2 Genes
                2: nine_nine * nine_nine,  # Father has 2 Genes
                1: nine_nine * 0.5,  # Father has 1 Gene
                0: zero_one * nine_nine  # Father has 0 Genes
            },
            1: {  # Mother has 1 Gene
                2: nine_nine * 0.5,  # Father has 2 Genes
                1: 0.5 * 0.5,  # Father has 1 Gene
                0: zero_one * 0.5  # Father has 0 Genes
            },
            0: {  # Mother has 0 Genes
                2: zero_one * nine_nine,  # Father has 2 Genes
                1: zero_one * 0.5,  # Father has 1 Gene
                0: zero_one * zero_one  # Father has 0 Genes
            }
        },
        1: {  # 1 Gene
            2: {  # Mother has 2 Genes
                2: (zero_one * nine_nine) * 2,  # Father has 2 Genes
                1: (zero_one * 0.5) + (nine_nine * 0.5),  # Father has 1 Gene
                0: (zero_one ** 2) + (nine_nine ** 2)  # Father has 0 Genes
            },
            1: {  # Mother has 1 Gene
                2: (zero_one * 0.5) + (nine_nine * 0.5),  # Father has 2 Genes
                1: (0.5 * 0.5) + (0.5 * 0.5),  # Father has 1 Gene
                0: (zero_one * 0.5) + (nine_nine * 0.5)  # Father has 0 Genes
            },
            0: {  # Mother has 0 Genes
                2: (zero_one ** 2) + (nine_nine ** 2),  # Father has 2 Genes
                1: (zero_one * 0.5) + (nine_nine * 0.5),  # Father has 1 Gene
                0: (zero_one * nine_nine) * 2  # Father has 0 Genes
            }
        },
        0: {  # 0 Genes
            2: {  # Mother has 2 Genes
                2: zero_one * zero_one,  # Father has 2 Genes
                1: zero_one * 0.5,  # Father has 1 Gene
                0: zero_one * nine_nine  # Father has 0 Genes
            },
            1: {  # Mother has 1 Gene
                2: zero_one * 0.5,  # Father has 2 Genes
                1: 0.5 * 0.5,  # Father has 1 Gene
                0: nine_nine * 0.5  # Father has 0 Genes
            },
            0: {  # Mother has 0 Genes
                2: zero_one * nine_nine,  # Father has 2 Genes
                1: nine_nine * 0.5,  # Father has 1 Gene
                0: nine_nine * nine_nine  # Father has 0 Genes
            }
        }
    }


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
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
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    joint_prob = float(1)
    for person in people:
        mother_name = people[person]["mother"]
        father_name = people[person]["father"]

        # If the target person has parents this set of comparisons represent
        # each parent's genes as integers to later be passed into functions
        # that are looking for that type of input
        if mother_name is not None and father_name is not None:
            if mother_name in one_gene:
                mother_num = 1
            elif mother_name in two_genes:
                mother_num = 2
            else:
                mother_num = 0

            if father_name in one_gene:
                father_num = 1
            elif father_name in two_genes:
                father_num = 2
            else:
                father_num = 0

        # Determine which aspect of the PROBS dict to access.
        # This allows us to skip comparisons before each function call
        if person in have_trait:
            tf = True
        else:
            tf = False

        # checks what gene count you are computing the probability for
        if person in one_gene:

            # calls the have_trait_check() function to multiply the probability
            # of a person with the specified gene count having or not having
            # the trait (indicated by the previously defined tf variable)
            joint_prob *= have_trait_check(1, tf)

            # If the person has no parents multiply the unconditional
            # probability that they have the specified number of genes
            # defined in the PROBS dictionary
            if mother_name is None and father_name is None:
                joint_prob *= PROBS["gene"][1]

            # If the person has parents use the number of genes the parents
            # have to call gene_calc() which will return the probability that
            # the specified gene_count is created by the parent's gene counts
            else:
                joint_prob *= gene_calc(1, mother_num, father_num)

        # Duplicate steps in lines 247 to 265 again for 2 and 0 genes
        # in the specified person
        elif person in two_genes:
            joint_prob *= have_trait_check(2, tf)
            if mother_name is None and father_name is None:
                joint_prob *= PROBS["gene"][2]
            else:
                joint_prob *= gene_calc(2, mother_num, father_num)
        else:
            joint_prob *= have_trait_check(0, tf)
            if mother_name is None and father_name is None:
                joint_prob *= PROBS["gene"][0]
            else:
                joint_prob *= gene_calc(0, mother_num, father_num)

    return joint_prob


def gene_calc(gene_num, mother, father):
    """
    Uses the number of genes of the target person, the number of genes
    possessed by the target's mother and father to navigate through
    the globally defined gene probability dictionary and to return the
    corresponding value
    """
    return gene_dict[gene_num][mother][father]


def have_trait_check(gene_num, trait):
    """
    Uses the number of genes of the target person, and whether or not
    the probability of the trait being present or not is being
    calculated to return the correct value from the globally
    defined gene probability dictionary
    """
    return PROBS["trait"][gene_num][trait]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_prefix = probabilities[person]["gene"]
        trait_prefix = probabilities[person]["trait"]

        if person in one_gene:
            gene_prefix[1] += p
        elif person in two_genes:
            gene_prefix[2] += p
        else:
            gene_prefix[0] += p

        if person in have_trait:
            trait_prefix[True] += p
        else:
            trait_prefix[False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for category in probabilities[person]:
            abnormal_sum = sum(list(probabilities[person][category].values()))
            if abnormal_sum != 1:
                factor = 1 / abnormal_sum
                for elem in probabilities[person][category]:
                    probabilities[person][category][elem] *= factor
    return probabilities


if __name__ == "__main__":
    main()
