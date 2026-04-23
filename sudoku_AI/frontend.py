import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


SIZE = 9
BOX_SIZE = 3
SOLVER_PATH = Path(__file__).with_name("sudoku_solver.pl")
USER_TEXT_COLOR = "black"
SOLVER_TEXT_COLOR = "#0066cc"
NORMAL_CELL_BG = "white"
SOLVER_CELL_BG = "#eaf4ff"


# -------------------------
# Convert grid
# -------------------------
def grid_to_prolog(grid):
    rows = []
    for row in grid:
        new_row = []
        for val in row:
            if val == "":
                new_row.append("_")
            else:
                new_row.append(val)
        rows.append("[" + ",".join(new_row) + "]")
    return "[" + ",".join(rows) + "]"


# -------------------------
# Validation
# -------------------------
def is_valid_input(grid):
    for row in grid:
        for val in row:
            if val != "":
                if not val.isdigit() or not (1 <= int(val) <= SIZE):
                    return False
    return True


def duplicate_message(values, label):
    seen = set()
    for val in values:
        if val == "":
            continue
        if val in seen:
            return f"{label} has duplicate {val}."
        seen.add(val)
    return None


def find_contradiction(grid):
    for i, row in enumerate(grid):
        message = duplicate_message(row, f"Row {i + 1}")
        if message:
            return message

    for j in range(SIZE):
        column = [grid[i][j] for i in range(SIZE)]
        message = duplicate_message(column, f"Column {j + 1}")
        if message:
            return message

    for box_row in range(0, SIZE, BOX_SIZE):
        for box_col in range(0, SIZE, BOX_SIZE):
            box = [
                grid[i][j]
                for i in range(box_row, box_row + BOX_SIZE)
                for j in range(box_col, box_col + BOX_SIZE)
            ]
            label = f"Box {box_row // BOX_SIZE + 1},{box_col // BOX_SIZE + 1}"
            message = duplicate_message(box, label)
            if message:
                return message

    return None


# -------------------------
# Solve
# -------------------------
def solve_sudoku():
    grid = get_grid()
    solver_cells = [[grid[i][j] == "" for j in range(SIZE)] for i in range(SIZE)]

    if not is_valid_input(grid):
        messagebox.showerror("Error", "Only numbers 1-9 allowed")
        return

    contradiction = find_contradiction(grid)
    if contradiction:
        messagebox.showerror("Error", contradiction)
        return

    reset_cell_colors()
    threading.Thread(target=run_solver, args=(grid, solver_cells), daemon=True).start()


def get_grid():
    return [[entries[i][j].get().strip() for j in range(SIZE)] for i in range(SIZE)]


def clear_grid():
    for row in entries:
        for entry in row:
            entry.delete(0, tk.END)
            entry.config(fg=USER_TEXT_COLOR, bg=NORMAL_CELL_BG)


def reset_cell_colors():
    for row in entries:
        for entry in row:
            entry.config(fg=USER_TEXT_COLOR, bg=NORMAL_CELL_BG)


def show_error(title, message):
    root.after(0, lambda: messagebox.showerror(title, message))


def fill_solution(output, solver_cells):
    rows = output.strip().splitlines()

    if len(rows) < SIZE:
        messagebox.showerror("Error", "No solution found!")
        return

    for i in range(SIZE):
        row_vals = rows[i].strip().strip("[]").split(",")
        if len(row_vals) != SIZE:
            messagebox.showerror("Error", "Unexpected solver output.")
            return

        for j in range(SIZE):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, row_vals[j].strip())
            if solver_cells[i][j]:
                entries[i][j].config(fg=SOLVER_TEXT_COLOR, bg=SOLVER_CELL_BG)
            else:
                entries[i][j].config(fg=USER_TEXT_COLOR, bg=NORMAL_CELL_BG)


def run_solver(grid, solver_cells):
    prolog_input = grid_to_prolog(grid)
    goal = f"solve9({prolog_input}),halt."

    try:
        result = subprocess.run(
            ["swipl", "-q", "-s", str(SOLVER_PATH), "-g", goal],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0:
            error = result.stderr.strip() or "No solution found!"
            show_error("Error", error)
            return

        root.after(0, lambda: fill_solution(result.stdout, solver_cells))

    except subprocess.TimeoutExpired:
        show_error("Error", "Solver took too long!")
    except Exception as e:
        show_error("Error", str(e))


# -------------------------
# Navigation
# -------------------------
def move_focus(event, i, j):
    key = event.keysym

    if key == "Up" and i > 0:
        entries[i - 1][j].focus_set()
    elif key == "Down" and i < SIZE - 1:
        entries[i + 1][j].focus_set()
    elif key == "Left" and j > 0:
        entries[i][j - 1].focus_set()
    elif key == "Right" and j < SIZE - 1:
        entries[i][j + 1].focus_set()


def on_key_release(event, i, j):
    val = entries[i][j].get()
    if len(val) == 1 and val.isdigit():
        if j < SIZE - 1:
            entries[i][j + 1].focus_set()


def main():
    global root, entries

    # -------------------------
    # GUI
    # -------------------------
    root = tk.Tk()
    root.title("9x9 Sudoku Solver")
    root.geometry("430x500")

    entries = []

    for i in range(SIZE):
        row = []
        for j in range(SIZE):
            e = tk.Entry(
                root,
                width=2,
                font=("Arial", 18),
                justify="center",
                fg=USER_TEXT_COLOR,
                bg=NORMAL_CELL_BG,
            )
            padx = (8 if j % BOX_SIZE == 0 else 2, 8 if j % BOX_SIZE == BOX_SIZE - 1 else 2)
            pady = (8 if i % BOX_SIZE == 0 else 2, 8 if i % BOX_SIZE == BOX_SIZE - 1 else 2)
            e.grid(row=i, column=j, padx=padx, pady=pady)

            e.bind("<KeyPress>", lambda event, i=i, j=j: move_focus(event, i, j))
            e.bind("<KeyRelease>", lambda event, i=i, j=j: on_key_release(event, i, j))

            row.append(e)
        entries.append(row)

    btn = tk.Button(
        root,
        text="Solve",
        command=solve_sudoku,
        bg="green",
        fg="white",
        font=("Arial", 12),
    )
    btn.grid(row=SIZE + 1, column=0, columnspan=4, pady=14)

    clear_btn = tk.Button(
        root,
        text="Clear",
        command=clear_grid,
        bg="gray",
        fg="white",
        font=("Arial", 12),
    )
    clear_btn.grid(row=SIZE + 1, column=5, columnspan=4, pady=14)

    root.mainloop()


if __name__ == "__main__":
    main()
