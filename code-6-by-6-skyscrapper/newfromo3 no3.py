def solve_puzzle(clues):
    import itertools

    n = 6

    # Compute visible count for a sequence.
    def visible_count(seq):
        count, max_seen = 0, 0
        for num in seq:
            if num > max_seen:
                count += 1
                max_seen = num
        return count

    # Precompute all possible rows (permutations of 1..6) and store their (left, right) visible counts.
    all_rows = list(itertools.permutations(range(1, n+1)))
    vis = {}  # vis[row] = (left_visible, right_visible)
    for row in all_rows:
        vis[row] = (visible_count(row), visible_count(row[::-1]))
    
    # For each row index 0..5, the row clues come from:
    #   left clue: clues[23 - i]   (rows counted top-to-bottom)
    #   right clue: clues[6 + i]
    # (A value 0 means “don’t care”.)
    candidates = {}
    for i in range(n):
        left_clue  = clues[23 - i]
        right_clue = clues[6 + i]
        cand = []
        for row in all_rows:
            if left_clue and vis[row][0] != left_clue:
                continue
            if right_clue and vis[row][1] != right_clue:
                continue
            cand.append(row)
        candidates[i] = cand

    # Order the rows in the order of increasing candidate count (this is a common “minimum remaining value” heuristic).
    row_order = sorted(range(n), key=lambda i: len(candidates[i]))

    # We'll represent column assignments as bit masks.
    # For column j, a bit mask is an integer with bits 0..(n-1) representing numbers 1..n.
    # For example, if number x is already used in column j then bit (x-1) is 1.
    # Initially, no number is used: 0.
    init_cols = (0,) * n

    # Forward checking:
    # Given current columns state, check that every unassigned row has at least one candidate row that can be placed.
    def forward_check(pos, cols_masks):
        for i in range(pos, n):
            r = row_order[i]
            ok = False
            for cand in candidates[r]:
                conflict = False
                for j in range(n):
                    if cols_masks[j] & (1 << (cand[j]-1)):
                        conflict = True
                        break
                if not conflict:
                    ok = True
                    break
            if not ok:
                return False
        return True

    # Use memoization to avoid re–exploring the same state:
    # The state is (pos, cols_masks) where cols_masks is a tuple of n integers.
    memo = set()
    
    # The recursive search function.
    # pos: index into row_order (i.e. how many rows (in the chosen order) have been assigned).
    # cols_masks: current tuple of column bit masks.
    # assignment: dictionary mapping a row index (0..5) to a candidate row (a tuple of ints).
    def search(pos, cols_masks, assignment):
        # When pos == n, all rows have been assigned.
        if pos == n:
            # Build the grid in natural order (row 0 at top to row 5 at bottom)
            grid = [None] * n
            for r in range(n):
                grid[r] = assignment[r]
            # Now check the column clues.
            # For each column j:
            #   top clue is clues[j] (if nonzero, check visible_count on col top-to-bottom)
            #   bottom clue is clues[17 - j] (if nonzero, check visible_count on col bottom-to-top)
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top_clue = clues[j]
                bottom_clue = clues[17 - j]
                if top_clue and visible_count(col) != top_clue:
                    return None
                if bottom_clue and visible_count(col[::-1]) != bottom_clue:
                    return None
            # All clues satisfied.
            return grid

        state = (pos, cols_masks)
        if state in memo:
            return None
        # Get the next row to assign (r is the actual row index)
        r = row_order[pos]
        for cand in candidates[r]:
            # Check that cand can be placed (no conflict with columns)
            conflict = False
            new_cols = list(cols_masks)
            for j in range(n):
                bit = 1 << (cand[j]-1)
                if new_cols[j] & bit:
                    conflict = True
                    break
                new_cols[j] |= bit
            if conflict:
                continue
            new_cols = tuple(new_cols)
            # Forward check on the remaining unassigned rows.
            if not forward_check(pos+1, new_cols):
                continue
            assignment[r] = cand
            sol = search(pos+1, new_cols, assignment)
            if sol is not None:
                return sol
            del assignment[r]
        memo.add(state)
        return None

    sol = search(0, init_cols, {})
    if sol is None:
        return None
    return tuple(tuple(row) for row in sol)


# --- Sample tests (these are for your local testing) ---
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

    print("\nAll sample tests passed.")
