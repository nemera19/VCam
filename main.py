import numpy as np
import math as m
import tkinter as tk
file_name = "coords.txt"
EDGES = np.ones(shape=(48,6))
CUBE_1 = np.zeros(shape=(8,4))
CUBE_2 = np.zeros(shape=(8,4))
CUBE_3 = np.zeros(shape=(8,4))
CUBE_4 = np.zeros(shape=(8,4))

def projection(x, y, z):
   r = 0.0001
   matrix_2d = np.array([[x/(r*z +1), y/(r*z +1)]])
   return matrix_2d

class App(tk.Tk):
       def __init__(self):
              super().__init__()
              self.canv = tk.Canvas(self, bg = 'white')
              self.canv["width"] = 800
              self.canv["height"] = 700
              self.canv.focus_set()
              self.draw()
              self.canv.bind("<Up>", self.process_movements)
              self.canv.bind("<Down>", self.process_movements)
              self.canv.bind("<Right>", self.process_movements)
              self.canv.bind("<Left>", self.process_movements)
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


       def update_drawing(self):
              all_items = self.canv.find_all()
              for n, item in enumerate(all_items):
                     #self.canv.itemconfig(item, fill='green', width=2)
                     coords_1 = projection(EDGES[n][0], EDGES[n][1], EDGES[n][2])
                     coords_2 = projection(EDGES[n][3], EDGES[n][4], EDGES[n][5])
                     self.canv.coords(item, coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1]) 


       def process_movements(self, event):
              global EDGES
              MOVE_X = 0
              MOVE_Y = 0
              if event.keysym == 'Up':
                     MOVE_Y = 2
              if event.keysym == 'Down':
                     MOVE_Y =-2
              if event.keysym == 'Right':
                     MOVE_X =-2
              if event.keysym == 'Left':
                     MOVE_X = 2
              move_matrix = np.array([MOVE_X, MOVE_Y, 0, MOVE_X, MOVE_Y, 0])
              EDGES+=move_matrix
              self.update_drawing()

       def process_zoom(self, event):
              global EDGES
              SX, SY, SZ = 0, 0, 0
              if event.keysym == 'plus':
                     SX, SY, SZ = 0.8, 0.8, 0.8
              if event.keysym == 'minus':
                     SX, SY, SZ = 1.2, 1.2, 1.2
              zoom_matrix = np.array([SX, SY, SZ, SX, SY, SZ])
              EDGES = EDGES / SX
              self.update_drawing()

       def process_rotation(self, event):
              axis = 'x'
              angle = (10*m.pi)/180
              if event.keysym == 'w':
                     axis = 'y'
              if event.keysym == 's':
                     angle = angle * (-1)
                     axis = 'y'
              if event.keysym == 'a':
                      angle = angle * (-1)
              if axis == 'y':
                     zoom_matrix = np.array([[1, 0, 0, 0], [0, m.cos(angle), -m.sin(angle), 0], [0, m.sin(angle), m.cos(angle), 0], [0, 0, 0, 1]])
              if axis == 'x':
                     zoom_matrix = np.array([[m.cos(angle), 0, m.sin(angle), 0], [0, 1, 0, 0], [-m.sin(angle), 0, m.cos(angle), 0], [0, 0, 0, 1]])

              for edge in EDGES:
                     xyz = np.ones(shape=(1, 4))
                     xyz2 = np.ones(shape=(1, 4))
                     xyz[0][0], xyz[0][1], xyz[0][2] = edge[0], edge[1], edge[2]
                     xyz2[0][0], xyz2[0][1], xyz2[0][2] = edge[3], edge[4], edge[5]
                     xyz = xyz.dot(zoom_matrix)
                     xyz2 = xyz2.dot(zoom_matrix)
                     edge[0:6] = xyz[0][0], xyz[0][1], xyz[0][2], xyz2[0][0], xyz2[0][1], xyz2[0][2]

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
       for n,line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              CUBE_1[n,:] = float(line[0]), float(line[1]), float(line[2]), 1


if __name__ == "__main__":
       read_data(file_name)
       app = App()
       app.title("Grafika komputerowa")
       app.mainloop()