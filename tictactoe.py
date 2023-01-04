from tkinter import *
from tkinter import ttk


root = Tk()
root.title("Tic Tac Toe")
root.resizable(0, 0)

buttons = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

values = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
current_player = "X"


def click_pvp(r, c):
    global current_player
    global buttons
    global values
    if current_player == "X" and not handle_game_end() and values[r][c] == 0:
        values[r][c] = current_player
        buttons[r][c].configure(text="X")
        current_player = "O"
    elif current_player == "O" and not handle_game_end() and values[r][c] == 0:
        values[r][c] = current_player
        buttons[r][c].configure(text="O")
        current_player = "X"
    handle_game_end()


def click_pvai(r, c):
    global buttons
    global values
    best_score = -1000
    best_move = [0, 0]

    if values[r][c] == 0:
        values[r][c] = "X"
        buttons[r][c].configure(text="X")

        for i in range(3):
            for j in range(3):
                if values[i][j] == 0:
                    values[i][j] = "O"
                    score = minimax(False)
                    values[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = [i, j]

        values[best_move[0]][best_move[1]] = "O"
        buttons[best_move[0]][best_move[1]].configure(text="O")

        handle_game_end()


def minimax(is_maximizing):
    win_side = False
    for i in range(3):
        if values[i][0] == values[i][1] == values[i][2] != 0:
            win_side = values[i][0]
        elif values[0][i] == values[1][i] == values[2][i] != 0:
            win_side = values[0][i]
    if values[0][0] == values[1][1] == values[2][2] != 0:
        win_side = values[0][0]
    elif values[0][2] == values[1][1] == values[2][0] != 0:
        win_side = values[0][2]
    else:
        win_side = "Draw"

    if win_side == "X":
        return -100
    elif win_side == "O":
        return 100
    elif win_side == "Draw":
        return 0

    if is_maximizing:
        best_score = -1000

        for i in range(3):
            for j in range(3):
                if values[i][j] == 0:
                    values[i][j] = "O"
                    score = minimax(False)
                    values[i][j] = 0
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 1000
        for i in range(3):
            for j in range(3):
                if values[i][j] == 0:
                    values[i][j] = "X"
                    score = minimax(True)
                    values[i][j] = 0
                    if score < best_score:
                        best_score = score
        return best_score


def handle_game_end():
    global buttons
    global values
    check = False

    for i in range(3):
        if values[i][0] == values[i][1] == values[i][2] != 0:
            check = [i, 0, i, 1, i, 2]
        elif values[0][i] == values[1][i] == values[2][i] != 0:
            check = [0, i, 1, i, 2, i]
    if values[0][0] == values[1][1] == values[2][2] != 0:
        check = [0, 0, 1, 1, 2, 2]
    elif values[0][2] == values[1][1] == values[2][0] != 0:
        check = [0, 2, 1, 1, 2, 0]

    if check or not any(0 in sublist for sublist in values):
        end_window = Tk()
        end_window.resizable(0, 0)
        frame = ttk.Frame(end_window, padding=20)
        frame.grid()
        if check:
            buttons[check[0]][check[1]].configure(bg="red")
            buttons[check[2]][check[3]].configure(bg="red")
            buttons[check[4]][check[5]].configure(bg="red")
            ttk.Label(frame, text=f"{values[check[0]][check[1]]} wins the game!").grid(
                column=0, row=0)
        else:
            ttk.Label(frame, text="Draw").grid(column=0, row=0)

        ttk.Button(frame, width=10, text="Close", command=lambda: [
                   end_window.destroy(), main_menu()]).grid(column=0, row=1)
        values = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        buttons = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]


def pvp(menu_frame):
    menu_frame.destroy()
    for i in range(3):
        for j in range(3):
            buttons[i][j] = Button(
                width=10, height=5, command=lambda r=i, c=j: click_pvp(r, c))
            buttons[i][j].grid(row=i, column=j)


def pvai(menu_frame):
    menu_frame.destroy()
    for i in range(3):
        for j in range(3):
            buttons[i][j] = Button(
                width=10, height=5, command=lambda r=i, c=j: click_pvai(r, c))
            buttons[i][j].grid(row=i, column=j)


def main_menu():

    for l in root.grid_slaves():
        l.destroy()

    menu_frame = ttk.Frame(root)
    menu_frame.grid()
    ttk.Label(menu_frame, text="Choose mode").grid(row=0, column=1)
    button1 = Button(menu_frame, width=15, height=3,
                     text="Player vs Player", command=lambda frame=menu_frame: pvp(frame))
    button1.grid(row=1, column=0, pady=10, padx=10)
    button2 = Button(menu_frame,  width=15, height=3,
                     text="Player vs computer", command=lambda frame=menu_frame: pvai(frame))
    button2.grid(row=1, column=2, pady=10, padx=10)
    root.mainloop()


main_menu()
