import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (len(self.cells) != 0) and self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            if self.count > 0:
                self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Marks the cell as a move that has been made
        self.moves_made.add(cell)

        # Notes that the cell that has been clicked is a safe cell
        self.mark_safe(cell)

        # Collects a list of empty cells adjacent to the target cell
        adj_cells = []
        for i in range((cell[0] - 1), (cell[0] + 2)):
            for j in range((cell[1] - 1), (cell[1] + 2)):
                if (i >= 0) and (i <= (self.width - 1)) and (j >= 0) and \
                        (j <= (self.height - 1)) and \
                        (i, j) not in self.moves_made:
                    adj_cells.append((i, j))

        # Adds the sentence created by the newest move made to knowledge
        if Sentence(adj_cells, count) not in self.knowledge:
            self.knowledge.append(Sentence(adj_cells, count))

        # Collects all new known mines and safes and stores them in two sets
        mine_list = set()
        safe_list = set()
        for sentence in self.knowledge:
            if len(sentence.known_mines()) > 0:
                for mine in sentence.known_mines():
                    if mine not in mine_list:
                        mine_list.add(mine)
            if len(sentence.known_safes()) > 0:
                for safe in sentence.known_safes():
                    if safe not in safe_list:
                        safe_list.add(safe)

        # Loops through the set of newly discovered safes and mines and
        # marks the cells accordingly
        for mine in mine_list:
            self.mark_mine(mine)
        for safe in safe_list:
            self.mark_safe(safe)

        # Checks for new inferences
        self.inferences()

    def inferences(self):
        """
        Loops through and compares each sentence in knowledge to every other.
        If the cells of a sentence are a subset of the cells of another
        sentence then a new sentence is created (and added to knowledge) by
        subtracting common cells and the count of the subset from the count
        of the superset (this is the third inference type)
        """
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells.issubset(sentence2.cells):
                    sentence3 = copy.deepcopy(sentence2)
                    for cell in sentence2.cells:
                        if cell in sentence1.cells:
                            sentence3.cells.remove(cell)
                    sentence3.count = sentence2.count - sentence1.count
                    if len(sentence3.cells) > 0 and \
                            sentence3 not in self.knowledge:
                        self.knowledge.append(sentence3)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_selection = [move for move in self.safes
                          if move not in self.moves_made]

        if len(safe_selection) > 0:
            return random.choice(safe_selection)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        random_selection = [(i, j) for i in range(self.width)
                            for j in range(self.height)
                            if (i, j) not in self.moves_made
                            and (i, j) not in self.mines]

        if len(random_selection) > 0:
            return random.choice(random_selection)
        return None
