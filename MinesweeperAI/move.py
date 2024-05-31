def flag(i, j, flags, mines_no):
    if len(flags) > mines_no: 
        print("You've run out of flags!")
        return "F", False
    return str(i) + " " + str(j) + " F", True

def explore(i, j):
    return str(i) + " " + str(j), True
