import random


class GameLogic:
    def __init__(self):
        self._board = [[0] * 4 for _ in range(4)]
        self._score = 0
        self._won = False
        self._over = False

    def initialise_board(self):
        self._board = [[0] * 4 for _ in range(4)]
        self._score = 0
        self._won = False
        self._over = False
        self._place_random()
        self._place_random()

    def _place_random(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self._board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self._board[row][col] = 2 if random.random() < 0.9 else 4

    def handle_placement_if_not_game_over(self):
        if self._check_if_game_over():
            self._over = True
        elif self._check_if_game_won():
            self._won = True
        else:
            self._place_random()
        self._check_if_game_over()
        self._check_if_game_won()

    @staticmethod
    def shift_left(row, colum):
        for colum in range(colum, 3):
            row[colum] = row[colum + 1]
        row[3] = 0

    @staticmethod
    def keep_swifting_till_leading_zeros(row, colum):
        count = 0
        for c in range(colum, 4):
            if row[c] == 0:
                count += 1
            else:
                break
        for _ in range(count):
            GameLogic.shift_left(row, colum)

    def remove_spaces_left(self):
        for row in self._board:
            for colum in range(3):
                if row[colum] == 0:
                    self.keep_swifting_till_leading_zeros(row, colum)

    def merge_adjacent_equal_values_in_row_from_left(self):
        for row in self._board:
            for colum in range(3):
                if row[colum] == row[colum + 1]:
                    self._score += row[colum]
                    row[colum] *= 2
                    row[colum + 1] = 0

    def merge_adjacent_equal_values_in_row_from_right(self):
        for row in self._board:
            for colum in range(3, 0, -1):
                if row[colum] == row[colum - 1]:
                    self._score += row[colum]
                    row[colum] *= 2
                    row[colum - 1] = 0

    @staticmethod
    def shift_right(row, colum):
        for colum in range(colum, 0, -1):
            row[colum] = row[colum - 1]
        row[0] = 0

    @staticmethod
    def keep_swifting_till_trailing_zeros(row, colum):
        count = 0
        for c in range(colum, -1, -1):
            if row[c] == 0:
                count += 1
            else:
                break
        for _ in range(count):
            GameLogic.shift_right(row, colum)

    def remove_spaces_right(self):
        for row in self._board:
            for colum in range(3, 0, -1):
                if row[colum] == 0:
                    self.keep_swifting_till_trailing_zeros(row, colum)

    @staticmethod
    def has_left_leading_zeros(row):
        zero_index = -1
        non_zero_index = -1
        for i in range(4):
            if row[i] == 0:
                zero_index = i
                break

        for i in range(zero_index + 1, 4):
            if row[i] != 0:
                non_zero_index = i
                break

        return non_zero_index > zero_index

    @staticmethod
    def are_adjacent_equal_values_in_row(row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                return True
        return False

    def is_left_move_possible(self):
        for row in self._board:
            if self.has_left_leading_zeros(row):
                return True
            if self.are_adjacent_equal_values_in_row(row):
                return True
        return False

    @staticmethod
    def has_trailing_zeros(row):
        zero_index = -1
        non_zero_index = -1
        for i in range(3, -1, -1):
            if row[i] == 0:
                zero_index = i
                break

        for i in range(zero_index - 1, -1, -1):
            if row[i] != 0:
                non_zero_index = i
                break
        return non_zero_index != -1 and non_zero_index < zero_index

    def is_right_move_possible(self):
        for row in self._board:
            if self.has_trailing_zeros(row):
                return True
            if self.are_adjacent_equal_values_in_row(row):
                return True
        return False

    def has_zero_above(self, colum):
        zero_index = -1
        for i in range(3):
            if self._board[i][colum] == 0:
                zero_index = i
                break

        non_zero_index = -1
        for i in range(zero_index + 1, 4):
            if self._board[i][colum] != 0:
                non_zero_index = i
                break
        return non_zero_index > zero_index

    def has_equal_values_in_column(self, colum):
        for i in range(3):
            if self._board[i][colum] != 0 and self._board[i][colum] == self._board[i + 1][colum]:
                return True
        return False

    def is_up_move_possible(self):
        for i in range(4):
            if self.has_zero_above(i):
                return True
            if self.has_equal_values_in_column(i):
                return True
        return False

    def has_zero_below(self, colum):
        zero_index = -1
        for i in range(3, 0, -1):
            if self._board[i][colum] == 0:
                zero_index = i
                break

        non_zero_index = -1
        for i in range(zero_index - 1, -1, -1):
            if self._board[i][colum] != 0:
                non_zero_index = i
                break

        return non_zero_index != -1 and non_zero_index < zero_index

    def is_down_move_possible(self):
        for i in range(4):
            if self.has_zero_below(i):
                return True
            if self.has_equal_values_in_column(i):
                return True
        return False

    @staticmethod
    def shift_up(board, row, colum):
        for r in range(row, 3):
            board[r][colum] = board[r + 1][colum]
        board[3][colum] = 0

    @staticmethod
    def keep_swifting_till_leading_zeros_up(board, row, colum):
        count = 0
        for r in range(row, 4):
            if board[r][colum] == 0:
                count += 1
            else:
                break
        for _ in range(count):
            GameLogic.shift_up(board, row, colum)

    def remove_spaces_up(self):
        for i in range(4):
            for j in range(3):
                if self._board[j][i] == 0:
                    self.keep_swifting_till_leading_zeros_up(self._board, j, i)

    def merge_adjacent_equal_values_in_column_from_top(self):
        for i in range(4):
            for j in range(3):
                if self._board[j][i] == self._board[j + 1][i]:
                    self._score += self._board[j][i]
                    self._board[j][i] *= 2
                    self._board[j + 1][i] = 0

    @staticmethod
    def shift_down(board, row, colum):
        for r in range(row, 0, -1):
            board[r][colum] = board[r - 1][colum]
        board[0][colum] = 0

    @staticmethod
    def keep_swifting_till_trailing_zeros_down(board, row, colum):
        count = 0
        for r in range(row, -1, -1):
            if board[r][colum] == 0:
                count += 1
            else:
                break
        for _ in range(count):
            GameLogic.shift_down(board, row, colum)

    def remove_spaces_down(self):
        for i in range(4):
            for j in range(3, 0, -1):
                if self._board[j][i] == 0:
                    self.keep_swifting_till_trailing_zeros_down(self._board, j, i)

    def merge_adjacent_equal_values_in_column_down(self):
        for i in range(4):
            for j in range(3, 0, -1):
                if self._board[j][i] == self._board[j - 1][i]:
                    self._board[j][i] *= 2
                    self._board[j - 1][i] = 0

    # movement functions
    def only_move_left(self):
        self.remove_spaces_left()
        self.merge_adjacent_equal_values_in_row_from_left()
        self.remove_spaces_left()

    def capture_move_left(self):
        if not self.is_left_move_possible():
            return
        self.only_move_left()

        self.handle_placement_if_not_game_over()

    def only_move_right(self):
        self.remove_spaces_right()
        self.merge_adjacent_equal_values_in_row_from_right()
        self.remove_spaces_right()

    def capture_move_right(self):
        if not self.is_right_move_possible():
            return
        self.only_move_right()

        self.handle_placement_if_not_game_over()

    def only_move_up(self):
        if not self.is_up_move_possible():
            return
        self.remove_spaces_up()
        self.merge_adjacent_equal_values_in_column_from_top()
        self.remove_spaces_up()

    def capture_move_up(self):
        if not self.is_up_move_possible():
            return
        self.only_move_up()

        self.handle_placement_if_not_game_over()

    def only_move_down(self):
        self.remove_spaces_down()
        self.merge_adjacent_equal_values_in_column_down()
        self.remove_spaces_down()

    def capture_move_down(self):
        if not self.is_down_move_possible():
            return
        self.only_move_down()

        self.handle_placement_if_not_game_over()

    def get_score(self):
        return self._score

    def get_current_board(self):
        return self._board

    def get_won(self):
        return self._won

    def get_over(self):
        return self._over

    def _check_if_game_won(self):
        for row in self._board:
            if 2048 in row:
                self._won = True
                return True
        return False

    def _check_if_game_over(self):
        for row in self._board:
            if 0 in row:
                return False
        for i in range(4):
            for j in range(3):
                if self._board[j][i] == self._board[j + 1][i]:
                    return False
                elif self._board[i][j] == self._board[i][j + 1]:
                    return False
        self._over = True
        print("coming here or not")
        return True

    # functions to aid testing
    def set_board(self, board):
        self._board = board

