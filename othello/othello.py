class Othello():
    def __init__(self):
        self.board = [[' ' for i in range(10)] for j in range(10)]
        for i in range(9):
            for j in range(9):
                if i in (4,5) and j in (4,5):
                    if i==j:
                        self.board[i][j] = 'x'
                    else:
                        self.board[i][j] = 'o'
                elif i == 0 or j == 0:
                    if j != 0:
                        self.board[i][j] = chr(j+96)
                    if i != 0:
                        self.board[i][j] = str(i)
                else:
                    self.board[i][j] = '.'
    
    def draw(self):
        len_board = len(self.board)
        board = '\n'.join([' '.join(self.board[i]) for i in range(len_board-1)])
        print(board)

    def place(self, color, position):
        try:
            if color == 'b':
                stone = 'o'
            elif color == 'w':
                stone = 'x'
        except:
            print('colorはbかwです')
            return 0
        try:
            row = int(position[1])
            col = ord(position[0])-96
            if self.board[row][col] == '.':
                self.board, re = played_board(self.board, row, col, stone)
                return re
            else:
                print('すでに石があります')
                return 0
        except:
            print('positionはa1~h8です')
            return 0

    def check_situation(self):
        for color in ('b', 'w'):
            if color == 'b':
                stone = 'o'
                b_stone = cnt_stones(self.board)[stone]
            elif color == 'w':
                stone = 'x'
                w_stone = cnt_stones(self.board)[stone]
            print('{}: {}'.format(color, cnt_stones(self.board)[stone]))
        if b_stone > w_stone:
            print('b wins')
        elif b_stone < w_stone:
            print('w wins')
        else:
            print('draw')      
    
    def start(self):
        color = 'b'
        print('start')
        while(1):
            self.draw()
            if cnt_able(self.board, color) == 0:
                print('pass ({} cannot place)'.format(color))
                color = change_color(color)
                if cnt_able(self.board, color) == 0:
                    print('pass ({} cannot place)'.format(color))
                    break
                else:
                    continue
            position = input('select place {}: '.format(color))
            if self.place(color, position):
                color = change_color(color)

        self.check_situation()

    def vs_com(self):
        color = 'b'
        print('start')
        while(1):
            self.draw()
            #print(cnt_able(self.board, color))
            if cnt_able(self.board, color)[0] == 0:
                print('pass ({} cannot place)'.format(color))
                color = change_color(color)
                if cnt_able(self.board, color)[0] == 0:
                    print('pass ({} cannot place)'.format(color))
                    break
                else:
                    continue
            if color == 'b':
                position = input('select place {}: '.format(color))
                if self.place(color, position):
                    color = change_color(color)
                    continue
            else:
                position = com(self.board, color)
                if self.place(color, position):
                    color = change_color(color)

        self.check_situation()        

def change_color(color):
    if color == 'b':
        return 'w'
    elif color == 'w':
        return 'b'
    else:
        print('colorはbかwです')
        return None

def played_board(board, row, col, stone):
    board_ = [[board[i][j] for j in range(len(board[0]))] for i in range(len(board))]

    if stone == 'x':
        another_stone = 'o'
    elif stone == 'o':
        another_stone = 'x'
    else:
        print('stoneはoかxです')
        return board_, 0

    flag = 0
    for i in range(3):
       for j in range(3):
            if board[row+i-1][col+j-1] == another_stone:
                k = 2
                while(row+(i-1)*k not in (0,9) and col+(j-1)*k not in (0,9)):
                    if board[row+(i-1)*k][col+(j-1)*k] == stone:
                        flag = 1
                        for l in range(k):
                            board_[row+(i-1)*l][col+(j-1)*l] = stone
                        break
                    k += 1
    
    if flag == 0:
        print('そこに石は置けません')
        return board_, 0
    else:
        return board_, 1

def cnt_stones(board):
    cnt = {'.':0, 'o':0, 'x':0}
    for i in range(1,9):
        for j in range(1,9):
            cnt[board[i][j]] += 1
    return cnt

def cnt_able(board, color):
    if color == 'b':
        stone = 'o'
        another_stone = 'x'
    elif color == 'w':
        stone = 'x'
        another_stone = 'o'
    else:
        print('colorはbかwです')

    cnt = 0
    ables = []
    for row in range(1,9):
        for col in range(1,9):
            if board[row][col] != '.':
                continue
            flag = 0
            i = 0
            while(i in (0,1,2) and flag == 0):
                j = 0
                while(j in (0,1,2) and flag == 0):
                    if board[row+i-1][col+j-1] == another_stone:
                        k = 2
                        while(row+(i-1)*k not in (0,9) and col+(j-1)*k not in (0,9)):
                            if board[row+(i-1)*k][col+(j-1)*k] == stone:
                                cnt += 1
                                ables.append([row, col])
                                flag = 1
                                break
                            k += 1
                    j += 1    
                i += 1
    return cnt, ables

def com(board, color):
    try:
        if color == 'b':
            stone = 'o'
            another_color = 'w'
        elif color == 'w':
            stone = 'x'
            another_color = 'b'
    except:
        print('cannot play')       

    choices = []
    cnt, candidates = cnt_able(board, color)
    for num in range(cnt):
        row = candidates[num][0]
        col = candidates[num][1]
        board_temp, _ = played_board(board, row, col, stone)
        cnt_temp = cnt_able(board_temp, color)[0]
        cnt_temp_another = cnt_able(board_temp, another_color)[0]
        d_eval = eval_board(board_temp)
        choices.append([row, col, d_eval[color] + cnt_temp])
    choices.sort(reverse=True, key=lambda x: x[2])

    position = '{}{}'.format(chr(int(choices[0][1])+96), int(choices[0][0]))
    print('com select {}'.format(position))
    return position

def eval_board(board):
    d_eval = {'b':0, 'w':0}
    for i in range(1,9):
        for j in range(1,9):
            i_ = min(i, 9-i)
            j_ = min(j, 9-j)
            pos = (min(i_, j_), max(i_, j_))
            if pos == (1, 1):
                if board[i][j]  == 'o':
                    d_eval['b'] += 30
                elif board[i][j] == 'x':
                    d_eval['w'] += 30
            elif pos == (1, 2):
                if board[i][j]  == 'o':
                    d_eval['b'] += -12
                elif board[i][j] == 'x':
                    d_eval['w'] += -12
            elif pos == (2, 2):
                if board[i][j]  == 'o':
                    d_eval['b'] += -15
                elif board[i][j] == 'x':
                    d_eval['w'] += -15                             
            elif min(i_, j_) == 2:
                if board[i][j]  == 'o':
                    d_eval['b'] += -3
                elif board[i][j] == 'x':
                    d_eval['w'] += -3                
            elif max(i_, j_) == 4:
                if board[i][j]  == 'o':
                    d_eval['b'] += -1
                elif board[i][j] == 'x':
                    d_eval['w'] += -1
    vec = [(1,1), (1,-1), (-1,1), (-1,-1)]
    for (c,s)  in [('b','o'), ('w','x')]:
        for idx, (i, j) in enumerate([(1,1), (1,8), (8,1), (8,8)]):
            if board[i][j] == s:
                k = 1
                while(board[i+k*vec[idx][0]][j] == s and k < 7):
                    d_eval[c] += 12
                    k += 1
                k = 1
                while(board[i][j+k*vec[idx][1]] == s and k < 7):
                    d_eval[c] += 12
                    k += 1
    return d_eval

if __name__ == '__main__':
    othello = Othello()
    #othello.start()
    othello.vs_com()