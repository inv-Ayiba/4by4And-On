def solve_puzzle(clues):
    import itertools
    from functools import lru_cache

    n = 6

    # Helper: count visible skyscrapers in a sequence.
    def visible(seq):
        cnt, max_seen = 0, 0
        for x in seq:
            if x > max_seen:
                cnt += 1
                max_seen = x
        return cnt

    # Precompute all 720 row permutations (rows of numbers 1..6)
    all_rows = list(itertools.permutations(range(1, n+1)))
    # Precompute each row's visible counts (from left and from right)
    row_vis = { row: (visible(row), visible(row[::-1])) for row in all_rows }

    # For a grid row r (0 = top, 5 = bottom) the clues are:
    #   left clue  = clues[23 - r]    (since left clues are given bottom-to–top)
    #   right clue = clues[6 + r]      (right clues are given top-to–bottom)
    # For each candidate row we also precompute a candidate mask: for each column j,
    # the number row[j] is represented as (1 << (row[j]-1)) shifted left by (j*6) bits.
    def compute_mask(row):
        m = 0
        for j, num in enumerate(row):
            m |= (1 << (num - 1)) << (j * 6)
        return m

    # Build candidate lists for each grid row index.
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
            cand_list.append((row, compute_mask(row)))
        candidates[r] = cand_list

    # We choose an ordering of grid rows (a permutation of 0..5) sorted by increasing candidate count.
    order = sorted(range(n), key=lambda r: len(candidates[r]))

    # Forward checking: for each remaining (unassigned) grid row, ensure at least one candidate fits the current used mask.
    def forward_check(pos, used):
        for i in range(pos, n):
            r = order[i]
            possible = False
            for cand, mask in candidates[r]:
                if used & mask == 0:
                    possible = True
                    break
            if not possible:
                return False
        return True

    # We cache on (pos, used, assignment) where:
    #   pos is the current depth in our 'order' list,
    #   used is the current integer mask representing numbers used in all columns,
    #   assignment is a tuple of candidate rows (in the order of 'order').
    @lru_cache(maxsize=None)
    def search(pos, used, assignment):
        if pos == n:
            # Full assignment reached.
            # Reconstruct the grid in natural row order.
            assign_dict = { order[i]: assignment[i] for i in range(n) }
            grid = tuple(assign_dict[i] for i in range(n))
            # Verify the column clues.
            for j in range(n):
                col = [grid[i][j] for i in range(n)]
                top = clues[j]          # top clue for column j
                bottom = clues[17 - j]    # bottom clue for column j
                if top and visible(col) != top:
                    return None
                if bottom and visible(col[::-1]) != bottom:
                    return None
            return assignment  # assignment tuple is our “solution”
        r = order[pos]
        for cand, mask in candidates[r]:
            if used & mask:
                continue
            new_used = used | mask
            if not forward_check(pos + 1, new_used):
                continue
            res = search(pos + 1, new_used, assignment + (cand,))
            if res is not None:
                return res
        return None

    sol_assignment = search(0, 0, ())
    if sol_assignment is None:
        return None
    # Build grid (tuple of 6 tuples) in natural row order.
    assign_dict = { order[i]: sol_assignment[i] for i in range(n) }
    grid = tuple(assign_dict[i] for i in range(n))
    return grid

# --- Local testing code (remove or comment out before submission) ---
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
