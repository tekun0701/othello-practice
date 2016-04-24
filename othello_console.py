from othello import Board, Color

# ここからがメイン部分だよ
half_x = Board.board_x_size // 2
half_y = Board.board_y_size // 2

main_board = Board(
    {(half_x, half_y): Color.black,
    (half_x, half_y + 1): Color.white,
    (half_x + 1, half_y): Color.white,
    (half_x + 1, half_y + 1): Color.black}
)

while True:
    print(main_board.get_string())
    print(main_board.get_status_dict())
    if main_board.is_finish():
        print("おしまい!")
        exit(0)
    # 自分の置ける石
    player_dict = main_board.get_put_dict(Color.black)

    print("今の●の置ける位置:")
    print(player_dict)
    if player_dict:
        input_x = input("縦位置を入力してみてください(1～%d)：" % Board.board_x_size)
        input_y = input("横位置を入力してみてください(1～%d)：" % Board.board_y_size)
        if (int(input_x), int(input_y)) not in list(player_dict.keys()):
            print("置けないのでやり直し！")
            continue

        # 自分の石を置く
        main_board.put_stone((int(input_x), int(input_y)), Color.black)
        print(main_board.get_string())
        print(main_board.get_status_dict())
        if main_board.is_finish():
            print("おしまい!")
            exit(0)
    else:
        print("置けないので相手へ")

    # 相手の石の置ける一覧を調べる
    enemy_stone, value = main_board.get_evalution_stone(Color.white, 0)
    # (0, 0)が来た時は置けないパターン
    if enemy_stone != (0, 0):
        print("敵の石：")
        print(enemy_stone)
        main_board.put_stone(enemy_stone, Color.white)
    else:
        print("置けないので自分へ")
