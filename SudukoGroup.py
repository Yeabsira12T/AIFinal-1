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
def all_exist(self, arr): """ verify that there is at least one of each number present """ count = self.counting(arr)
missing = None
for num, c in enumerate(count[1:]): # exclude 0:
if c == 0:
return False, num+1 # no value or candidate exists
return True, missing
def check_done(self, num_boxes=SIZE) -> bool: """ check if each row/column/box only has unique elements""" # check rows
for i in range(self.n):
if not self.all_unique(self.get_row(i)):
return False
# check columns
for j in range(self.n):
if not self.all_unique(self.get_col(j)):
return False
# check boxes
for i0 in range(0, self.n, BOX_SIZE):
for j0 in range(0, self.n, BOX_SIZE):
if not self.all_unique(self.get_box(i0, j0)):
return False
return True
def get_candidates(self, start, end): " get candidates within two corners of a rectangle/column/row" candidates = set()
for i in range(start[0], end[0] + 1):
for j in range(start[1], end[1] + 1):
candidates = candidates | self.candidates[i][j]
return candidates
def check_possible(self): """ check if each row/column/box can have all unique elements""" # get rows
rows_set = []
for i in range(self.n):
inds = [(i, j) for j in range(self.n)]
rows_set.append(inds)
# get columns
cols_set = []
for j in range(self.n):
inds = [(i, j) for i in range(self.n)]
cols_set.append(inds)
# get diagonals
diags_set = []
if self.is_X_Sudoku:
diags_set.append(self.get_diagonals(0, 0))
diags_set.append(self.get_diagonals(0, self.n-1))
# check rows, columns and diagonals
type_ = ['row', 'column', 'diagonal']
for t, inds_set in enumerate([rows_set, cols_set]):
for k, inds in enumerate(inds_set):
arr = [self.grid[i][j] for i, j in inds]
if not self.no_duplicates(arr):
return False, 'Duplicate values in %s %d' % (type_[t], k)
arr += list(self.get_candidates(inds[0], inds[-1]))
possible, missing_num = self.all_exist(arr)
if not possible:
return False, '%d not placeable in %s %d' % (missing_num, type_[t], k)
# check boxes
for i0 in range(0, self.n, BOX_SIZE):
for j0 in range(0, self.n, BOX_SIZE):
arr = self.get_box(i0, j0)[:]
if not self.no_duplicates(arr):
return False, 'Duplicate values in box (%d, %d)' % (i0, j0)
for i in range(i0, i0 + BOX_SIZE):
for j in range(j0, j0 + BOX_SIZE):
arr += list(self.candidates[i][j])
possible, missing_num = self.all_exist(arr)
if not possible:
return False, '%d not placeable in box (%d, %d)' % (missing_num, i0, j0)
return True, ""
## ------- Candidate functions -------- ##
def place_and_erase(self, r: int, c: int, x: int, constraint_prop=True): """ remove x as a candidate in the grid in this row, column and box""" # place candidate x
self.grid[r][c] = x
self.candidates[r][c] = set()
# remove candidate x in neighbours
inds_neighbours = self.get_neighbour_inds(r, c, flatten=True)
erased = [(r, c)] # set of indices for constraint propogration
erased += self.erase([x], inds_neighbours, [])
# constraint propagation, through every index that was changed
while erased and constraint_prop:
i, j = erased.pop()
inds_neighbours = self.get_neighbour_inds(i, j, flatten=False)
for inds in inds_neighbours:
uniques = self.get_unique(inds, type=[1, 2, 3])
for inds_combo, combo in uniques:
# passing back the erased here doesn't seem to be very helpful
self.set_candidates(combo, inds_combo)
erased += self.erase(combo, inds, inds_combo)
inds_box = self.get_box_inds(i, j)
pointers = self.pointing_combos(inds_box)
for line, inds_pointer, num in pointers:
erased += self.erase(num, line, inds_pointer)
# keeps = self.box_line_reduction(inds_box) # doesn't work??
# for inds_keep, nums in keeps:
# self.erase(nums, inds_box, inds_keep)
def erase(self, nums, indices, keep): """ erase nums as candidates in indices, but not in keep""" erased = []
for i, j in indices:
edited = False
if ((i, j) in keep):
continue
for x in nums:
if (x in self.candidates[i][j]):
self.candidates[i][j].remove(x)
edited = True
if edited:
erased.append((i, j))
return erased
def set_candidates(self, nums, indices): """set candidates at indices. Remove all other candidates""" erased = []
for i, j in indices:
# beware triples where the whole triple is not in each box
old = self.candidates[i][j].intersection(nums)
if self.candidates[i][j] != old:
self.candidates[i][j] = old.copy()
erased.append((i, j)) # made changes here
return erased
def count_candidates(self, indices):
count = [[] for _ in range(self.n + 1)]
# get counts
for i, j in indices:
for num in self.candidates[i][j]:
count[num].append((i, j))
return count
def get_unique(self, indices, type=(0, 1, 2)):
# See documentation at https://www.sudokuwiki.org/Hidden_Candidates
groups = self.count_candidates(indices)
uniques = [] # final set of unique candidates to return
uniques_temp = {2: [], 3: []} # potential unique candidates
for num, group_inds in enumerate(groups):
c = len(group_inds)
if c == 1 and (1 in type):
uniques.append((group_inds, [num]))
if c == 2 and ((2 in type) or (3 in type)):
uniques_temp[2].append(num)
if c == 3 and (3 in type):
uniques_temp[3].append(num)
uniques_temp[3] += uniques_temp[2]
# check for matching combos (both hidden and naked)
for c in [2, 3]:
if c not in type:
continue
# make every possible combination
for combo in list(combinations(uniques_temp[c], c)):
group_inds = set(groups[combo[0]])
for k in range(1, c):
# if positions are shared, this will not change the length
group_inds = group_inds | set(groups[combo[k]])
if len(group_inds) == c:
# unique combo (pair or triple) found
uniques.append((list(group_inds), combo))
return uniques
