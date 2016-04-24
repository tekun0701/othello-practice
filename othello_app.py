from flask import Flask
from flask import render_template, flash
from othello import Board, Color

app = Flask(__name__)

# 初期マップ
half_x = Board.board_x_size // 2
half_y = Board.board_y_size // 2
main_board = Board(
        {(half_x, half_y): Color.black,
         (half_x, half_y + 1): Color.white,
         (half_x + 1, half_y): Color.white,
         (half_x + 1, half_y + 1): Color.black}
    )

@app.route('/')
def main():
    main_board = Board(
        {(half_x, half_y): Color.black,
         (half_x, half_y + 1): Color.white,
         (half_x + 1, half_y): Color.white,
         (half_x + 1, half_y + 1): Color.black}
    )
    return render_template(
            'othello.html',
            board_x_size=Board.board_x_size,
            board_y_size=Board.board_y_size,
            stone_dict=main_board.get_stone_dict(),
            put_dict=main_board.get_put_dict(Color.black),
            status_dict=main_board.get_status_dict(),
            is_finish=main_board.is_finish(),
            Color=Color)


@app.route('/stone/<int:x>/<int:y>')
def put_stone(x, y):
    enemy_stone = (0, 0)
    if (x, y) in main_board.get_put_dict(Color.black):
        main_board.put_stone((x, y), Color.black)
        while True:
            # 最適な石を算出する
            enemy_stone, value = main_board.get_evalution_stone(Color.white, 0)
            if enemy_stone != (0, 0):
                # 石を置く
                main_board.put_stone(enemy_stone, Color.white)
                # もし自分の石が置けたら大丈夫だが置けない時は敵のターン
                if main_board.get_put_dict(Color.black):
                    break
            # 終局判定
            if main_board.is_finish():
                break

    return render_template(
            'othello.html',
            board_x_size=Board.board_x_size,
            board_y_size=Board.board_y_size,
            stone_dict=main_board.get_stone_dict(),
            put_dict=main_board.get_put_dict(Color.black),
            status_dict=main_board.get_status_dict(),
            is_finish=main_board.is_finish(),
            enemy_stone=enemy_stone,
            Color=Color)

if __name__ == '__main__':
    app.run(debug=True)
