from enum import Enum
import copy

class Color(Enum):
    black = 1
    white = 2

class Neighbor(Enum):
    top_left = (-1, -1)
    center_left = (0, -1)
    bottom_left = (1, -1)
    top_center = (-1, 0)
    bottom_center = (1, 0)
    top_right = (-1, 1)
    center_right = (0, 1)
    bottom_right = (1, 1)


class Board:
    board_x_size = 8
    board_y_size = 8
    # 敵の強さ（探索度）
    max_dept = 4
    # 動的に探索度を変えてみる
    is_dynamic_dept = True
    # 評価関数
    evaluation = {
        (1, 1): 30,  (1, 2): -12, (1, 3):0,   (1, 4): -1, (1, 5): -1, (1, 6):0,  (1, 7): -12, (1, 8): 30,
        (2, 1): -12, (2, 2): -15, (2, 3): -3, (2, 4): -3, (2, 5): -3, (2, 6):-3, (2, 7): -15, (2, 8): -12,
        (3, 1): 0,   (3, 2): -3,  (3, 3): 0,  (3, 4): -1, (3, 5): -1, (3, 6):0,  (3, 7): -3,  (3, 8): 0,
        (4, 1): -1,  (4, 2): -3,  (4, 3): -1, (4, 4): -1, (4, 5): -1, (4, 6):-1, (4, 7): -3,  (4, 8): -1,
        (5, 1): -1,  (5, 2): -3,  (5, 3): -1, (5, 4): -1, (5, 5): -1, (5, 6):-1, (5, 7): -3,  (5, 8): -1,
        (6, 1): 0,   (6, 2): -3,  (6, 3): 0,  (6, 4): -1, (6, 5): -1, (6, 6):0,  (6, 7): -3,  (6, 8): 0,
        (7, 1): -12, (7, 2): -15, (7, 3): -3, (7, 4): -3, (7, 5): -3, (7, 6):-3, (7, 7): -15, (7, 8): -12,
        (8, 1): 30,  (8, 2): -12, (8, 3): 0,  (8, 4): -1, (8, 5): -1, (8, 6):0,  (8, 7): -12, (8, 8): 30
    }

    # 初期
    def __init__(self, stone_dict):
        self.stone_dict = stone_dict

    # オセロの文字列表現
    def get_string(self):
        str = ""
        for x in range(1, self.board_x_size+1):
            for y in range(1, self.board_y_size+1):
                if (x,y) in self.stone_dict:
                    if self.stone_dict[(x,y)] == Color.black:
                        str += "● "
                    else:
                        str += "○ "
                else:
                    str += "― "
            str += "\n"
        return str

    # 置ける位置を返す
    def get_put_dict(self, input_color):
        put_dict = {}
        for locate, color in self.stone_dict.items():
            # 自分の色
            if color == input_color:
                # 隣接の石を見る
                for neighbor in Neighbor:
                    # その方向に石を置ける座標を返す
                    xy = self.get_put_pos(input_color, locate, neighbor)
                    if xy:
                        # 探査始めた座標と隣接していないときだけが候補になる
                        if abs(xy[0] - locate[0]) >= 2 or \
                                abs(xy[1] - locate[1]) >= 2:
                            put_dict[xy] = input_color
        return put_dict

    # その座標の方向において置けるかどうか？
    def get_put_pos(self, input_color, locate, neighbor):
        new_x = locate[0] + neighbor.value[0]
        new_y = locate[1] + neighbor.value[1]
        if (new_x, new_y) in self.stone_dict:
            # 違う色だったらさらに進む
            # 同じ色が来たらその方向にはおけない
            if self.stone_dict[(new_x, new_y)] != input_color:
                return self.get_put_pos(input_color, (new_x, new_y), neighbor)
            else:
                return None
        else:
            # 石がない場合は盤面の範囲内であれば大丈夫
            # (もしくは隣接していない場合)
            if 1 <= new_x <= self.board_x_size and 1 <= new_y <= self.board_x_size:
                return (new_x, new_y)

    # 石を置く
    def put_stone(self, locate, input_color):
        self.stone_dict[locate] = input_color
        # 隣接の石を見る
        for neighbor in Neighbor:
            # その方向にある石を裏返す
            self.set_put_pos(input_color, locate, neighbor)

    # その方向にある石を裏返していく
    def set_put_pos(self, input_color, locate, neighbor):
        new_x = locate[0] + neighbor.value[0]
        new_y = locate[1] + neighbor.value[1]
        if (new_x, new_y) in self.stone_dict:
            # 違う色だったらさらに進む
            if self.stone_dict[(new_x, new_y)] != input_color:
                self.set_put_pos(input_color, (new_x, new_y), neighbor)
            else:
                # 同じ色だったら逆にたどって同じ色に会うまでひっくり返す
                while True:
                    c_x = new_x - neighbor.value[0]
                    c_y = new_y - neighbor.value[1]
                    if self.stone_dict[(c_x, c_y)] == input_color:
                        break
                    self.stone_dict[(c_x, c_y)] = input_color
                    new_x = c_x
                    new_y = c_y

    # 今の勝敗状況
    def get_status_dict(self):
        status_dict = {
            Color.black: 0,
            Color.white: 0
        }
        for color in self.stone_dict.values():
            status_dict[color] += 1
        return status_dict

    # ゲーム終わったかどうか
    def is_finish(self):
        # 両方置けなくなったら終わり
        return not self.get_put_dict(Color.black) and not self.get_put_dict(Color.white)

    # 石の一覧を返す
    def get_stone_dict(self):
        return self.stone_dict

    # 置ける手と評価値を返す
    def get_evalution_stone(self, input_color, dept):
        # 一定深くなったら探索しない
        if dept >= self.max_dept:
            return (0, 0), self.get_evalution_estimate_value(input_color)
        board = Board(self.stone_dict)
        put_dict = board.get_put_dict(input_color)
        if dept == 0 and self.is_dynamic_dept:
            self.max_dept = max(10 - len(put_dict) // 2 * 2, 4)
        m_value = None
        m_stone = None
        if put_dict:
            for candidate_stone in list(put_dict.keys()):
                # 石を仮で置く
                copy_board = Board(copy.deepcopy(self.stone_dict))
                copy_board.put_stone(candidate_stone, input_color)
                # 相手の置ける石一覧を見る
                reverse_color = self.reserse_color(input_color)
                reverse_stone, value = copy_board.get_evalution_stone(reverse_color, dept+1)
                # deptが偶数の時はmax比較、奇数のときはmin比較
                if dept % 2 == 1:
                    if m_value is None or value <= m_value:
                        m_value = value
                        m_stone = candidate_stone
                else:
                    if m_value is None or value >= m_value:
                        m_value = value
                        m_stone = candidate_stone
            return m_stone, m_value
        else:
            reverse_color = self.reserse_color(input_color)
            # 反対の色が置けるとき
            if board.get_put_dict(reverse_color):
                # 置けない時は敵に置かせる
                return self.get_evalution_stone(input_color, dept+1)
            else:
                # 置けない時は終局状態なので個数差で返す
                return (0,0), self.get_color_value(input_color) * 10000


    # 逆の色を返す
    def reserse_color(self, color):
        if color == Color.white:
            return Color.black
        else:
            return Color.white

    # 評価値を返す(概算値)
    def get_evalution_estimate_value(self, input_color):
        status_dict = {
            Color.black: 0,
            Color.white: 0
        }
        for stone, color in self.stone_dict.items():
            status_dict[color] += self.evaluation[stone]
        evaluation = status_dict[Color.black] - status_dict[Color.white]
        return -1 * evaluation if input_color == Color.white else evaluation

    # 個数の差を返す
    def get_color_value(self, input_color):
        status_dict = {
            Color.black: 0,
            Color.white: 0
        }
        for stone, color in self.stone_dict.items():
            status_dict[color] += 1
        evaluation = status_dict[Color.black] - status_dict[Color.white]
        return -1 * evaluation if input_color == Color.white else evaluation
