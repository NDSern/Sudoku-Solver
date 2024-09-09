import sudoku_solver
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk



class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Sudoku Solver")
        
        # Create the main Box of the application, every widgets will go under this
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Pinned window button
        pinButton = Gtk.CheckButton(label="Pin this Window")
        pinButton.connect("toggled", self.on_pinned_button_pressed)
        
        main_box.pack_start(pinButton, True, True, 0)
        
        # Creating a 9x9 grid for Sudoku inputs
        self.entries = []

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        for row in range(11):
            row_entries = []
            for col in range(11):
                if col in [3, 7]:
                    seperator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                    grid.attach(seperator, col, 0, 1, 11)
                    continue
                if row in [3, 7]:
                    seperator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                    grid.attach(seperator, 0, row, 11, 1)
                    continue
                entry = Gtk.Entry()
                entry.set_width_chars(1)
                grid.attach(entry, col, row, 1, 1)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        main_box.pack_start(grid, True, True, 0)
        
        # Solve Button. Get the inputs, and called the solve function.
        solveButton = Gtk.Button(label="Solve")
        solveButton.connect("clicked", self.on_solve_button_pressed)
        
        main_box.pack_start(solveButton, True, True, 0)
        
        # Clear Board button
        clearBoardButton = Gtk.Button(label="Clear Board")
        clearBoardButton.connect("clicked", self.on_clear_board_pressed)
        
        main_box.pack_start(clearBoardButton, True, True, 0)
        
        # Allow "<-" and "->" arrows key to be able to navigate the grid
        self.connect("key-press-event", self.on_keyboard_event)
        
        self.add(main_box)
        
        
    def on_pinned_button_pressed(self, button):
        if button.get_active():
            self.set_keep_above(True)
        else:
            self.set_keep_above(False)
        print("Pin pressed")
        
        
    def on_solve_button_pressed(self, button):
        # Default empty board
        board = []
        for row in range(11):
            new_column = []
            if row in [3, 7]:
                continue
            for col in range(9):
                cell_data = self.entries[row][col].get_text()
                if cell_data:
                    new_column.append(str(cell_data))
                else:
                    new_column.append(".")
            board.append(new_column)
        
        solve_status = sudoku_solver.SudokuSolver().solveSudoku(board)
        
        if not solve_status:
            print("unsolvable")
        else:
            print("solved")
            for row in range(11):
                if row in [3, 7]:
                    continue
                for col in range(9):
                    # 0 1 2 | 4 5 6 | 8 9 10
                    convert_to_board_row = row
                    if row in [4, 5, 6]:
                        convert_to_board_row = row - 1
                    if row in [8, 9, 10]:
                        convert_to_board_row = row - 2
                    cell_data = board[convert_to_board_row][col]
                    self.entries[row][col].set_text(cell_data)
                    
    
    def on_clear_board_pressed(self, button):
        for row in range(11):
            if row in [3, 7]:
                continue
            for col in range(9):
                self.entries[row][col].set_text("")
                
    
    def on_keyboard_event(self, widget, event):
        # Handle arrow key presses to navigate between widgets.
        focus_widget = self.get_focus()
        if focus_widget is None:
            return

        # Get the current position in the grid
        for i, row in enumerate(self.entries):
            if focus_widget in row:
                x, y = row.index(focus_widget), i
                break
        else:
            return
        

        # Move focus based on arrow key
        if event.keyval == Gdk.KEY_Left and x > 0:
            new_focus = self.entries[y][x - 1]
        elif event.keyval == Gdk.KEY_Right and x < len(self.entries[0]) - 1:
            new_focus = self.entries[y][x + 1]
        else:
            new_focus = None

        if new_focus:
            new_focus.grab_focus()



if __name__ == "__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()