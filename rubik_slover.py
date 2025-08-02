import tkinter as tk
from tkinter import messagebox

try:
    import kociemba
    kociemba_available = True
except ImportError:
    kociemba_available = False

# 🔴 Color Configurations
COLORS = ['W', 'Y', 'R', 'O', 'G', 'B']
COLOR_MAP = {
    'W': 'white', 'Y': 'yellow',
    'R': 'red', 'O': 'orange',
    'G': 'green', 'B': 'blue'
}
FACES = ['U', 'R', 'F', 'D', 'L', 'B']
DEFAULT_COLORS = {
    'U': 'W', 'D': 'Y', 'F': 'R',
    'B': 'O', 'L': 'G', 'R': 'B'
}

class CubeInput(tk.Frame):
    def __init__(self, master, face_name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.face_name = face_name
        self.cells = [[None for _ in range(3)] for _ in range(3)]
        default_color = DEFAULT_COLORS[face_name]

        tk.Label(self, text=f"{face_name} Face", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self, text=default_color, width=4, height=2,
                                bg=COLOR_MAP[default_color],
                                command=lambda i=i, j=j: self.cycle_color(i, j))
                btn.grid(row=i+1, column=j)
                self.cells[i][j] = btn

    def cycle_color(self, i, j):
        current = self.cells[i][j]['text']
        idx = COLORS.index(current)
        new = COLORS[(idx + 1) % len(COLORS)]
        self.cells[i][j]['text'] = new
        self.cells[i][j]['bg'] = COLOR_MAP[new]

    def get_data(self):
        return [[self.cells[i][j]['text'] for j in range(3)] for i in range(3)]

    def reset(self):
        default_color = DEFAULT_COLORS[self.face_name]
        for i in range(3):
            for j in range(3):
                self.cells[i][j]['text'] = default_color
                self.cells[i][j]['bg'] = COLOR_MAP[default_color]

class RubiksCubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver - GUI Edition")
        self.face_widgets = {}
        self.create_ui()

    def create_ui(self):
        layout = {
            'U': (0, 1), 'L': (1, 0), 'F': (1, 1),
            'R': (1, 2), 'B': (1, 3), 'D': (2, 1)
        }
        for face, (r, c) in layout.items():
            frame = CubeInput(self.root, face)
            frame.grid(row=r, column=c, padx=10, pady=10)
            self.face_widgets[face] = frame

        self.solve_btn = tk.Button(self.root, text="Solve Cube", font=("Arial", 12, "bold"), command=self.solve)
        self.solve_btn.grid(row=3, column=1, columnspan=2, pady=10)

        self.reset_btn = tk.Button(self.root, text="Reset Cube", font=("Arial", 10), command=self.reset_cube)
        self.reset_btn.grid(row=3, column=0, pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"), fg="blue")
        self.result_label.grid(row=4, column=0, columnspan=4)

    def get_cube_state(self):
        return {face: self.face_widgets[face].get_data() for face in FACES}

    def validate(self, state):
        color_count = {c: 0 for c in COLORS}
        for face, grid in state.items():
            if len(grid) != 3 or any(len(row) != 3 for row in grid):
                return False, f"Face '{face}' is not 3x3."
            for row in grid:
                for sticker in row:
                    if sticker not in COLORS:
                        return False, f"Invalid color '{sticker}' in face '{face}'"
                    color_count[sticker] += 1
        for c, count in color_count.items():
            if count != 9:
                return False, f"Color '{c}' has {count} stickers. Expected 9."
        return True, None

    def state_to_kociemba_string(self, state):
        face_centers = {state[face][1][1]: face for face in FACES}
        facelet_string = ''
        for face in FACES:
            for row in state[face]:
                for sticker in row:
                    if sticker not in face_centers:
                        raise ValueError(f"Sticker color '{sticker}' doesn't match any center face color.")
                    facelet_string += face_centers[sticker]
        return facelet_string

    def solve(self):
        state = self.get_cube_state()
        valid, err = self.validate(state)
        if not valid:
            messagebox.showerror("Validation Error", err)
            return
        if not kociemba_available:
            messagebox.showerror("Missing Library", "Install the `kociemba` library:\npip install kociemba")
            return
        try:
            cube_str = self.state_to_kociemba_string(state)
            solved_cube = ''.join(face * 9 for face in FACES)
            if cube_str == solved_cube:
                self.result_label.config(text="Cube is already solved ✅")
                return
            solution = kociemba.solve(cube_str)
            self.result_label.config(text=f"Solution: {solution}")
        except ValueError as ve:
            messagebox.showerror("Color Mapping Error", str(ve))
        except Exception as e:
            messagebox.showerror("Solve Error", str(e))

    def reset_cube(self):
        for frame in self.face_widgets.values():
            frame.reset()
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksCubeApp(root)
    root.mainloop()
