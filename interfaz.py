import tkinter as tk

class NonogramApp:
    def __init__(self, master, sizeN,sizeM, row_clues, col_clues):
        self.master = master
        self.sizeN = sizeN
        self.sizeM = sizeM
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.board = [[0 for _ in range(sizeN)] for _ in range(sizeM)]

        self.setup_ui()

    def setup_ui(self):
        # Setup grid
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack()

        # Draw column clues
        max_clue_length = max(len(clue) for clue in self.col_clues)
        for i, clue in enumerate(self.col_clues):
            for j, (num, color) in enumerate(clue):
                label = tk.Label(
                    self.grid_frame, 
                    text=num if num != 0 else ' ', 
                    font=('TkDefaultFont', 10, 'bold'),
                    fg=self.get_color(color)
                )
                label.grid(row=j, column=i + max_clue_length)

        # Draw row clues
        max_row_clue_length = max(len(clue) for clue in self.row_clues)
        for i, clue in enumerate(self.row_clues):
            for j, (num, color) in enumerate(clue):
                label = tk.Label(
                    self.grid_frame, 
                    text=num if num != 0 else ' ', 
                    font=('TkDefaultFont', 10, 'bold'),
                    fg=self.get_color(color)
                )
                label.grid(row=i + max_row_clue_length, column=j)

        # Draw the grid
        self.cells = []
        for i in range(self.sizeN):
            row = []
            for j in range(self.sizeM):
                cell = tk.Canvas(self.grid_frame, width=20, height=20, bg='white', highlightbackground='black')
                cell.grid(row=i + max_row_clue_length, column=j + max_clue_length)
                row.append(cell)
            self.cells.append(row)

    def update_board(self, new_board):
        if len(new_board) == self.sizeN and all(len(row) == self.sizeM for row in new_board):
            self.board = new_board
            self.redraw_board()
        else:
            print("Error: La matriz no coincide con el tamaño del tablero.")

    def redraw_board(self):
        for i in range(self.sizeN):
            for j in range(self.sizeM):
                color = self.get_color(self.board[i][j])
                self.cells[i][j].config(bg=color)

    def get_color(self, value):
        color_map = {
            0: 'white',
            1: '#be0060',
            2: '#f4958f',
            3: '#000000',
            4: '#f0e8ba',
        }
        return color_map.get(value, 'white')
