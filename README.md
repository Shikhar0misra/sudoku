# 🧩 Sudoku Solver (Prolog + Python GUI)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Prolog](https://img.shields.io/badge/Prolog-SWI--Prolog-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> A 9×9 Sudoku Solver powered by **Prolog (CLPFD)** for constraint-based logic solving and **Python (Tkinter)** for an interactive GUI.

---

## 📌 Overview

This project combines the power of **logic programming** with a clean **graphical interface**. The user enters a Sudoku puzzle, clicks Solve, and the Prolog backend instantly computes the solution using constraint logic programming (CLP).

---

## 🚀 Features

- ✅ 9×9 interactive Sudoku grid
- ✅ Input validation (only digits 1–9 accepted)
- ✅ Duplicate detection in rows, columns & 3×3 boxes
- ✅ Fast solving via Prolog CLPFD constraints
- ✅ Solver-filled cells highlighted in the GUI
- ✅ Keyboard arrow key navigation

---

## 🛠️ Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Frontend    | Python 3 + Tkinter      |
| Backend     | SWI-Prolog (CLPFD)      |
| Integration | Python `subprocess`     |

---

## 📂 Project Structure


---

## ⚙️ Requirements

- [Python 3.x](https://www.python.org/downloads/)
- [SWI-Prolog](https://www.swi-prolog.org/Download.html)

> Make sure `swipl` is added to your system PATH after installation.

---

## ▶️ How to Run

```bash
# Step 1: Clone the repository
git clone https://github.com/your-username/sudoku-solver.git

# Step 2: Navigate into the folder
cd sudoku-solver

# Step 3: Run the application
python sudoku_gui.py
```

---

## 🧠 How It Works
1. **Input** — User fills in known cells; empty cells are left blank
2. **Validation** — Checks for invalid characters and duplicate values
3. **Conversion** — Grid is formatted for Prolog: `["5","","3"]` → `[5,_,3]`
4. **Solving** — Prolog applies constraints (unique rows, columns, 3×3 boxes) and uses `labeling/2` for backtracking
5. **Output** — Solution is passed back to Python and displayed; solver-filled cells are highlighted

---

## 🎯 Example

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| **A** | 5 | 3 | _ | _ | 7 | _ | _ | _ | _ |
| **B** | 6 | _ | _ | 1 | 9 | 5 | _ | _ | _ |
| **C** | _ | 9 | 8 | _ | _ | _ | _ | 6 | _ |

**Solved Output:**

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| **A** | 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| **B** | 6 | 7 | 2 | 1 | 9 | 5 | 3 | 4 | 8 |
| **C** | 1 | 9 | 8 | 3 | 4 | 2 | 5 | 6 | 7 |

---

## ❗ Error Handling

| Scenario | Behavior |
|---|---|
| Non-numeric input | Error popup shown |
| Duplicate in row/column/box | Exact location reported |
| Unsolvable puzzle | "No solution found" message |

---

## 📌 Key Functions

### 🐍 Python — `sudoku_gui.py`

| Function | Description |
|---|---|
| `solve_sudoku()` | Triggers the solve process |
| `get_grid()` | Reads current grid values |
| `run_solver()` | Calls the Prolog backend via subprocess |
| `fill_solution()` | Renders the solution on the GUI |

### 📐 Prolog — `sudoku_solver.pl`

| Predicate | Description |
|---|---|
| `sudoku9/1` | Defines all CLPFD constraints |
| `blocks/3` | Validates 3×3 box uniqueness |
| `labeling/2` | Backtracking search for solution |

---

## 👤 Made By
Uday Gangal

Shikhar Misra

vanshika rajput

Lakshay Saini

---
---

⭐ If you found this helpful, give it a star on GitHub!
