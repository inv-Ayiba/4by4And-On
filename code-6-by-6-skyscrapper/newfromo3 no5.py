def solve_puzzle(clues):
    import itertools
    n = 6

    # Helper: count visible skyscrapers in a sequence.
    def visible(seq):
        count, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                count += 1
                max_seen = x
        return count

    # Generate all 720 permutations of 1..6.
    all_rows = list(itertools.permutations(range(1, n+1)))
    # Precompute each row’s visible counts: (left_visible, right_visible)
    vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # For each grid row (0 = top, 5 = bottom) the clues are:
    #   left clue = clues[23 - r]   (since left clues are given bottom-to–top)
    #   right clue = clues[6 + r]     (since right clues are given top-to–bottom)
    # (A clue value of 0 means “don’t care”.)
    candidates = {}
    for r in range(n):
        left = clues[23 - r]
        right = clues[6 + r]
        cand = []
        for row in all_rows:
            if left and vis[row][0] != left:
                continue
            if right and vis[row][1] != right:
                continue
            cand.append(row)
        candidates[r] = cand

    # Use a minimum–remaining–value heuristic: fill grid rows in the order of fewest candidates.
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    solution = None       # will hold the final grid if found
    assignment = {}       # maps a grid row index to its chosen candidate (a tuple of 6 numbers)
    used_in_col = [set() for _ in range(n)]  # for each column, record which numbers are used

    def backtrack(pos):
        nonlocal solution
        if pos == n:
            # All rows have been assigned.
            # Reconstruct the grid in natural order (row 0 to 5).
            grid = [assignment[r] for r in range(n)]
            # Check each column’s clues:
            for j in range(n):
                col = [grid[r][j] for r in range(n)]
                top = clues[j]         # top clue (for column j)
                bottom = clues[17 - j]   # bottom clue (for column j)
                if top and visible(col) != top:
                    return
                if bottom and visible(col[::-1]) != bottom:
                    return
            solution = grid[:]  # save a copy of the solution
            return

        # Select the next row (r) to assign according to our ordering.
        r = order[pos]
        for cand in candidates[r]:
            # Check that placing cand in row r does not conflict with already placed numbers in each column.
            valid = True
            for j, num in enumerate(cand):
                if num in used_in_col[j]:
                    valid = False
                    break
            if not valid:
                continue
            # Place the candidate row.
            assignment[r] = cand
            for j, num in enumerate(cand):
                used_in_col[j].add(num)
            backtrack(pos + 1)
            if solution is not None:
                return
            # Backtrack: remove candidate from assignment and free the column numbers.
            for j, num in enumerate(cand):
                used_in_col[j].remove(num)
            del assignment[r]

    backtrack(0)
    if solution is None:
        return None
    # Return the solution as a tuple of 6 tuples (each row).
    return tuple(tuple(row) for row in solution)


# --------------------
# Example testing code (for local testing only):

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
