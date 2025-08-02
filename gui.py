import tkinter as tk
import sys, os, random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rubiks_solver import RubiksCube

COLOR_MAP = {
    'W': 'white',
    'Y': 'yellow',
    'R': 'red',
    'G': 'green',
    'B': 'blue',
    'O': 'orange'
}

class CubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Simulator")

        self.canvas = tk.Canvas(root, width=700, height=500, bg="lightgray")
        self.canvas.pack()

        self.cube = RubiksCube()
        self.scramble_moves = []

        self.create_buttons()
        self.create_log_window()
        self.draw_cube()

    def create_buttons(self):
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5)

        tk.Button(frame1, text="Scramble", command=self.scramble, bg="orange").grid(row=0, column=0, padx=5)
        tk.Button(frame1, text="Solve", command=self.solve, bg="lightgreen").grid(row=0, column=1, padx=5)
        tk.Button(frame1, text="Reset", command=self.reset_cube, bg="lightblue").grid(row=0, column=2, padx=5)

        frame2 = tk.LabelFrame(self.root, text="Manual Moves")
        frame2.pack(pady=5)

        moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

        for i, move in enumerate(moves):
            tk.Button(frame2, text=move, width=4,
                      command=lambda m=move: self.manual_move(m)).grid(
                row=i // 6, column=i % 6, padx=3, pady=3)

    def create_log_window(self):
        self.log_box = tk.Text(self.root, height=8, width=80, bg="black", fg="white")
        self.log_box.pack(pady=5)
        self.log("GUI Initialized.")

    def log(self, message):
        # Print to console
        print(message)
        # Add to log box
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def scramble(self):
        moves_list = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        random_scramble = random.choices(moves_list, k=10)

        for m in random_scramble:
            self.apply_move_by_name(m)

        self.scramble_moves.extend(random_scramble)
        self.log("Scramble: " + " ".join(random_scramble))

    def manual_move(self, move):
        self.apply_move_by_name(move)
        self.scramble_moves.append(move)
        self.log(f"Manual Move: {move}")

    def solve(self):
        if not self.scramble_moves:
            self.log("Nothing to solve.")
            return

        reverse_moves = self.invert_moves(self.scramble_moves)
        self.log("Solution path: " + " ".join(reverse_moves))
        self.animate_solution(reverse_moves)

        self.scramble_moves = []

    def invert_moves(self, moves):
        inv = []
        for m in reversed(moves):
            if "'" in m:
                inv.append(m.replace("'", ""))
            elif "2" in m:
                inv.append(m)
            else:
                inv.append(m + "'")
        return inv

    def animate_solution(self, moves, index=0):
        if index < len(moves):
            self.apply_move_by_name(moves[index])
            self.root.after(500, self.animate_solution, moves, index + 1)

    def apply_move_by_name(self, move):
        move_map = {
            "U": self.cube.move_U, "U'": self.cube.move_U_prime,
            "D": self.cube.move_D, "D'": self.cube.move_D_prime,
            "L": self.cube.move_L, "L'": self.cube.move_L_prime,
            "R": self.cube.move_R, "R'": self.cube.move_R_prime,
            "F": self.cube.move_F, "F'": self.cube.move_F_prime,
            "B": self.cube.move_B, "B'": self.cube.move_B_prime
        }
        if move in move_map:
            move_map[move]()
            self.draw_cube()

    def draw_face(self, stickers, x, y, size=30):
        for i, sticker in enumerate(stickers):
            row, col = divmod(i, 3)
            color = COLOR_MAP.get(sticker, "black")
            self.canvas.create_rectangle(
                x + col * size, y + row * size,
                x + (col + 1) * size, y + (row + 1) * size,
                fill=color, outline="black"
            )

    def draw_cube(self):
        self.canvas.delete("all")
        size = 30
        ox, oy = 100, 50
        self.draw_face(self.cube.faces['U'], ox + size*3, oy, size)
        self.draw_face(self.cube.faces['L'], ox, oy + size*3, size)
        self.draw_face(self.cube.faces['F'], ox + size*3, oy + size*3, size)
        self.draw_face(self.cube.faces['R'], ox + size*6, oy + size*3, size)
        self.draw_face(self.cube.faces['B'], ox + size*9, oy + size*3, size)
        self.draw_face(self.cube.faces['D'], ox + size*3, oy + size*6, size)

    def reset_cube(self):
        self.cube.reset()
        self.scramble_moves = []
        self.draw_cube()
        self.log("Cube reset.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CubeGUI(root)
    root.mainloop()
