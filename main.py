import argparse
import maze

"""
Происходит обработка аргументов, переданных в модуль.
"""

parser = argparse.ArgumentParser()
parser.add_argument('mode', type=str)
parser.add_argument('height', type=int)
parser.add_argument('width', type=int)
args = parser.parse_args()

maze.init_args(args)

maze.canvas.mainloop()
