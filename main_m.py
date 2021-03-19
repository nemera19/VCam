import numpy as np
import math as m
import tkinter as tk
file_name = "coords.txt"
edges = np.ones(shape=(48,6))

def projection(x, y, z):
   r = 0.0001
   matrix_2d = np.array([[x/(r*z +1), y/(r*z +1)]])
   return matrix_2d

class App(tk.Tk):
       def __init__(self):
              super().__init__()
              self.canv = tk.Canvas(self, bg = 'white')
              self.canv["width"] = 700
              self.canv["height"] = 600
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
              for edge in edges:
                     coords_1 = projection(edge[0], edge[1], edge[2])
                     coords_2 = projection(edge[3], edge[4], edge[5])
                     side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])


       def update_drawing(self):
              all_items = self.canv.find_all()
              for n, item in enumerate(all_items):
                     self.canv.itemconfig(item, fill='green', width=2)
                     coords_1 = projection(edges[n][0], edges[n][1], edges[n][2])
                     coords_2 = projection(edges[n][3], edges[n][4], edges[n][5])
                     self.canv.coords(item, coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1]) 


       def process_movements(self, event):
              global edges
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
              edges+=move_matrix
              self.update_drawing()

       def process_zoom(self, event):
              global edges
              SX, SY, SZ = 0, 0, 0
              if event.keysym == 'plus':
                     SX, SY, SZ = 0.8, 0.8, 0.8
              if event.keysym == 'minus':
                     SX, SY, SZ = 1.2, 1.2, 1.2
              zoom_matrix = np.array([SX, SY, SZ, SX, SY, SZ])
              edges = edges / SX
              self.update_drawing()

       def process_rotation(self, event):
              global edges
              angle = (30*m.pi)/180
              SX, SY = 0, 0
              if event.keysym == 'w':
                     SX, SY = 1.2, 1.2
              if event.keysym == 's':
                     SX, SY = -1.2, -1.2
              if event.keysym == 'a':
                     SX, SY = 1.2, 1.2
              if event.keysym == 'd':
                     edges[:, [1,4]] = m.cos(angle)*edges[:, [1,4]] - m.sin(angle)*edges[:, 2]
                     edges[:, 4] = m.cos(angle)*edges[:, 4] - m.sin(angle)*edges[:, 5]
                     edges[:, 2] = m.sin(angle)*edges[:, 1] + m.cos(angle)*edges[:, 2]
                     edges[:, 4] = m.sin(angle)*edges[:, 4] + m.cos(angle)*edges[:, 5]
              self.update_drawing()

def read_data(file_name):
       global edges
       f = open(file_name, "r")
       mod = 3
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              x1, y1, z1, x2, y2, z2 = float(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])
              edges[n,:] = (x1, y1, z1, x2, y2, z2)

              
if __name__ == "__main__":
       read_data(file_name)
       app = App()
       app.title("Grafika komputerowa")
       app.mainloop()