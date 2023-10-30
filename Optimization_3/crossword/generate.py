import math
import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Parses through all variables in the problem
        for var in self.crossword.variables:
            delete_set = set()
            # Parses through the domain of each variable
            for word in self.domains[var]:
                # if the domain value doesn't fit the variable length
                # add it to the deletion set
                if var.length != len(word):
                    delete_set.add(word)
            # Remove all domain items scheduled for deletion
            # from the variable's domain
            for word in delete_set:
                self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        # Create a copy of the domain to freely edit
        x_domain_copy = self.domains[x].copy()
        # If there are no arcs there is no arc consistency to enforce
        if overlap is None:
            return revised
        else:
            # Check each word in the domain of x
            for x_word in self.domains[x]:
                count = 0
                # Compare each word in x's domain to every word in the
                # domain of y
                for y_word in self.domains[y]:
                    # If the two words do not have the same letter at the
                    # point of intersection that x and y share increment count
                    if x_word[overlap[0]] != y_word[overlap[1]]:
                        count += 1
                # If count equals the length of the domain of y then that means
                # that no value of y's domain works with that given
                # value for x. That means that it must be deleted from
                # the copy of x's domain
                if count == len(self.domains[y]):
                    x_domain_copy.remove(x_word)
            # x's domain is updated to reflect the enforcement of
            # arc consistency
            self.domains[x] = x_domain_copy
            # A revision has been made so the return value is
            # updated to reflect that
            revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # if arc = None then look at all arcs in the problem by adding them to
        # the list "queue"
        if arcs is None:
            queue = []
            for x in self.domains:
                for var in self.crossword.neighbors(x):
                    queue.append((x, var))
        else:
            queue = arcs

        # Go through every arc in queue
        for _ in range(len(queue)):
            (x, y) = queue.pop()
            # enforce arc consistency on each arc using revise
            if self.revise(x, y) is True:
                # if there are no values left in the domain of a variable
                # return False to indicate an impossible problem
                if len(self.domains[x]) == 0:
                    return False
                # If needed add new arc to the queue
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z, x))
        # if this point is reached it means the problem is solvable and solved
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checks if assignment contains all the variables in the problem
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Create a list of the variables already in assignment
        var_list = [n for n in self.crossword.variables
                    if n in assignment]
        # look at each variable in assignment
        for var in var_list:
            # Check if the word assigned to the variable is the correct length
            if var.length != len(assignment[var]):
                return False
            # Check if intersections are without conflict
            for n_var in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, n_var]
                if n_var in assignment and \
                        assignment[var][overlap[0]] != \
                        assignment[n_var][overlap[1]]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Create list of the variable's neighbors that have not
        # already been put into assignment
        neighbor_list = [n for n in self.crossword.neighbors(var)
                         if n not in assignment]
        solution_list = []
        # Parse through all words in the domain of the variable
        for word in self.domains[var]:
            count = 0
            # Loop through neighbors not already in assignment to
            # see if the word rules out words in neighboring domains
            for neighbor in neighbor_list:
                if word in self.domains[neighbor]:
                    count += 1
            # Add a nested list to the solution list with the word
            # and the count of variables ruled out by using that word
            solution_list.append([word, count])
        # sort the list by least-constraining values heuristic according to the
        # count value stored in the second element of each sub list
        solution_list.sort(key=lambda x: x[1])
        # Convert that nested loop back to a normal list by removing
        # the counts, as now that the words are in the correct order
        # the count value is no longer necessary
        solution_list = [elem[0] for elem in solution_list]
        return solution_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Create a list of all unassigned variables
        unassigned = [var for var in self.crossword.variables
                      if var not in assignment]

        # Create a solution list to compare to
        smallest_domain = [math.inf, None]
        # Check through every unassigned variable
        for var in unassigned:
            # If the variable has a smaller domain than the current smallest
            # domain, edit the solution list accordingly
            if len(self.domains[var]) < smallest_domain[0]:
                smallest_domain = [len(self.domains[var]), var]
            # If there is a tie choose the variable with the highest degree
            elif len(self.domains[var]) == smallest_domain[0]:
                if len(self.crossword.neighbors(var)) > \
                        len(self.crossword.neighbors(smallest_domain[1])):
                    smallest_domain = [len(self.domains[var]), var]

        # return only the second value of the solution list,
        # as it is the variable
        return smallest_domain[1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If the puzzle has been filled we're done and we can return an answer
        if self.assignment_complete(assignment):
            return assignment
        # pick an unassigned variable (intelligently)
        var = self.select_unassigned_variable(assignment)
        # look through values in the intelligently ordered domain
        for value in self.order_domain_values(var, assignment):
            # Make sure you don't use a word twice in a puzzle
            if value in assignment.values():
                continue
            # Create a copy of assignment and implement a new edit
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            # If the edit follows the rules of the problem recursively call
            # backtrack to make yet another edit passing in the edited copy
            # of assignment
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result:
                    return result
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
