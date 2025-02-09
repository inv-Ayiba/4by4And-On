def solve_puzzle(clues):
    import itertools

    # Helper: given a sequence (row or column) compute how many "skyscrapers" are visible.
    def visible_count(seq):
        count = 0
        max_seen = 0
        for height in seq:
            if height > max_seen:
                count += 1
                max_seen = height
        return count

    # All possible rows (permutations of 1..6)
    all_rows = list(itertools.permutations(range(1, 7)))
    
    # Precompute candidates for each row index.
    # For a row with index i, the left clue is clues[23 - i] and right clue is clues[6 + i].
    candidates = []
    for i in range(6):
        left_clue  = clues[23 - i]
        right_clue = clues[6 + i]
        row_candidates = []
        for row in all_rows:
            if left_clue and visible_count(row) != left_clue:
                continue
            if right_clue and visible_count(row[::-1]) != right_clue:
                continue
            row_candidates.append(row)
        candidates.append(row_candidates)
    
    # Backtracking search:
    solution = None  # to hold the final solution once found
    grid = []        # will store the rows as we build them
    # For each column j, we keep a set of numbers already used in that column.
    cols_used = [set() for _ in range(6)]
    
    def backtrack(row_index):
        nonlocal solution
        if solution is not None:
            return  # already found a solution
        if row_index == 6:
            # Full grid complete: now check the column clues.
            for j in range(6):
                # Build column j:
                col = [grid[r][j] for r in range(6)]
                top_clue = clues[j]         # top clues: indices 0 to 5
                bottom_clue = clues[17 - j]   # bottom clues: note the order!
                if top_clue and visible_count(col) != top_clue:
                    return
                if bottom_clue and visible_count(col[::-1]) != bottom_clue:
                    return
            # All column clues match; we have found our solution.
            solution = [row for row in grid]
            return
        
        # Try each candidate row for the current row index.
        for row in candidates[row_index]:
            # Check column uniqueness: no number in the candidate row must already appear in the same column.
            conflict = False
            for j, num in enumerate(row):
                if num in cols_used[j]:
                    conflict = True
                    break
            if conflict:
                continue
            # Place the row: update grid and mark numbers as used in each column.
            grid.append(row)
            for j, num in enumerate(row):
                cols_used[j].add(num)
            backtrack(row_index + 1)
            if solution is not None:
                return
            # Backtrack: remove the row and update the column sets.
            grid.pop()
            for j, num in enumerate(row):
                cols_used[j].remove(num)
                
    backtrack(0)
    
    if solution is None:
        return None
    # Return the grid as a tuple of tuples, as required.
    return tuple(tuple(row) for row in solution)


# --- Testing with the provided sample puzzles ---
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
