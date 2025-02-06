class Board:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.board = []
        self.battleships = []

    def create_board(self, size):
        if not isinstance(size, int) or size <= 0:
            raise ValueError(
                "Error: Size must be a positive integer.")
        if size > len(self.alphabet):
            raise ValueError(
                f"Error: Maximum board size is {len(self.alphabet)}.")
        self.board = [
            [0 for _ in range(size)]
            for _ in range(size)
        ]
        return f'Board created. Start: A1, End: {self.alphabet[size - 1]}{size}'

    def validate_placement(self, row_index, col_index, size, orientation):
        """
        Validates if the battleship can be placed at the given position without causing
        boundary overflows or collisions.
        """
        if orientation == "H" and (col_index + size > len(self.board)):
            raise ValueError("End outside of board for horizontal placement.")
        if orientation == "S" and (row_index + size > len(self.board)):
            raise ValueError("End outside of board for vertical placement.")
        if orientation == "D" and (row_index + size > len(self.board) or col_index + size > len(self.board)):
            raise ValueError("End outside of board for diagonal placement.")

        for i in range(size):
            if orientation == "H" and self.board[row_index][col_index + i] != 0:
                raise ValueError("Position already occupied in horizontal placement.")
            if orientation == "S" and self.board[row_index + i][col_index] != 0:
                raise ValueError("Position already occupied in vertical placement.")
            if orientation == "D" and self.board[row_index + i][col_index + i] != 0:
                raise ValueError("Position already occupied in diagonal placement.")

    def update_board_with_ship(self, row_index, col_index, size, orientation):
        """
        Updates the board with the battleship's position and returns the occupied coordinates.
        """
        battleship = []
        for i in range(size):
            if orientation == "H":
                self.board[row_index][col_index + i] = 1
                battleship.append(f"{self.alphabet[row_index]}{col_index + i + 1}")
            elif orientation == "S":
                self.board[row_index + i][col_index] = 1
                battleship.append(f"{self.alphabet[row_index + i]}{col_index + 1}")
            elif orientation == "D":
                self.board[row_index + i][col_index + i] = 1
                battleship.append(f"{self.alphabet[row_index + i]}{col_index + i + 1}")
        return battleship

    def place_battleship(self, start_position, size, orientation):
        """
        Public method to place a battleship on the board.
        """
        row = start_position[0]
        col = int(start_position[1:]) - 1  # Convert 1-based index to 0-based index
        row_index = self.alphabet.find(row)

        if row_index == -1 or col < 0 or row_index >= len(self.board) or col >= len(self.board):
            raise ValueError("Start is outside of board size.")
        if orientation not in ["H", "S", "D"]:
            raise ValueError("Invalid orientation. Use 'H', 'S', or 'D'.")

        # Validate and place
        self.validate_placement(row_index, col, size, orientation)
        battleship = self.update_board_with_ship(row_index, col, size, orientation)
        self.battleships.append(battleship)

        return f"Battleship placed successfully at {start_position} with size {size} and orientation {orientation}"

    def miss_or_hit(self, coordinate):
        """
        Determines whether the given coordinate is a hit or miss, and updates the board
        and battleship state accordingly.
        """
        row_index = self.alphabet.find(coordinate[0])
        col_index = int(coordinate[1:]) - 1  # Convert 1-based index to 0-based index

        if row_index == -1 or col_index < 0 or row_index >= len(self.board) or col_index >= len(self.board):
            raise ValueError("Coordinate is outside of board size.")

        if self.board[row_index][col_index] == 1:  # Hit
            self.board[row_index][col_index] = -1
            for battleship in self.battleships:
                if coordinate in battleship:
                    battleship.remove(coordinate)
                    if not battleship:  # If battleship is sunk
                        self.battleships.remove(battleship)
                        if not self.battleships:
                            return f"Hit and sink at {coordinate}. Congratulations, you have sunk all battleships. You win!"
                        return f"Hit and sink at {coordinate}"
                    return f"Hit at {coordinate}"
        elif self.board[row_index][col_index] == -1:  # Already hit
            return f"Already hit at {coordinate}"
        return f"Miss at {coordinate}"
