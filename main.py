import tkinter as tk
from custom_button import CustomButton
import random

grid_rows: int = 16
grid_cols: int = 16
total_bombs: int = 40
free_blocks: int = grid_cols * grid_rows - total_bombs
flag_counter: int = total_bombs

root: tk.Tk = tk.Tk()
root.title("MineSweeper")
root.geometry("465x425")

# Create a label for displaying the timer.
timer_label: tk.Label = tk.Label(root, text="Time: 0", font=("Helvetica", 16), fg="red", bg="black", relief=tk.SUNKEN, borderwidth=6)
timer_label.grid(row=0, column=0, columnspan=grid_cols // 4 + 1)
timer_seconds: int = 0
timer_id: int = 0

# Create a label for displaying the number of remaining bombs.
bomb_counter: tk.Label = tk.Label(root, text=str(free_blocks), font=("Helvetica", 16), fg="red", bg="black", relief=tk.SUNKEN, borderwidth=6)
bomb_counter.grid(row=0, column=grid_cols // 3 + 5, columnspan=grid_cols // 3, sticky="e")

smily_img: tk.PhotoImage = tk.PhotoImage(file="smily.png")
smily_img = smily_img.subsample(20)
flag_button: tk.Button = tk.Button(root, image=smily_img, font=("Helvetica", 16), fg="yellow")
flag_button.grid(row=0, column=grid_cols // 4, columnspan=grid_cols // 3, sticky="e")

buttons = []

# Function to update the timer label.
def updateTimer() -> None:
    global timer_seconds, timer_id
    timer_seconds += 1
    timer_label.config(text=f"Time: {timer_seconds}")
    timer_id = root.after(1000, updateTimer)

# Function to update the bomb counter label.
def updatCounter() -> None:
    if free_blocks > 100:
        bomb_counter.configure(text=str(free_blocks))
    elif free_blocks > 10:
        bomb_counter.configure(text="0" + str(free_blocks))
    else:
        bomb_counter.configure(text="00" + str(free_blocks))

# Function to handle left-click events on a cell.
def onLeftClick(i: int, j: int) -> None:
    if buttons[i][j].is_flagged:
        return

    if not buttons[i][j].is_bomb:
        revealCell(i, j)
    else:
        endGame("Lose")
        return

# Function to handle right-click events on a cell.
def onRightClick(i: int, j: int) -> None:
    global flag_counter
    if buttons[i][j].is_disabled:
        return

    if not buttons[i][j].is_flagged:
        buttons[i][j].is_flagged = True
        buttons[i][j].configure(text="🚩", fg="red")
        flag_counter -= 1
    else:
        buttons[i][j].is_flagged = False
        buttons[i][j].configure(text=" ", fg="black")
        flag_counter += 1

# Function to check if the player has won the game.
def flagCheck() -> None:
    if flag_counter != 0:
        return
    else:
        for i in range(grid_rows):
            for j in range(grid_cols):
                if buttons[i][j].is_flagged and not buttons[i][j].is_bomb:
                    return
        endGame("WIN")

# Function to reveal a cell and adjacent cells when it has no adjacent bombs.
def revealCell(i: int, j: int) -> None:
    global free_blocks
    if buttons[i][j].is_flagged or buttons[i][j].is_disabled or buttons[i][j].is_bomb:
        return

    buttons[i][j].is_disabled = True
    buttons[i][j].configure(text=str(buttons[i][j].bombs_around), state="disabled", bg="light gray")
    free_blocks -= 1
    updatCounter()

    if free_blocks == 0:
        endGame("WIN")
    if buttons[i][j].bombs_around == 0:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = i + dx, j + dy
            if 0 <= new_i < grid_rows and 0 <= new_j < grid_cols:
                revealCell(new_i, new_j)

# Function to end the game with the specified outcome.
def endGame(outcome: str) -> None:
    for i in range(grid_rows):
        for j in range(grid_cols):
            if buttons[i][j].is_bomb:
                buttons[i][j].configure(text="💣", state="disabled")

    root.after_cancel(timer_id)
    if outcome == "Lose":
        popup: tk.Toplevel = tk.Toplevel(root)
        popup.title("")
        popup.geometry("300x100")
        message_label: tk.Label = tk.Label(popup, text="YOU LOST.", fg="red", font=("Helvetica", 30))
        message_label.pack()
    else:
        popup: tk.Toplevel = tk.Toplevel(root)
        popup.title("")
        popup.geometry("300x100")
        message_label: tk.Label = tk.Label(popup, text="YOU WIN.", fg="red", font=("Helvetica", 30))
        message_label.pack()

# Function to randomly place bombs on the game grid.
def bombPlacement() -> None:
    i: int = 0
    while i < total_bombs:
        j, k = random.randint(0, grid_rows - 1), random.randint(0, grid_cols - 1)
        if not buttons[j][k].is_bomb:
            buttons[j][k].is_bomb = True
            i += 1

# Function to calculate and store the number of bombs around each cell.
def checkForBombs() -> None:
    for i in range(grid_rows):
        for j in range(grid_cols):
            count: int = 0
            for s in range(i - 1, i + 2):
                for k in range(j - 1, j + 2):
                    if s == i and k == j:
                        continue
                    elif 0 <= s < grid_rows and 0 <= k < grid_cols and buttons[s][k].is_bomb:
                        count += 1
            buttons[i][j].bombs_around = count

# Create and initialize the game grid with buttons.
for i in range(grid_rows):
    row = []
    for j in range(grid_cols):
        is_bomb: bool = False
        cell_button: CustomButton = CustomButton(root, is_bomb, text=" ", width=3, height=1, padx=0, pady=0, fg="#000000")
        cell_button.grid(row=i + 4, column=j)
        row.append(cell_button)
        cell_button.bind("<Button-1>", lambda event, i=i, j=j: onLeftClick(i, j))
        cell_button.bind("<Button-3>", lambda event, i=i, j=j: onRightClick(i, j))
    buttons.append(row)

bombPlacement()
checkForBombs()
updateTimer()
root.mainloop()