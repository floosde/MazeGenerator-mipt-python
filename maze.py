import random
import json
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

EmptyCell = 0
FilledCell = 1
Wall = 2
Frontier = 3
Path = 4


def draw_rect(i, j, y_size, x_size, color):
    """
    Функция по переданным координатам, посчитанным размерам квадратика и цвету рисует на canvas клетку.
    """
    x1 = j * x_size
    y1 = (i * y_size)
    x2 = (j + 1) * x_size
    y2 = (i + 1) * y_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')


def init_array(real_height, real_width):
    """
    В силу невозможности использовать numpy-массивы, данная функция вынуждена инициализировать матрицу,
    заданнаго размера.
    """
    array = []
    for i in range(0, real_height):
        subarray = []
        for j in range(0, real_width):
            subarray.append(0)
        array.append(subarray)
    return array


class Maze:
    """
    Главный класс, который хранит в себе лабиринт.
    """

    def fill_cells(self):
        """
        Функция подготавливает матрицу для дальнейшего применения на неё генерирующий алгоритмов.
        Заполняет каждую клетку в соответсвии с её i, j.
        """
        for i in range(0, self.real_height):
            for j in range(0, self.real_width):
                if i < 1 or i == 2 * self.real_width or j < 1 or j == 2 * self.real_height:
                    self.cells[i][j] = Wall
                elif i % 2 == 1 and j % 2 == 1:
                    self.cells[i][j] = EmptyCell
                else:
                    self.cells[i][j] = Wall

    def __init__(self, height, width):
        """
        Инициализируются:
        1) curr_position - клетка, отвечающее за передвижение игрока во время игры.
        2) real_width и real_height - размеры, переданные как аргументы модуля преобразуются
        с учётом границы и стенок
        3) play_end - выход для игры
        4) cell_y_size и cell_x_size - размеры клетки рисования
        5) cells - массив, хранящий сам лабиринт
        Вызов fill_cells заполняет cells необходимыми для обработки значениями.
        """
        self.curr_position = (1, 1)
        self.real_width = 2 * width + 1
        self.real_height = 2 * height + 1
        self.play_end = (self.real_height - 2, self.real_width - 2)
        self.cell_y_size = 500 / self.real_height
        self.cell_x_size = 500 / self.real_width
        self.cells = init_array(self.real_height, self.real_width)
        self.fill_cells()

    def draw(self):
        """
        По значениям клеток в cells производится рисование всего лабиринта
        """
        for i in range(0, self.real_height):
            for j in range(0, self.real_width):
                if self.cells[i][j] == Wall:
                    draw_rect(i, j, self.cell_y_size, self.cell_x_size, 'black')
                elif self.cells[i][j] == Path:
                    draw_rect(i, j, self.cell_y_size, self.cell_x_size, 'red')

    def calculate_path(self):
        """
        Рекурсивный алгоритм поиска выхода.
        """
        path_stack = []
        self.cells[1][1] = Path
        curr_point = (1, 1)
        while curr_point[0] != self.real_height - 2 or curr_point[1] != self.real_width - 2:
            neighbours = []
            if self.cells[curr_point[0]][curr_point[1] + 1] == FilledCell:
                neighbours.append((curr_point[0], curr_point[1] + 1))
            if self.cells[curr_point[0]][curr_point[1] - 1] == FilledCell:
                neighbours.append((curr_point[0], curr_point[1] - 1))
            if self.cells[curr_point[0] + 1][curr_point[1]] == FilledCell:
                neighbours.append((curr_point[0] + 1, curr_point[1]))
            if self.cells[curr_point[0] - 1][curr_point[1]] == FilledCell:
                neighbours.append((curr_point[0] - 1, curr_point[1]))
            if len(neighbours) != 0:
                path_stack.append(curr_point)
                chosen_neigh = random.randrange(0, len(neighbours))
                curr_point = neighbours[chosen_neigh]
                self.cells[curr_point[0]][curr_point[1]] = Path
            elif path_stack != 0:
                self.cells[curr_point[0]][curr_point[1]] = EmptyCell
                curr_point = path_stack.pop()
                continue
            else:
                break


