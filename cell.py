from tkinter import Button, Label
from PIL import Image, ImageTk
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(location, width=12, height=4)
        btn.configure(width=12, height=4)
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn
        btn.grid(row=self.y, column=self.x)

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, bg='black', fg='white', text=f'Cells Left:{Cell.cell_count}',
                    font=("", 30))
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):  # Click Box
        self.cell_btn_object.configure(relief='sunken')
        if self.is_mine:
            self.show_mine()

        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You Won!", "Game Over", 0)

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [self.get_cell_by_axis(self.x - 1, self.y - 1), self.get_cell_by_axis(self.x - 1, self.y),
                 self.get_cell_by_axis(self.x - 1, self.y + 1), self.get_cell_by_axis(self.x, self.y - 1),
                 self.get_cell_by_axis(self.x + 1, self.y - 1), self.get_cell_by_axis(self.x + 1, self.y),
                 self.get_cell_by_axis(self.x + 1, self.y + 1), self.get_cell_by_axis(self.x, self.y + 1)]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def resize_image(self, image_path, width, height):  # new code begin
        image = Image.open(image_path)
        resize_image = image.resize((width, height))
        tk_image = ImageTk.PhotoImage(resize_image)
        return tk_image

    def show_cell(self):
        if not self.is_opened:

            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f'Cells Left:{Cell.cell_count}')
            self.cell_btn_object.configure(bg='SystemButtonFace')
        self.is_opened = True

    def show_mine(self):
        for cell in Cell.all:
            if cell.is_mine:
                cell.cell_btn_object.configure(bg='red')

        ctypes.windll.user32.MessageBoxW(0, "You CLicked on a Mine", "Game Over", 0)
        # sys.exit()

    '''
    def resize_image(self, image_path, width, height):  # new code begin
        image = Image.open(image_path)
        resize_image = image.resize((width, height))
        tk_image = ImageTk.PhotoImage(resize_image)
        return tk_image
    '''

    def right_click_actions(self, event):  # Flag
        if not self.is_mine_candidate:
            flag_image_path = "flags.png"
            desired_width = 55
            desired_height = 55
            resized_flag_image = self.resize_image(flag_image_path, desired_width, desired_height)
            self.flag_image = resized_flag_image
            self.cell_btn_object.configure(width=desired_width, height=desired_height)
            self.cell_btn_object.configure(bg='orange', image=resized_flag_image, relief='sunken')
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(width=12, height=4)
            self.cell_btn_object.configure(bg='SystemButtonFace', image='', relief='raised')
            self.cell_btn_object.image = None
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        print(picked_cells)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
