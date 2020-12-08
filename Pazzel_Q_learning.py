from random import shuffle, randrange

alpha = 0.1
landa = 0.9


def find_empty_index(board):
    i = 0
    j = 0
    for t in range(len(board)):
        if board[t] == 'o':
            return t // 3, t % 3
    return i, j


def select_move(s, Q, dic):
    i, j = find_empty_index(s)
    possible_moves = []
    if i > 0:
        possible_moves.append(0)
    if i< 2:
        possible_moves.append(1)
    if j<2:
        possible_moves.append(2)
    if j > 0:
        possible_moves.append(3)
    max_list = possible_moves
    a = -1
    index = dic[s]
    max_Q = -2
    if len(max_list) > 1:
        a = max_list[randrange(0, len(max_list))]
    return a


def make_move(s, a):
    t = 0
    for i in range(len(s)):
        if s[i] == 'o':
            t = i
            break

    s = [char for char in s]
    if a == 0:  # up
        s[t], s[t - 3] = s[t - 3], s[t]
    elif a == 1:
        s[t], s[(t + 3)%len(s)] = s[(t + 3)%len(s)], s[t]
    elif a == 2:
        s[t], s[t + 1] = s[t + 1], s[t]
    else:
        s[t], s[t - 1] = s[t - 1], s[t]
    s = ''.join(s)
    return s


def update_Q(Q, R, dic, board, a, new):
    index = dic[board]
    snew = dic[new]
    max = 0
    for i in Q[snew]:
        if i > max:
            max = i
    Q[index][a] = ((1 - alpha) * Q[index][a]) + (alpha * (R[index][a] + (landa * max)))

    return Q


def run_Qlearning():
    R = [[0 for i in range(4)] for j in range(630)]
    Q = [[0.0 for i in range(4)] for j in range(630)]
    state = ['sssmsmmom']
    list = ['s', 's', 's', 's', 'm', 'm', 'm', 'm', 'o']
    while len(state) < 630:
        while ''.join(list) in state:
            shuffle(list)
        state.append(''.join(list))
    dic = dict([(state[i], i) for i in range(630)])
    R[dic['mmsosmsms']][0] = 1
    R[dic['mosmsmsms']][3] = 1

    goal = 'omsmsmsms'
    counter = 0
    print("training please wait")
    while counter < 600:
        board = 'sssmsmmom'
        finish = 0
        time = 0
        while not finish:
            a = select_move(board, Q, dic)
            newboard = make_move(board, a)
            Q = update_Q(Q, R, dic, board, a, newboard)
            past =board
            board = newboard
            if board == goal or time == 200:
                finish = 1
            time+=1
        counter += 1

    for i in range(630):
        print(i, state[i], end=" : ")
        for j in Q[i]:
            print(round(j,6),end=",")
        print('\n')

    return Q, dic


def display(s):
    print("-------------")
    print("[", s[0], ',', s[1], ',', s[2], "]")
    print("[", s[3], ',', s[4], ',', s[5], "]")
    print("[", s[6], ',', s[7], ',', s[8], "]")
    return


def next_move(board, Q, dic):
    index = dic[board]
    move = 0
    max =0
    for i in range(len(Q[index])):
        if Q[index][i] > max:
            max = Q[index][i]
            move = i
    board = make_move(board, move)
    return board


def play(Q, dic):
    board = "sssmsmmom"
    display(board)
    finish = 0
    goal = 'omsmsmsms'
    counter = 0
    while not finish:
        board = next_move(board, Q, dic)
        counter += 1
        display(board)

        if goal == board:
            finish = 1
    print("**************************************")
    print("number of moves:", counter)
    return


if __name__ == "__main__":
    Q, dictionary = run_Qlearning()
    play(Q, dictionary)