def recursive_backtracker(maze):
    """
    Генерации с помощью DFS
    """
    stack_of_cells = []
    curr_point = (1, 1)
    maze.cells[1][1] = FilledCell
    while True:
        neighbours = []
        if curr_point[1] + 2 < maze.real_width and maze.cells[curr_point[0]][curr_point[1] + 2] == EmptyCell:
            neighbours.append((curr_point[0], curr_point[1] + 2))
        if curr_point[1] - 2 > 0 and maze.cells[curr_point[0]][curr_point[1] - 2] == EmptyCell:
            neighbours.append((curr_point[0], curr_point[1] - 2))
        if curr_point[0] + 2 < maze.real_height and maze.cells[curr_point[0] + 2][curr_point[1]] == EmptyCell:
            neighbours.append((curr_point[0] + 2, curr_point[1]))
        if curr_point[0] - 2 > 0 and maze.cells[curr_point[0] - 2][curr_point[1]] == EmptyCell:
            neighbours.append((curr_point[0] - 2, curr_point[1]))
        if len(neighbours) != 0:
            stack_of_cells.append(curr_point)
            chosen_neigh = random.randrange(0, len(neighbours))
            next_point = neighbours[chosen_neigh]
            wall_point = ((curr_point[0] + next_point[0]) // 2, (curr_point[1] + next_point[1]) // 2)
            maze.cells[wall_point[0]][wall_point[1]] = FilledCell
            curr_point = next_point
            maze.cells[curr_point[0]][curr_point[1]] = FilledCell
        elif len(stack_of_cells) != 0:
            curr_point = stack_of_cells.pop()
            continue
        else:
            break


def prim(maze):
    """
    Генерация с помощью построения минимального остовного дерева (Алгоритм Прима)
    """
    frontiers = []
    in_maze = []
    rand_x = random.randint(0, maze.real_height - 2)
    rand_point_x = rand_x + (rand_x + 1) % 2
    rand_y = random.randint(0, maze.real_width - 2)
    rand_point_y = rand_y + (rand_y + 1) % 2
    maze.cells[rand_point_x][rand_point_y] = FilledCell
    in_maze.append((rand_point_x, rand_point_y))
    while len(frontiers) != 0 or len(in_maze) == 1:
        if in_maze[-1][1] + 2 < maze.real_width and maze.cells[in_maze[-1][0]][in_maze[-1][1] + 2] == EmptyCell:
            frontiers.append((in_maze[-1][0], in_maze[-1][1] + 2))
            maze.cells[in_maze[-1][0]][in_maze[-1][1] + 2] = Frontier
        if in_maze[-1][1] - 2 > 0 and maze.cells[in_maze[-1][0]][in_maze[-1][1] - 2] == EmptyCell:
            frontiers.append((in_maze[-1][0], in_maze[-1][1] - 2))
            maze.cells[in_maze[-1][0]][in_maze[-1][1] - 2] = Frontier
        if in_maze[-1][0] + 2 < maze.real_height and maze.cells[in_maze[-1][0] + 2][in_maze[-1][1]] == EmptyCell:
            frontiers.append((in_maze[-1][0] + 2, in_maze[-1][1]))
            maze.cells[in_maze[-1][0] + 2][in_maze[-1][1]] = Frontier
        if in_maze[-1][0] - 2 > 0 and maze.cells[in_maze[-1][0] - 2][in_maze[-1][1]] == EmptyCell:
            frontiers.append((in_maze[-1][0] - 2, in_maze[-1][1]))
            maze.cells[in_maze[-1][0] - 2][in_maze[-1][1]] = Frontier
        rand_frontier = random.randint(0, len(frontiers) - 1)
        chosen_frontier = frontiers[rand_frontier]
        maze.cells[chosen_frontier[0]][chosen_frontier[1]] = FilledCell
        in_maze.append((chosen_frontier[0], chosen_frontier[1]))
        neighbours = []
        if (chosen_frontier[0], chosen_frontier[1] + 2) in in_maze:
            neighbours.append((chosen_frontier[0], chosen_frontier[1] + 2))
        if (chosen_frontier[0], chosen_frontier[1] - 2) in in_maze:
            neighbours.append((chosen_frontier[0], chosen_frontier[1] - 2))
        if (chosen_frontier[0] + 2, chosen_frontier[1]) in in_maze:
            neighbours.append((chosen_frontier[0] + 2, chosen_frontier[1]))
        if (chosen_frontier[0] - 2, chosen_frontier[1]) in in_maze:
            neighbours.append((chosen_frontier[0] - 2, chosen_frontier[1]))
        rand_neigh = random.randrange(0, len(neighbours))
        neigh_point = (neighbours[rand_neigh][0], neighbours[rand_neigh][1])
        wall_point = ((chosen_frontier[0] + neigh_point[0]) // 2, (chosen_frontier[1] + neigh_point[1]) // 2)
        maze.cells[wall_point[0]][wall_point[1]] = FilledCell
        del frontiers[rand_frontier]


def afterplay_unbinding():
    """
    Отвязывание стрелочек после игры
    """
    root.unbind('<Left>')
    root.unbind('<Right>')
    root.unbind('<Up>')
    root.unbind('<Down>')


def path():
    """
    Функция запускает поиск пути, выводит результат на canvas, удаляет кнопки "Play" и "Path"
    и отвязывает кнопки после игры, если таковая была
    """
    root.maze.calculate_path()
    root.maze.draw()
    buttons_frame.nametowidget("path").destroy()
    buttons_frame.nametowidget("play").destroy()
    afterplay_unbinding()


def play_game():
    """
    Функция рисует игрока и выход из лабиринта, привязывает кнопки для игры
    """
    if root.maze.curr_position == (1, 1):
        draw_rect(1, 1, root.maze.cell_y_size, root.maze.cell_x_size, 'blue')
        end = root.maze.play_end
        draw_rect(end[0], end[1], root.maze.cell_y_size, root.maze.cell_x_size, 'orange')
    root.bind('<Left>', left_key)
    root.bind('<Right>', right_key)
    root.bind('<Up>', up_key)
    root.bind('<Down>', down_key)


def win_check():
    """
    Функция проверяет, если игрок дошёл до конца пути, выводит победное сообщение, отвязывает кнопки
    и удаляет клетку с выходом и игроком.
    """
    if root.maze.curr_position == root.maze.play_end:
        messagebox.showinfo("You did it!", "OMG YOU ARE MLG PRO!!!")
        afterplay_unbinding()
        draw_rect(root.maze.play_end[0], root.maze.play_end[1], root.maze.cell_y_size, root.maze.cell_x_size, 'white')
        root.maze.curr_position = (1, 1)


def left_key(event):
    """
    Обработка нажатия "Стрелочка влево"
    """
    curr_pos = root.maze.curr_position
    if root.maze.cells[curr_pos[0]][curr_pos[1] - 1] == FilledCell:
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'white')
        root.maze.curr_position = (curr_pos[0], curr_pos[1] - 1)
        curr_pos = root.maze.curr_position
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'blue')
    win_check()


