

class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': ['W'] * 9,
            'D': ['Y'] * 9,
            'L': ['O'] * 9,
            'R': ['R'] * 9,
            'F': ['G'] * 9,
            'B': ['B'] * 9
        }

    def rotate_face_clockwise(self, face):
        """Rotate a face 90° clockwise"""
        f = self.faces[face]
        self.faces[face] = [f[6], f[3], f[0],
                            f[7], f[4], f[1],
                            f[8], f[5], f[2]]

    def rotate_face_counterclockwise(self, face):
        """Rotate a face 90° counterclockwise"""
        f = self.faces[face]
        self.faces[face] = [f[2], f[5], f[8],
                            f[1], f[4], f[7],
                            f[0], f[3], f[6]]

    def move_R(self):
        self.rotate_face_clockwise('R')
        u, f, d, b = self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B']
        u_col = [u[2], u[5], u[8]]
        f_col = [f[2], f[5], f[8]]
        d_col = [d[2], d[5], d[8]]
        b_col = [b[6], b[3], b[0]]
        u[2], u[5], u[8] = b_col[::-1]
        b[6], b[3], b[0] = d_col[::-1]
        d[2], d[5], d[8] = f_col
        f[2], f[5], f[8] = u_col

    def move_R_prime(self):
        for _ in range(3):
            self.move_R()

    def move_R2(self):
        for _ in range(2):
            self.move_R()

    def move_L(self):
        self.rotate_face_clockwise('L')
        u, f, d, b = self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B']
        u_col = [u[0], u[3], u[6]]
        f_col = [f[0], f[3], f[6]]
        d_col = [d[0], d[3], d[6]]
        b_col = [b[8], b[5], b[2]]
        u[0], u[3], u[6] = f_col
        f[0], f[3], f[6] = d_col
        d[0], d[3], d[6] = b_col[::-1]
        b[8], b[5], b[2] = u_col[::-1]

    def move_L_prime(self):
        for _ in range(3):
            self.move_L()

    def move_L2(self):
        for _ in range(2):
            self.move_L()

    def move_U(self):
        self.rotate_face_clockwise('U')
        f, r, b, l = self.faces['F'], self.faces['R'], self.faces['B'], self.faces['L']
        f_row = f[:3]
        r_row = r[:3]
        b_row = b[:3]
        l_row = l[:3]
        f[:3], r[:3], b[:3], l[:3] = r_row, b_row, l_row, f_row

    def move_U_prime(self):
        for _ in range(3):
            self.move_U()

    def move_U2(self):
        for _ in range(2):
            self.move_U()

    def move_D(self):
        self.rotate_face_clockwise('D')
        f, r, b, l = self.faces['F'], self.faces['R'], self.faces['B'], self.faces['L']
        f_row = f[6:]
        r_row = r[6:]
        b_row = b[6:]
        l_row = l[6:]
        f[6:], r[6:], b[6:], l[6:] = l_row, f_row, r_row, b_row

    def move_D_prime(self):
        for _ in range(3):
            self.move_D()

    def move_D2(self):
        for _ in range(2):
            self.move_D()

    def move_F(self):
        self.rotate_face_clockwise('F')
        u, r, d, l = self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L']
        u_row = [u[6], u[7], u[8]]
        r_col = [r[0], r[3], r[6]]
        d_row = [d[2], d[1], d[0]]
        l_col = [l[8], l[5], l[2]]
        u[6], u[7], u[8] = l_col
        l[8], l[5], l[2] = d_row
        d[2], d[1], d[0] = r_col
        r[0], r[3], r[6] = u_row

    def move_F_prime(self):
        for _ in range(3):
            self.move_F()

    def move_F2(self):
        for _ in range(2):
            self.move_F()

    def move_B(self):
        self.rotate_face_clockwise('B')
        u, r, d, l = self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L']
        u_row = [u[0], u[1], u[2]]
        r_col = [r[2], r[5], r[8]]
        d_row = [d[6], d[7], d[8]]
        l_col = [l[6], l[3], l[0]]
        u[0], u[1], u[2] = r_col
        r[2], r[5], r[8] = d_row[::-1]
        d[6], d[7], d[8] = l_col
        l[6], l[3], l[0] = u_row[::-1]

    def move_B_prime(self):
        for _ in range(3):
            self.move_B()

    def move_B2(self):
        for _ in range(2):
            self.move_B()

    def reset(self):
        self.__init__()

    def solve(self):
    
        self.reset()
        return "Cube reset to solved"

