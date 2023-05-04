""""

Group Assignment
	1 Aklil Zewde
	2 Helina Teshome
	3 Sena Adane
	4 Yeabsira Kelil
"""
from typing import List, Tuple, Set
from itertools import combinations

SIZE = 9
BOX_SIZE = 3


class Sudoku():
    def __init__(self, grid: List, is_X_Sudoku=False):
        n = len(grid)
        #assert len(grid[0]) == n, "Grid is not square. n_rows=%d, n_columns=%d" % (n, len(grid[0]))
        self.grid = grid
        self.n = n
        self.is_X_Sudoku = is_X_Sudoku
        # create a grid of viable candidates for each position
        candidates = []
        for i in range(n):
            row = []
            for j in range(n):
                if grid[i][j] == 0:
                    row.append(self.find_options(i, j))
                else:
                    row.append(set())
            candidates.append(row)
        self.candidates = candidates

    def __repr__(self) -> str:
        repr = ''
        for row in self.grid:
            repr += str(row) + '\n'
        return repr

    def get_row(self, r: int) -> List[int]:
        return self.grid[r]

    def get_col(self, c: int) -> List[int]:
        return [row[c] for row in self.grid]

    def get_box_inds(self, r: int, c: int) -> List[Tuple[int, int]]:
        inds_box = []
        i0 = (r // BOX_SIZE) * BOX_SIZE  # get first row index
        j0 = (c // BOX_SIZE) * BOX_SIZE  # get first column index
        for i in range(i0, i0 + BOX_SIZE):
            for j in range(j0, j0 + BOX_SIZE):
                inds_box.append((i, j))
        return inds_box

    def get_box(self, r: int, c: int) -> List[int]:
        box = []
        for i, j in self.get_box_inds(r, c):
            box.append(self.grid[i][j])
        return box
    def get_diagonals(self, r: int, c: int):
        diag = []
        if r==c:
            for i in range(self.n):
                diag.append(self.grid[i][i])
        if r==(self.n - c - 1):
            for i in range(self.n):
                    diag.append(self.grid[i][self.n - i - 1])
        return diag

    def get_neighbour_inds(self, r: int, c: int, flatten=False):
        inds_row = [(r, j) for j in range(self.n)]
        inds_col = [(i, c) for i in range(self.n)]
        inds_box = self.get_box_inds(r, c)
        inds_diag = []
        if self.is_X_Sudoku:
            if r == c:
                inds_diag.extend([(i, i) for i in range(self.n)])
            if r== (self.n - c - 1):
                inds_diag.extend([(i, self.n - i - 1) for i in range(self.n)])
        if flatten:
            return list(set(inds_row + inds_col + inds_box + inds_diag ))
        return [inds_row, inds_col, inds_box, inds_diag]

    def find_options(self, r: int, c: int) -> Set:
        nums = set(range(1, SIZE + 1))
        set_row = set(self.get_row(r))
        set_col = set(self.get_col(c))
        set_box = set(self.get_box(r, c))
        set_diagonals = set(self.get_diagonals(r, c)) if self.is_X_Sudoku else set()
        used = set_row | set_col | set_box | set_diagonals
        valid = nums.difference(used)
        return valid

    def counting(self, arr: List[int], m=SIZE) -> List[int]:
        """ count occurances in an array """
        count = [0] * (m + 1)
        for x in arr:
            count[x] += 1
        return count

    def all_unique(self, arr: List[int], m=SIZE) -> bool:
        """ verify that all numbers are used, and at most once """
        count = self.counting(arr, m=m)
        for c in count[1:]:  # ignore 0
            if c != 1:
                return False # not unique
        return True

    def no_duplicates(self, arr):
        """ verify that no number is used more than once """
        count = self.counting(arr)
        for c in count[1:]:  # exclude 0:
            if c > 1:
                return False  # more than 1 of value
        return True
