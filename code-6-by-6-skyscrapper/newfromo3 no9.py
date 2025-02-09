def solve_puzzle(clues):
    import itertools

    n = 6
    total_cols_bits = n * 6  # 36 bits in total

    # Helper: Count visible skyscrapers from a sequence.
    def visible(seq):
        cnt, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                cnt += 1
                max_seen = x
        return cnt

    # Precompute all 720 permutations (rows) of 1..6.
    all_rows = list(itertools.permutations(range(1, n+1)))
    # Compute for each row its (left, right) visible counts.
    row_vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # For grid row r (0 = top, 5 = bottom) the clues are:
    #   left clue = clues[23 - r]   (since left clues are given bottom-to–top)
    #   right clue = clues[6 + r]     (right clues are given top-to–bottom)
    # For each candidate row we also precompute a single integer candidate_mask.
    # For each column j, represent the number x as (1 << (x-1)) shifted left by (j*6) bits.
    def compute_mask(row):
        m = 0
        for j, num in enumerate(row):
            m |= (1 << (num - 1)) << (j * 6)
        return m

    # Build candidates for each grid row (keyed by row index 0..5).
    candidates = {}
    for r in range(n):
        left_clue  = clues[23 - r]
        right_clue = clues[6 + r]
        cand_list = []
        for row in all_rows:
            if left_clue and row_vis[row][0] != left_clue:
                continue
            if right_clue and row_vis[row][1] != right_clue:
                continue
            # Precompute candidate_mask for fast conflict-checking.
            cand_list.append((row, compute_mask(row)))
        candidates[r] = cand_list

    # Order grid rows by increasing candidate count (minimum–remaining–value heuristic).
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    # 'used' is an integer (36 bits) representing numbers already placed in each column.
    # For column j, the bits j*6 .. j*6+5 represent numbers used in that column.
    used = 0  # initially no column has any number (all bits 0)
    solution = None
    assignment = {}  # assignment[r] = chosen candidate row (tuple of ints) for grid row r

    # Forward checking: for every unassigned grid row, ensure there is at least one candidate that fits.
    def forward_check(pos, used):
        for i in range(pos, n):
            r = order[i]
            possible = False
            for cand, cand_mask in candidates[r]:
                if (used & cand_mask) == 0:
                    possible = True
                    break
            if not possible:
                return False
        return True

    # Backtracking search over grid rows in the order defined by 'order'.
    def backtrack(pos, used):
        nonlocal solution
        if solution is not None:
            return
        if pos == n:
            # All rows have been assigned; reconstruct grid in natural order (0 to 5).
            grid = [assignment[r] for r in range(n)]
            # Verify column clues.
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top_clue = clues[j]          # top clues: indices 0 to 5 (left-to-right)
                bottom_clue = clues[17 - j]    # bottom clues: indices 17 down to 12 (left-to-right)
                if top_clue and visible(col) != top_clue:
                    return
                if bottom_clue and visible(col[::-1]) != bottom_clue:
                    return
            solution = grid[:]
            return

        r = order[pos]
        for row_val, cand_mask in candidates[r]:
            # Conflict check: if any number in candidate row is already used in the corresponding column.
            if (used & cand_mask) != 0:
                continue

            new_used = used | cand_mask
            assignment[r] = row_val

            # Forward check: ensure that every remaining row can still be assigned.
            if forward_check(pos + 1, new_used):
                backtrack(pos + 1, new_used)
                if solution is not None:
                    return

            del assignment[r]

    backtrack(0, used)
    if solution is None:
        return None
    return tuple(tuple(row) for row in solution)


# --- Local testing (remove before submission) ---
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
