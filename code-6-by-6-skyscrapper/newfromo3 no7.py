def solve_puzzle(clues):
    import itertools
    n = 6

    # Helper: count visible skyscrapers in a sequence.
    def visible(seq):
        cnt, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                cnt += 1
                max_seen = x
        return cnt

    # Precompute all 720 rows (permutations of 1..6)
    all_rows = list(itertools.permutations(range(1, n+1)))
    # For each row, store its (left, right) visible counts.
    row_vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # For a grid row r (0 = top, 5 = bottom):
    #   left clue = clues[23 - r]   (left clues are given from top to bottom when read in reverse)
    #   right clue = clues[6 + r]     (right clues are given top-to-bottom)
    #
    # For each candidate row we also precompute a “bit–version” of the row:
    #   for a number x, we represent it as a bit mask: 1 << (x-1)
    candidates = {}
    for r in range(n):
        left = clues[23 - r]
        right = clues[6 + r]
        cand_list = []
        for row in all_rows:
            if left and row_vis[row][0] != left:
                continue
            if right and row_vis[row][1] != right:
                continue
            # Precompute bit representation for each cell in the row.
            bit_row = tuple(1 << (num - 1) for num in row)
            cand_list.append((row, bit_row))
        candidates[r] = cand_list

    # Order the grid rows by increasing candidate count (minimum–remaining–value heuristic).
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    # used[j] is an integer bit mask representing which numbers have been used in column j.
    used = [0] * n
    solution = None
    assignment = {}  # Maps grid row index (0..5) -> candidate row (as a tuple of ints)

    def backtrack(pos):
        nonlocal solution
        if pos == n:
            # We have assigned all grid rows; reconstruct the grid in natural order.
            grid = [assignment[r] for r in range(n)]
            # Verify column clues:
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top_clue = clues[j]         # Top side: indices 0..5 (left-to-right)
                bottom_clue = clues[17 - j]   # Bottom side: indices 17..12 (left-to-right)
                if top_clue and visible(col) != top_clue:
                    return
                if bottom_clue and visible(col[::-1]) != bottom_clue:
                    return
            # All clues are satisfied.
            solution = grid[:]
            return

        r = order[pos]
        for row_val, bit_row in candidates[r]:
            # Check that candidate row 'row_val' can be placed (no duplicate in any column).
            conflict = False
            for j in range(n):
                if used[j] & bit_row[j]:
                    conflict = True
                    break
            if conflict:
                continue

            # Place candidate: update used for each column.
            for j in range(n):
                used[j] |= bit_row[j]
            assignment[r] = row_val

            backtrack(pos + 1)
            if solution is not None:
                return

            # Backtrack: undo assignment and restore column masks.
            for j in range(n):
                # Since each column has unique numbers, we can remove the candidate’s bit with XOR.
                used[j] ^= bit_row[j]
            del assignment[r]

    backtrack(0)
    if solution is None:
        return None
    return tuple(tuple(row) for row in solution)


# --- Local Testing ---
if __name__ == '__main__':
    # Puzzle 1
    puzzle1_clues = (3,2,2,3,2,1, 1,2,3,3,2,2, 5,1,2,2,4,3, 3,2,1,2,2,4)
    expected1 = (
        (2, 1, 4, 3, 5, 6),
        (1, 6, 3, 2, 4, 5),
        (4, 3, 6, 5, 1, 2),
        (6, 5, 2, 1, 3, 4),
        (5, 4, 1, 6, 2, 3),
        (3, 2, 5, 4, 6, 1)
    )
    sol1 = solve_puzzle(puzzle1_clues)
    print("Puzzle 1 solution:")
    for row in sol1:
        print(row)
    assert sol1 == expected1

    # Puzzle 2
    puzzle2_clues = (0,0,0,2,2,0, 0,0,0,6,3,0, 0,4,0,0,0,0, 4,4,0,3,0,0)
    expected2 = (
        (5, 6, 1, 4, 3, 2), 
        (4, 1, 3, 2, 6, 5), 
        (2, 3, 6, 1, 5, 4), 
        (6, 5, 4, 3, 2, 1), 
        (1, 2, 5, 6, 4, 3), 
        (3, 4, 2, 5, 1, 6)
    )
    sol2 = solve_puzzle(puzzle2_clues)
    print("\nPuzzle 2 solution:")
    for row in sol2:
        print(row)
    assert sol2 == expected2

    # Puzzle 3
    puzzle3_clues = (0,3,0,5,3,4, 0,0,0,0,0,1, 0,3,0,3,2,3, 3,2,0,3,1,0)
    expected3 = (
        (5, 2, 6, 1, 4, 3), 
        (6, 4, 3, 2, 5, 1), 
        (3, 1, 5, 4, 6, 2), 
        (2, 6, 1, 5, 3, 4), 
        (4, 3, 2, 6, 1, 5), 
        (1, 5, 4, 3, 2, 6)
    )
    sol3 = solve_puzzle(puzzle3_clues)
    print("\nPuzzle 3 solution:")
    for row in sol3:
        print(row)
    assert sol3 == expected3

    print("\nAll sample tests passed!")
