import numpy as np
import math as m
import tkinter as tk
file_name = "VCAM/coords.txt"
cubes_file = "VCAM/new_coords.txt"
EDGES = np.ones(shape=(48,6))
CENTER = 350.0
CUBE = np.ones(shape=(32, 4))
NUM = np.ones(shape=(12, 2))

def projection(x, y, z):
   r = 0.0008
   matrix_2d = np.array([[x/(r*z +1), y/(r*z +1)]])
   return matrix_2d

class App(tk.Tk):
       def __init__(self):
              super().__init__()
              self.canv = tk.Canvas(self, bg = 'white')
              self.canv["width"] = 700
              self.canv["height"] = 700
              self.canv.focus_set()
              # self.draw()
              self.draw_cubes()
              self.canv.bind("<Up>", self.process_movements)
              self.canv.bind("<Down>", self.process_movements)
              self.canv.bind("<Right>", self.process_movements)
              self.canv.bind("<Left>", self.process_movements)
              self.canv.bind("0", self.process_movements)
              self.canv.bind("9", self.process_movements)
              self.canv.bind("+", self.process_zoom)
              self.canv.bind("-", self.process_zoom)
              self.canv.bind("w", self.process_rotation)
              self.canv.bind("s", self.process_rotation)
              self.canv.bind("a", self.process_rotation)
              self.canv.bind("d", self.process_rotation)
              self.canv.pack()

       def draw(self):
              for edge in EDGES:
                     coords_1 = projection(edge[0], edge[1], edge[2])
                     coords_2 = projection(edge[3], edge[4], edge[5])
                     side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])
       
       def draw_cubes(self):
              for n in NUM:
                     first, second = int(n[0]), int(n[1])
                     for n in range (4):
                            coords_1 = projection(CUBE[first][0], CUBE[first][1], CUBE[first][2])
                            coords_2 = projection(CUBE[second][0], CUBE[second][1], CUBE[second][2])
                            side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])
                            first += 8
                            second += 8

       def update_drawing(self):
              all_items = self.canv.delete("all")
              for n in NUM:
                     first, second = int(n[0]), int(n[1])
                     for n in range (4):
                            coords_1 = projection(CUBE[first][0], CUBE[first][1], CUBE[first][2])
                            coords_2 = projection(CUBE[second][0], CUBE[second][1], CUBE[second][2])
                            side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])
                            self.canv.itemconfig(side, fill='green', width=2)
                            first += 8
                            second += 8


       def process_movements(self, event):
              MOVE_X = 0
              MOVE_Y = 0
              MOVE_Z = 0
              if event.keysym == 'Up':
                     MOVE_Y = 10
              if event.keysym == 'Down':
                     MOVE_Y =-10
              if event.keysym == 'Right':
                     MOVE_X =-10
              if event.keysym == 'Left':
                     MOVE_X = 10
              if event.keysym == '0':
                     MOVE_Z =-10
              if event.keysym == '9':
                     MOVE_Z = 10

              move_matrix = np.eye(4)
              move_matrix[0:3, 3] = MOVE_X, MOVE_Y, MOVE_Z
              for point in range (32):
                     CUBE[point, :] = move_matrix.dot(CUBE[point, :])

              self.update_drawing()

       def process_zoom(self, event):
              SX, SY, SZ = 0, 0, 0
              if event.keysym == 'plus':
                     SX, SY, SZ = 1.3, 1.3, 1.3
              if event.keysym == 'minus':
                     SX, SY, SZ = 0.9, 0.9, 0.9
              zoom_matrix = np.array([[SX, 0, 0, 0], [0, SY, 0, 0], [0, 0, SZ, 0], [0, 0, 0, 1]])
              for point in range (32):
                     CUBE[point, :] = zoom_matrix.dot(CUBE[point, :])

              self.update_drawing()

       def process_rotation(self, event):
              axis = 'x'
              angle = (7*m.pi)/180
              if event.keysym == 's':
                     axis = 'y'
              if event.keysym == 'w':
                     angle = angle * (-1)
                     axis = 'y'
              if event.keysym == 'd':
                      angle = angle * (-1)
              if axis == 'y':
                     rotate_matrix = np.array([[1, 0, 0, 0], [0, m.cos(angle), -m.sin(angle), 0], [0, m.sin(angle), m.cos(angle), 0], [0, 0, 0, 1]])
              if axis == 'x':
                     rotate_matrix = np.array([[m.cos(angle), 0, m.sin(angle), 0], [0, 1, 0, 0], [-m.sin(angle), 0, m.cos(angle), 0], [0, 0, 0, 1]])
              for point in range (32):
                     CUBE[point, :] = rotate_matrix.dot(CUBE[point, :])

              self.update_drawing()

def read_data(file_name):
       f = open(file_name, "r")
       mod = 3
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              x1, y1, z1, x2, y2, z2 = float(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])
              EDGES[n,:] = (x1, y1, z1, x2, y2, z2)


def read_cubes(file_name):
       f = open(file_name, "r")
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              if n < 32:
                     CUBE[n,:3] = float(line[0]), float(line[1]), float(line[2])
              else:
                     NUM[n-32,:] = int(line[0]), int(line[1])             



if __name__ == "__main__":
       read_cubes(cubes_file)
       #read_data(file_name)
       app = App()
       app.title("Grafika komputerowa")
       app.mainloop()