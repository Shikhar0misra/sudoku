:- use_module(library(clpfd)).

sudoku9(Rows) :-
    length(Rows, 9),
    maplist(same_length(Rows), Rows),

    append(Rows, Vs),
    Vs ins 1..9,

    maplist(all_distinct, Rows),

    transpose(Rows, Columns),
    maplist(all_distinct, Columns),

    blocks(Rows).

blocks([]).
blocks([A, B, C | Rest]) :-
    block_rows(A, B, C),
    blocks(Rest).

block_rows([], [], []).
block_rows([A, B, C | Rest1], [D, E, F | Rest2], [G, H, I | Rest3]) :-
    all_distinct([A, B, C, D, E, F, G, H, I]),
    block_rows(Rest1, Rest2, Rest3).

solve9(Puzzle) :-
    sudoku9(Puzzle),
    append(Puzzle, Vs),
    labeling([ff], Vs),
    print_sudoku(Puzzle).

print_sudoku([]).
print_sudoku([Row | Rest]) :-
    writeln(Row),
    print_sudoku(Rest).
