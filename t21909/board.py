from config import DIM
from stone import Stone
from position import Position


class Board:
    # 8方向
    DIRS = [
        [dx, dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1]
        if dx != 0 or dy != 0
    ]

    def __init__(self):
        self.board = [
            [Stone.SPACE for _ in range(DIM)] for _ in range(DIM)
        ]
        self.init_status()

    # (x, y) が board 上にあるか？
    def in_board(self, x, y):
        return (0 <= x < DIM) and (0 <= y < DIM)

    # 盤面の初期化（初期配置）
    def init_board(self):
        for y in range(DIM):
            for x in range(DIM):
                self.board[y][x] = Stone.SPACE

        c0 = DIM // 2 - 1
        self.board[c0][c0] = Stone.WHITE
        self.board[c0 + 1][c0 + 1] = Stone.WHITE
        self.board[c0 + 1][c0] = Stone.BLACK
        self.board[c0][c0 + 1] = Stone.BLACK

        self.init_status()

    def set_board(self, turn, ary2d):
        num = 0
        for y in range(DIM):
            for x in range(DIM):
                c = ary2d[y][x]
                if c == "o":
                    self.board[y][x] = Stone.WHITE
                    num += 1
                elif c == "x":
                    self.board[y][x] = Stone.BLACK
                    num += 1
                else:
                    self.board[y][x] = Stone.SPACE

        self.turn = turn     # 手番
        self.move_num = num  # 手数

        return self

    # 黒白の石数を Dict で返す
    def get_discs(self):
        discs = {Stone.BLACK: 0, Stone.WHITE: 0, Stone.SPACE: 0}
        for y in range(DIM):
            for x in range(DIM):
                discs[(self.board[y][x])] += 1
        return discs

    # 手番、手数の初期化
    def init_status(self):
        self.turn = Stone.BLACK  # 手番
        self.move_num = 0       # 手数

    # 指定のマスに石を打てるか？
    def is_movable(self, position):
        return self.is_movable_xy(position.x, position.y)

    def is_movable_xy(self, px, py):
        # 空きでなければ打てない
        if self.board[py][px] != Stone.SPACE:
            return False

        # 各方向に石をひっくり返せるか？
        for dx, dy in Board.DIRS:
            y = py + dy
            x = px + dx
            enemy = self.turn.invert()
            if self.in_board(x, y) and self.board[y][x] == enemy:
                # 隣が相手の石
                y += dy
                x += dx
                while self.in_board(x, y) and self.board[y][x] == enemy:
                    y += dy
                    x += dx
                if self.in_board(x, y) and self.board[y][x] == self.turn:
                    return True

        return False

    # 石を打てる Position のリストを返す
    def get_moveable_list(self):
        return [
            Position(x, y)
            for x in range(DIM) for y in range(DIM)
            if self.is_movable_xy(x, y)
        ]

    def set_marks(self, mark_list, disp=True):
        if disp:
            stone = Stone.MARK
        else:
            stone = Stone.SPACE

        for positon in mark_list:
            self.board[positon.y][positon.x] = stone

    # 局面を進める
    def move(self, position):
        reverse_stons = []
        # 石を打つ
        self.board[position.y][position.x] = Stone(self.turn.value)

        # 石をひっくり返す
        # 各方向に石をひっくり返せるか調べる
        for dx, dy in Board.DIRS:
            y = position.y + dy
            x = position.x + dx
            enemy = self.turn.invert()
            if self.in_board(x, y) \
                    and self.board[y][x] == enemy:
                # 隣が相手の石
                y += dy
                x += dx
                while self.in_board(x, y) \
                        and self.board[y][x] == enemy:
                    y += dy
                    x += dx
                if self.in_board(x, y) \
                        and self.board[y][x] == self.turn:
                    # この方向は返せる
                    # 1マス戻る
                    y -= dy
                    x -= dx
                    # 戻りながら返す
                    stons = []
                    while self.in_board(x, y) \
                            and self.board[y][x] == enemy:
                        self.board[y][x] = Stone(self.turn.value)
                        stons.append([x, y])
                        y -= dy
                        x -= dx

                    reverse_stons.append(stons)

        self.turn = self.turn.invert()  # 手番を変更
        self.move_num += 1              # 手数を増やす
        return reverse_stons

    # パスする
    def move_pass(self):
        self.turn = self.turn.invert()  # パス

    # 対局終了の判定
    def is_game_end(self):
        # 60手に達した時
        if self.move_num == DIM * DIM - 4:
            return True

        # 黒白どちらかの石数が0になった時
        discs = self.get_discs()
        if discs[Stone.BLACK] == 0 or discs[Stone.WHITE] == 0:
            return True

        # 黒白どちらも手がない場合
        move_list1 = self.get_moveable_list()
        if len(move_list1) == 0:
            self.move_pass()  # パスして相手番にする
            move_list2 = self.get_moveable_list()
            self.move_pass()  # パスして戻す
            if len(move_list2) == 0:
                return True

        return False
