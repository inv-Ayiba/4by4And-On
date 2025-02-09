def solve_puzzle(clues):
    import itertools
    n = 6

    # --- Helper: Count visible skyscrapers (simulate the view)
    def visible(seq):
        cnt, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                cnt += 1
                max_seen = x
        return cnt

    # --- Precompute all 720 permutations of 1..6 and their visible counts.
    all_rows = list(itertools.permutations(range(1, n+1)))
    # For each row, record (left_visible, right_visible)
    row_vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # --- For each grid row (r = 0 is top, 5 is bottom) the clues are:
    #   left clue  = clues[23 - r]   (because left clues are given bottom-to–top)
    #   right clue = clues[6 + r]     (right clues are given top-to–bottom)
    #
    # For every candidate row we also precompute a “bit–version”:
    # each number x is represented as 1 << (x-1)
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
            bit_row = tuple(1 << (x - 1) for x in row)
            cand_list.append((row, bit_row))
        candidates[r] = cand_list

    # --- Order the grid rows by increasing candidate count.
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    # --- used[j] is an integer bitmask of numbers already used in column j.
    used = [0] * n
    solution = None
    assignment = {}  # assignment[r] = chosen candidate row (tuple of ints) for grid row r

    # --- Forward–checking: for every still–unassigned grid row, check that
    # at least one candidate is compatible with the current used numbers.
    def forward_check(pos, used):
        for i in range(pos, n):
            r = order[i]
            possible = False
            for cand, bit_row in candidates[r]:
                ok = True
                for j in range(n):
                    if used[j] & bit_row[j]:
                        ok = False
                        break
                if ok:
                    possible = True
                    break
            if not possible:
                return False
        return True

    # --- Backtracking search (over the grid rows in the order defined above).
    def backtrack(pos):
        nonlocal solution
        if solution is not None:
            return
        if pos == n:
            # All rows are assigned. Reconstruct the grid in natural order.
            grid = [assignment[r] for r in range(n)]
            # Now check the column clues.
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top = clues[j]         # top clue (indices 0..5)
                bottom = clues[17 - j]   # bottom clue (indices 17 down to 12)
                if top and visible(col) != top:
                    return
                if bottom and visible(col[::-1]) != bottom:
                    return
            solution = grid[:]
            return

        r = order[pos]
        for row_val, bit_row in candidates[r]:
            # Check if candidate fits with current column assignments.
            conflict = False
            for j in range(n):
                if used[j] & bit_row[j]:
                    conflict = True
                    break
            if conflict:
                continue

            # Place candidate: update each column’s used mask.
            for j in range(n):
                used[j] |= bit_row[j]
            assignment[r] = row_val

            # Forward–check: ensure that every remaining unassigned row has at least one candidate.
            if forward_check(pos + 1, used):
                backtrack(pos + 1)
                if solution is not None:
                    return

            # Backtrack: undo assignment.
            for j in range(n):
                used[j] ^= bit_row[j]
            del assignment[r]

    backtrack(0)
    if solution is None:
        return None
    return tuple(tuple(row) for row in solution)


# ---------------------------
# Local testing code (remove or comment out before submission)

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
