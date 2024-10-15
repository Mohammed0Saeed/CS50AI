import itertools
import random


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
        # if the length of the set is equal to the count, then they are all mines
        if len(self.cells) == self.count and len(self.cells) != 0:
            return self.cells
        # if not, return an empty set
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the count is equal to zero, then all of the cells are safe
        if self.count == 0 and len(self.cells) != 0:
            return self.cells
        # if not, return an empty set
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # remove the cell from the set
        if cell in self.cells:
            self.cells.remove(cell)
            # take a mine from the count given the fact that a mine has been removed
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # remove the cell from the set
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
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.safes.add(cell)

        # get all the cells around the cell and append them in cells 
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # add the moves as long as they are not played or known mines
                if (i, j) != cell and (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) not in self.safes and 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i, j))
                # if the cell is a known mine, decrease the count by one
                elif (i, j) in self.mines:
                    count -= 1
        
        # create a new sentence to include the new information in the set
        new_sentence = Sentence(cells, count)

        # add the new sentence in the knowledge
        self.knowledge.append(new_sentence)   

        # update the KB untill there is no possible change
        KB_changed = True
        while KB_changed:
            # issume that the KB has not been changed
            KB_changed = False

            # clear the KB from empty cells
            for sentence in self.knowledge.copy():
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)     
            
            # check if we can create new information from the available sentences in the KB
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    # ignore the sentence itself
                    if sentence1 is sentence2:
                        continue
                    
                    # if there are two identical sentences, remove one of them
                    if sentence1 == sentence2:
                        self.knowledge.remove(sentence2)
                    
                    # if sentence1 is a sub set of sentence2, create a new sub set add append it in the KB
                    if sentence1.cells.issubset(sentence2.cells):
                        new_sentence = Sentence(
                            sentence2.cells - sentence1.cells,
                            sentence2.count - sentence1.count
                        )
                        
                        # append the new informatoin in KB only if it is not in KB
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            KB_changed = True
                            
            # check if there is a clear sentence in KB about the mines and safe cells
            for sentence in self.knowledge.copy():
                # if the new sentence have safes, mark them safe
                if sentence.known_safes():
                    for cell in sentence.known_safes().copy():
                        self.mark_safe(cell)
                        # since we made an update, then KB has changed
                        KB_changed = True   

                if sentence.known_mines():
                    for cell in sentence.known_mines().copy():
                        self.mark_mine(cell)
                        # since we made an update, then KB has changed
                        KB_changed = True
            

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # iterate through all the safe cells
        for safe_cell in self.safes:
            # check if the cell isn't a move that has been made
            if safe_cell not in self.moves_made:
                print(f"safe move found {safe_cell}")
                return safe_cell
        # if there is no available safe moves, return none
        print("no safe move found")
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # add all the available moves on the board to a list
        moves = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moves.append((i, j))
    
        # check if there is available moves
        if len(moves) > 0:
            random_move = random.choice(moves)
            print(f"random move exists! {random_move}")
            return random_move

        
        # if not return none
        print("no random move found!")
        return None