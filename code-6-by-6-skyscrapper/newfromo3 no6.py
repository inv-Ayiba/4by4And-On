def solve_puzzle(clues):
    import itertools

    n = 6

    # --- Helper: count visible skyscrapers in a sequence.
    def visible(seq):
        cnt, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                cnt += 1
                max_seen = x
        return cnt

    # --- Precompute all 720 rows and each row's (left, right) visible counts.
    all_rows = list(itertools.permutations(range(1, n+1)))
    row_vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # --- For each grid row (0 = top, 5 = bottom) determine candidate rows.
    # The clues for grid row r:
    #    left clue  = clues[23 - r]    (left clues are given bottom-to–top)
    #    right clue = clues[6 + r]      (right clues are given top-to–bottom)
    # For each candidate row, also precompute a tuple of bit masks:
    #    for a number x, the mask is 1 << (x-1)
    candidates = {}
    for r in range(n):
        left_clue  = clues[23 - r]
        right_clue = clues[6 + r]
        cand_list = []
        for row in all_rows:
            # Filter by row clues (ignore clue if zero)
            if left_clue and row_vis[row][0] != left_clue:
                continue
            if right_clue and row_vis[row][1] != right_clue:
                continue
            # Precompute the bit-mask version for each cell.
            bit_row = tuple(1 << (num - 1) for num in row)
            cand_list.append((row, bit_row))
        candidates[r] = cand_list

    # --- Determine the order in which to assign rows:
    # Use a minimum-remaining-values heuristic (rows with fewer candidates first).
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    # --- We'll track column usage with bit masks.
    # For column j, used[j] is an integer where a set bit means that number is used.
    used = [0] * n

    solution = None
    memo = set()

    def backtrack(pos, used, assignment):
        nonlocal solution
        if pos == n:
            # Reconstruct grid in natural order (row 0 at top, row 5 at bottom)
            grid = [assignment[r] for r in range(n)]
            # Now check column clues.
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top_clue    = clues[j]         # top clue for column j
                bottom_clue = clues[17 - j]      # bottom clue for column j
                if top_clue and visible(col) != top_clue:
                    return
                if bottom_clue and visible(col[::-1]) != bottom_clue:
                    return
            solution = grid[:]  # found a valid solution
            return

        state = (pos, tuple(used))
        if state in memo:
            return

        r = order[pos]
        for row_val, bit_row in candidates[r]:
            conflict = False
            for j in range(n):
                if used[j] & bit_row[j]:
                    conflict = True
                    break
            if conflict:
                continue

            # Save current state of used for backtracking.
            old_used = used[:]
            for j in range(n):
                used[j] |= bit_row[j]
            assignment[r] = row_val

            backtrack(pos + 1, used, assignment)
            if solution is not None:
                return

            # Backtrack.
            for j in range(n):
                used[j] = old_used[j]
            del assignment[r]

        memo.add(state)

    backtrack(0, used, {})

    if solution is None:
        return None
    return tuple(tuple(row) for row in solution)


# --- For local testing (you can remove this block before submission) ---
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
