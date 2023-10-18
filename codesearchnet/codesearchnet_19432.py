def print_boggle(board):
    "Print the board in a 2-d array."
    n2 = len(board); n = exact_sqrt(n2)
    for i in range(n2):
        if i % n == 0 and i > 0: print
        if board[i] == 'Q': print 'Qu',
        else: print str(board[i]) + ' ',
    print