def right_key(event):
    """
    Обработка нажатия "Стрелочка вправо"
    """
    curr_pos = root.maze.curr_position
    if root.maze.cells[curr_pos[0]][curr_pos[1] + 1] == FilledCell:
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'white')
        root.maze.curr_position = (curr_pos[0], curr_pos[1] + 1)
        curr_pos = root.maze.curr_position
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'blue')
    win_check()


def up_key(event):
    """
    Обработка нажатия "Стрелочка вверх"
    """
    curr_pos = root.maze.curr_position
    if root.maze.cells[curr_pos[0] - 1][curr_pos[1]] == FilledCell:
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'white')
        root.maze.curr_position = (curr_pos[0] - 1, curr_pos[1])
        curr_pos = root.maze.curr_position
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'blue')
    win_check()


def down_key(event):
    """
    Обработка нажатия "Стрелочка вниз"
    """
    curr_pos = root.maze.curr_position
    if root.maze.cells[curr_pos[0] + 1][curr_pos[1]] == FilledCell:
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'white')
        root.maze.curr_position = (curr_pos[0] + 1, curr_pos[1])
        curr_pos = root.maze.curr_position
        draw_rect(curr_pos[0], curr_pos[1], root.maze.cell_y_size, root.maze.cell_x_size, 'blue')
    win_check()


def copy_maze_for_save():
    """
    Функция сохраняет изначальное состояние лабиринта, после генерации для сохранения
    """
    root.original_cells = []
    for i in root.maze.cells:
        root.original_cells.append(i[:])


def generate_maze():
    """
    Функция производит генерацию лабиринта:
    предварительно отвязывает кнопки, если была игра, стирает старый лабиринт,
    генерирует новую матрицу и сохраняет как объект граф. интерфейса,
    производится генерация по выбранному алгоритму,
    создаются неободимые кнопки и лабиринт выводится на экран
    """
    afterplay_unbinding()
    canvas.delete("all")
    root.maze = Maze(root.args.height, root.args.width)
    if root.args.mode == 'Prim':
        prim(root.maze)
    elif root.args.mode == 'Recursive':
        recursive_backtracker(root.maze)
    copy_maze_for_save()
    path_start = Button(buttons_frame, name="path", text="Calculate Path", padx=20, command=lambda: path())
    path_start.grid(row=0, column=1)
    save_button = Button(buttons_frame, name="save", text="Save as file", padx=20, command=save_file)
    save_button.grid(row=0, column=5)
    play = Button(buttons_frame, name="play", text="Play", padx=20, command=lambda: play_game())
    play.grid(row=0, column=2)
    root.maze.draw()


def open_file():
    """
    Функция читает из файла типа txt лабиринт в виде "[[...]...[...]]",
    который потом преобразуется в list и сохраняется в cells
    """
    root.filename = filedialog.askopenfilename(title="Select a file")
    if root.filename and str(root.filename).endswith(".txt"):
        file = open(root.filename, 'r')
        root.maze.cells = json.loads(file.read())
        file.close()
        canvas.delete("all")
        root.maze.draw()


def save_file():
    """
    Функция сохраняет лабиринт в txt файле виде "[[...]...[...]]",
    который потом можно открыть при помощи кнопки "Open from file"
    """
    text_file = filedialog.asksaveasfilename(defaultextension=".txt", title="Save file",
                                             filetypes=(("txt", "*.txt"), ("All files", "*.*")))
    if text_file:
        text_file = open(text_file, 'w+')
        text_file.write(str(root.original_cells))


def init_args(args):
    root.args = args

"""
Создаются необходимые элементы графического интерфейса.
"""

root = Tk()
root.title("Maze Generator")
root.resizable(False, False)

canvas_width = 500
canvas_height = 500

canvas = Canvas(root, name="canvas", width=canvas_width, height=canvas_height, bg="white")
canvas.grid(row=1, column=0)

buttons_frame = Frame(root)
buttons_frame.grid(row=0, column=0)

gen_start = Button(buttons_frame, text="Generate Maze", padx=20, command=generate_maze)
gen_start.grid(row=0, column=0)

open_button = Button(buttons_frame, text="Open from file", padx=20, command=open_file)
open_button.grid(row=0, column=4)