def solve_puzzle(clues):
    import itertools

    n = 6

    # Helper: count how many skyscrapers are visible in the sequence.
    def visible_count(seq):
        count, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                count += 1
                max_seen = x
        return count

    # Precompute all possible rows (permutations of 1..6)
    all_rows = list(itertools.permutations(range(1, n+1)))
    # Also precompute each row's (left, right) visible counts.
    vis = { row: (visible_count(row), visible_count(row[::-1])) for row in all_rows }
    
    # For a given row index i (with 0 = top, 5 = bottom),
    # the row's left clue is at clues[23 - i] (since left clues are given bottom-to–top)
    # and the row's right clue is at clues[6 + i] (since right clues are given top-to–bottom).
    row_candidates = {}
    for i in range(n):
        left_clue  = clues[23 - i]
        right_clue = clues[6 + i]
        row_candidates[i] = []
        for row in all_rows:
            if left_clue and vis[row][0] != left_clue:
                continue
            if right_clue and vis[row][1] != right_clue:
                continue
            row_candidates[i].append(row)
    
    # We'll fill the grid row by row in natural order (row 0 at top, row 5 at bottom).
    solution = None
    grid = [None] * n
    # For each column j, track which numbers have been used.
    columns = [set() for _ in range(n)]
    
    def search(row_index):
        nonlocal solution
        if row_index == n:
            # All rows have been assigned.
            # Now verify the column clues.
            for j in range(n):
                col = [grid[i][j] for i in range(n)]
                top_clue    = clues[j]         # Top clues: indices 0 to 5 (left-to–right)
                bottom_clue = clues[17 - j]      # Bottom clues: indices 17 down to 12 (left-to–right)
                if top_clue and visible_count(col) != top_clue:
                    return
                if bottom_clue and visible_count(col[::-1]) != bottom_clue:
                    return
            # All clues match.
            solution = [row for row in grid]
            return

        # Try each candidate row for this row.
        for candidate in row_candidates[row_index]:
            # Check column uniqueness:
            valid = True
            for j, num in enumerate(candidate):
                if num in columns[j]:
                    valid = False
                    break
            if not valid:
                continue
            # Place the candidate row.
            grid[row_index] = candidate
            for j, num in enumerate(candidate):
                columns[j].add(num)
            search(row_index + 1)
            if solution is not None:
                return
            # Backtrack:
            for j, num in enumerate(candidate):
                columns[j].remove(num)
            grid[row_index] = None

    search(0)
    if solution is None:
        return None
    return tuple(tuple(row) for row in solution)


# --- The following code is for local testing only ---
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
