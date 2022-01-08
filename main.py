import tkinter as tk
from random import shuffle
from typing import Any
from tkinter.messagebox import showinfo, showerror

colors={
    1:'#62a832',
    2:'#32a896',
    3:'#327da8',
    4:'#1f668f',
    5:'blue',
    6:'#6d32a8',
    7:'purple',
    8:'red'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton  {self.number} ( {self.x} : {self.y} ) - {self.is_mine}'


class Saper:
    window = tk.Tk()
    rows = 10
    columns = 10
    mines = 5
    is_game_over = False
    is_first_click = True

    def __init__(self):
        self.buttons = []

        for i in range(Saper.rows + 2):
            temp = []
            for j in range(Saper.columns + 2):
                btn = MyButton(Saper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)

            self.buttons.append(temp)
        print('Start game!')


    def right_click(self, event):
        if Saper.is_game_over:
            return None
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] == 'disabled'
            cur_btn['text'] = '🚩'
            #cur_btn['disabledforeground'] = 'green'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'


    def click(self, clicked_button: MyButton):
        print(clicked_button)
        if Saper.is_game_over:
            return None

        if Saper.is_first_click:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            Saper.is_first_click = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            Saper.is_game_over = True
            showinfo('Game over', 'You lost!!!')
            for i in range(1, Saper.rows + 1):
                for j in range(1, Saper.columns + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                #clicked_button.config(text='', disabledforeground=color)
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)


    def breadth_first_search(self, btn:MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        #if not abs(dx - dy) == 1:
                            #continue
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open\
                                and 1 <= next_btn.x <= Saper.rows\
                                and 1 <= next_btn.y <= Saper.columns\
                                and next_btn not in queue:
                            queue.append(next_btn)


    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        Saper.is_first_click = True
        Saper.is_game_over = False


    def change_set(self, row: tk.Entry, col: tk.Entry, bomb: tk.Entry):
        try:
            int(row.get()), int (col.get()), int (bomb.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение!')
            return


        Saper.rows = int(row.get())
        Saper.columns = int(col.get())
        Saper.mines = int(bomb.get())
        self.reload()


    def create_set_win(self):
        win_set = tk.Toplevel(self.window)
        win_set.wm_title('Настройки игры')
        tk.Label(win_set, text='Количество строк поля').grid(row=0, column=0)
        row_entry = tk.Entry(win_set)
        row_entry.insert(0, Saper.rows)
        row_entry.grid(row=0, column=1, padx=30, pady=30)
        tk.Label(win_set, text='Количество колонок поля').grid(row=1, column=0)
        col_entry = tk.Entry(win_set)
        col_entry.insert(0, Saper.columns)
        col_entry.grid(row=1, column=1, padx=30, pady=30)
        tk.Label(win_set, text='Количество мин на поле').grid(row=2, column=0)
        bomb_entry = tk.Entry(win_set)
        bomb_entry.insert(0, Saper.mines)
        bomb_entry.grid(row=2, column=1, padx=30, pady=30)

        # кнопка Применить настройки
        save_set_btn = tk.Button(win_set, text='Применить настройки',
                  command=lambda :self.change_set(row_entry, col_entry, bomb_entry))
        save_set_btn.grid (row=3, column=0, columnspan=2, padx=30, pady=30)

    def create_about_win(self):
        win_about = tk.Toplevel(self.window)
        win_about.wm_title('О программе...')
        tk.Label(win_about, text='Программа: игра \"Сапер \"').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(win_about, text='Автор: Дьяченко Михаил').grid(row=1, column=0, padx=10, pady=10)
        tk.Label(win_about, text='2022').grid(row=1, column=0, padx=10, pady=10)
        ok_btn = tk.Button(win_about, text='ОК', command=win_about.destroy)
        ok_btn.grid (row=2, column=0, columnspan=1, padx=10, pady=10)

    def create_widgets(self):

        # Меню игры
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        set_menu = tk.Menu(menubar, tearoff=0)
        set_menu.add_command(label='Играть', command=self.reload)
        set_menu.add_command(label='Настройки', command=self.create_set_win)
        set_menu.add_command(label='О программе', command=self.create_about_win)
        set_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Меню', menu=set_menu)

        # Панель

        # Создание клеток
        count =1
        for i in range(1, Saper.rows + 1):
            for j in range(1, Saper.columns + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, Saper.rows + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, Saper.columns + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(Saper.rows + 2):
            for j in range(Saper.columns + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')

                elif btn.count_bomb in colors:
                    color=colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, foreground=color)
                else:
                    btn.config(text=btn.count_bomb, foreground='black')
                #btn.grid(row=i, column=j)

    def start(self):
        #self.open_all_buttons()
        self.create_widgets()
        Saper.window.mainloop()

    def print_buttons(self):
        for i in range(1, Saper.rows + 1):
            for j in range(1, Saper.columns + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, Saper.rows * Saper.columns))
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:Saper.mines]

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)

        for i in range(1, Saper.rows + 1):
            for j in range(1, Saper.columns + 1):
                btn = self.buttons[i][j]

                if btn.number in index_mines:
                    btn.is_mine = True


    def count_mines_in_buttons(self):
        for i in range(1, Saper.rows + 1):
            for j in range(1, Saper.columns + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in (-1, 0, 1):
                        for col_dx in (-1, 0, 1):
                            sosed = self.buttons[i + row_dx][j + col_dx]
                            if sosed.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb


game = Saper()
game.start()

