def solve_puzzle(clues):
    import itertools

    # Helper: compute visible count (a new building is seen if it is taller than all before)
    def visible_count(seq):
        count, max_seen = 0, 0
        for height in seq:
            if height > max_seen:
                count += 1
                max_seen = height
        return count

    # Precompute all 720 possible rows (permutations of 1..6)
    all_rows = list(itertools.permutations(range(1, 7)))
    
    # For each row (0 is top, 5 is bottom) filter candidates using the row's left/right clues.
    # Left clue is at index 23-i and right clue at index 6+i.
    candidates = {}
    for i in range(6):
        left_clue = clues[23 - i]
        right_clue = clues[6 + i]
        cand = []
        for row in all_rows:
            if left_clue and visible_count(row) != left_clue:
                continue
            if right_clue and visible_count(row[::-1]) != right_clue:
                continue
            cand.append(row)
        candidates[i] = cand

    # Choose a good ordering: assign first the row indices with the fewest candidates.
    row_order = sorted(range(6), key=lambda i: len(candidates[i]))

    # For each column j (0...5) keep track of used numbers.
    cols_used = [set() for _ in range(6)]
    # This dictionary will store the candidate row (a tuple) for each row index.
    assignment = {}
    solution = None

    # Forward checking: for every unassigned row, there must be at least one candidate
    # that does not conflict with the current column assignments.
    def forward_check():
        for r in row_order:
            if r in assignment:
                continue
            valid_candidate_exists = False
            for candidate in candidates[r]:
                conflict = False
                for j, val in enumerate(candidate):
                    if val in cols_used[j]:
                        conflict = True
                        break
                if not conflict:
                    valid_candidate_exists = True
                    break
            if not valid_candidate_exists:
                return False
        return True

    # Backtracking over rows in the order given by row_order.
    def backtrack(idx):
        nonlocal solution
        if solution is not None:
            return  # solution found already
        if idx == len(row_order):
            # Reconstruct grid in natural order (row 0 is the top, row 5 the bottom).
            grid = [assignment[i] for i in range(6)]
            # Now check the column clues.
            for j in range(6):
                col = [grid[r][j] for r in range(6)]
                top_clue = clues[j]         # Top clues: indices 0 to 5 (left-to-right)
                bottom_clue = clues[17 - j]   # Bottom clues: indices 17 down to 12 (left-to-right)
                if top_clue and visible_count(col) != top_clue:
                    return
                if bottom_clue and visible_count(col[::-1]) != bottom_clue:
                    return
            solution = grid[:]  # found a valid solution
            return

        r = row_order[idx]
        for row_candidate in candidates[r]:
            # Check column uniqueness: candidate's number must not appear already in the same column.
            if any(row_candidate[j] in cols_used[j] for j in range(6)):
                continue
            # Place the candidate row.
            assignment[r] = row_candidate
            for j, num in enumerate(row_candidate):
                cols_used[j].add(num)
            # Do forward checking: if any unassigned row has no possible candidate, backtrack.
            if forward_check():
                backtrack(idx + 1)
                if solution is not None:
                    return
            # Remove the assignment and restore column state.
            del assignment[r]
            for j, num in enumerate(row_candidate):
                cols_used[j].remove(num)

    backtrack(0)
    
    if solution is None:
        return None
    # Return the solution as a tuple of 6 tuples (each row).
    return tuple(tuple(row) for row in solution)


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
