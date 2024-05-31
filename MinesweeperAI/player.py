import random
import sys
from move import flag, explore

def getMove(mine_values, flags, mines_no):
    n = len(mine_values)

    def is_valid(r, c):
        return 0 <= r < n and 0 <= c < n

    def get_neighbors(r, c):
        neighbors = []
        for i in range(max(0, r-1), min(n, r+2)):
            for j in range(max(0, c-1), min(n, c+2)):
                if (i != r or j != c) and is_valid(i, j):
                    neighbors.append((i, j))
        return neighbors

    def count_flags_and_hidden(neighbors):
        flag_count = 0
        hidden_count = 0
        for (nr, nc) in neighbors:
            if mine_values[nr][nc] == 'F':
                flag_count += 1
            elif mine_values[nr][nc] == ' ':
                hidden_count += 1
        return flag_count, hidden_count

    # First move safety
    if all(cell == ' ' for row in mine_values for cell in row):
        return explore(n//2, n//2)

    # Safe move list
    safe_moves = []
    # Check for cells that can be flagged or explored
    for r in range(n):
        for c in range(n):
            if mine_values[r][c] not in {' ', 'F', 'M'}:
                mine_count = int(mine_values[r][c])
                neighbors = get_neighbors(r, c)
                flag_count, hidden_count = count_flags_and_hidden(neighbors)

                # If the number of hidden cells around a number equals the number of mines left to be flagged
                if hidden_count > 0 and (mine_count - flag_count) == hidden_count:
                    for (nr, nc) in neighbors:
                        if mine_values[nr][nc] == ' ':
                            return flag(nr+1, nc+1, flags, mines_no)

                # If the number of flagged cells around a number equals the number of mines
                if flag_count == mine_count:
                    for (nr, nc) in neighbors:
                        if mine_values[nr][nc] == ' ':
                            safe_moves.append((nr, nc))

    if safe_moves:
        r, c = safe_moves.pop(0)
        return explore(r+1, c+1)

    # Probability-based decision making
    def get_cell_prob(r, c):
        neighbors = get_neighbors(r, c)
        total_mines = sum(1 for nr, nc in neighbors if mine_values[nr][nc] == 'F')
        hidden_neighbors = sum(1 for nr, nc in neighbors if mine_values[nr][nc] == ' ')
        if hidden_neighbors == 0:
            return 0  # Cell is already explored or flagged
        return total_mines / hidden_neighbors

    min_prob = float('inf')
    best_move = None
    for r in range(n):
        for c in range(n):
            if mine_values[r][c] == ' ':
                prob = get_cell_prob(r, c)
                if prob < min_prob:
                    min_prob = prob
                    best_move = (r, c)

    if best_move:
        r, c = best_move
        return explore(r+1, c+1)

    # Fallback if no move is found
    hidden_cells = [(r, c) for r in range(n) for c in range(n) if mine_values[r][c] == ' ']
    if hidden_cells:
        r, c = random.choice(hidden_cells)
        return explore(r+1, c+1)

    move, status = explore(random.randint(1, n), random.randint(1, n))
    if not status:
        print("Invalid Move!! Exiting!")
        sys.exit(1)
    return move, status