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
            elif color == 'w':
                stone = 'x'
            print('{}: {}'.format(color, cnt_stones(self.board)[stone]))
    
    def start(self):
        color = 'b'
        print('start')
        while():
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
        

def change_color(color):
    if color == 'b':
        return 'w'
    elif color == 'w':
        return 'b'
    else:
        print('colorはbかwです')
        return None

def played_board(board, row, col, stone):
    if stone == 'x':
        another_stone = 'o'
    elif stone == 'o':
        another_stone = 'x'
    else:
        print('stoneはoかxです')
        return board, 0

    flag = 0
    for i in range(3):
       for j in range(3):
            if board[row+i-1][col+j-1] == another_stone:
                k = 2
                while(row+(i-1)*k not in (0,9) and col+(j-1)*k not in (0,9)):
                    if board[row+(i-1)*k][col+(j-1)*k] == stone:
                        flag = 1
                        for l in range(k):
                            board[row+(i-1)*l][col+(j-1)*l] = stone
                        break
                    k += 1
    
    if flag == 0:
        print('そこに石は置けません')
        return board, 0
    else:
        return board, 1

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
                                flag = 1
                                break
                            k += 1
                    j += 1    
                i += 1
    return cnt

if __name__ == '__main__':
    othello = Othello()
    othello.start()
    # othello.check_situation()
    # othello.draw()
    # othello.place('b','d3')
    # othello.check_situation()
    # othello.draw()
    # othello.place('w','e3')
    # othello.check_situation()
    # othello.draw()