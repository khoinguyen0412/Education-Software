from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import random
import datetime
import os

def print_vars():
    for value in vars:
        print(value.get())

def find_max_length_of_sublists(alist):
    if not alist:
        return None
    
    max_length = len(alist[0])
    for i in range(1, len(alist)):
        if max_length < len(alist[i]):
            max_length = len(alist)
    return max_length

def find_min_index(alist):
    if not alist:
        return None
    
    index = 0
    for i in range(len(alist)-1):
        if len(alist[i+1]) < len(alist[index]):
            index = i+1
    return index

def partition_names_into_groups(group_number, valid_names):
    use_names = valid_names[:]
    random.shuffle(use_names)

    number_per_group = int(len(use_names)/group_number)
    # fraction = (len(valid_names)/group_number) - number_per_group
    groups = []
    for i in range(group_number):
        group = []
        while len(group) < number_per_group and len(use_names) > 0:
            name = use_names.pop()
            group.append(name)
        groups.append(group)
    
    # for left over names, put them in groups with smallest size
    while len(use_names) > 0:
        index = find_min_index(groups) 
        groups[index].append(use_names.pop())

    return groups

class MainView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.font = ("Courier", 19)
        self.font_bold = ("Courier", 19, 'bold')
        self.roll_dir = './roll_by_day'

        # create top level menu
        self.menu_bar = Menu(self)

        # create file menus
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.choose_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        # add file menu to the menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.action_menu = Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label="Mark Roll", command=self.mark_roll)
        self.action_menu.add_command(label="Pair up", command=self.make_pairs)
        self.action_menu.add_command(label="Group up", command=self.make_groups)
        # add file menu to the menu bar
        self.menu_bar.add_cascade(label="Actions", menu=self.action_menu)

        self.name_list = []
        self.check_vars = []

        # p1 = Page1(self)
        # p2 = Page2(self)
        # p3 = Page3(self)
    
    def get_menubar(self):
        return self.menu_bar
    
    def make_groups(self):
        if len(self.name_list) > 0:
            group_number = simpledialog.askinteger(
                title='Group Number',
                prompt='Enter the number of groups', 
                parent=self)
            
            if group_number:
                valid_names = self.get_valid_names()
                groups = partition_names_into_groups(group_number, valid_names)
                # print(groups)

                number_of_columns = find_max_length_of_sublists(groups)
                pair_window = Toplevel()
                pair_window.title("Pairs")
                style = ttk.Style()
                style.configure('Frame1.TFrame', background="dark gray")
                frame = ttk.Frame(pair_window, style="Frame1.TFrame")
                frame.grid()

                ttk.Label(
                        frame, 
                        text="Group",
                        font=self.font_bold
                        ).grid(column=0, row=0,sticky=NSEW, padx=(3,3), pady=(5,5))
                
                for i in range(number_of_columns):
                    ttk.Label(
                        frame, 
                        text="Partner " + chr(65 + i) ,
                        font=self.font_bold
                        ).grid(column=i+1, row=0,sticky=NSEW, padx=(3,3), pady=(5,5))
                
                
                for row_number in range(len(groups)):
                    group = groups[row_number]
                    ttk.Label(
                        frame, 
                        text="Group " + str(row_number + 1),
                        font=self.font_bold
                        ).grid(column=0, row=row_number + 1,sticky=NSEW, padx=(3,3), pady=(5,5))
                    for column_number in range(len(group)):
                        member = group[column_number]
                        ttk.Label(
                            frame,
                            text=member,
                            font=self.font
                            ).grid(
                                column=column_number + 1,
                                row=row_number + 1,
                                sticky=NSEW, padx=(3,1), pady=(5,5))
                    
                    
    def make_pairs(self):
        valid_names = self.get_valid_names()
        random.shuffle(valid_names)
        if len(valid_names)  % 2 == 1:
            valid_names.append('<CHOOSE>')
        
        pairs = []
        for i in range(0, len(valid_names), 2):
            new_pair = [valid_names[i], valid_names[i+1]]
            pairs.append(new_pair)
        
        # disply pairs in a window
        pair_window = Toplevel()
        pair_window.title("Pairs")
        style = ttk.Style()
        style.configure('Frame1.TFrame', background="dark gray")
        frame = ttk.Frame(pair_window, style="Frame1.TFrame")
        frame.grid()

        ttk.Label(frame, text="Partner A", font=self.font_bold).grid(column=0, row=0,sticky=NSEW, padx=(3,3), pady=(5,5))
        ttk.Label(frame, text="Partner B", font=self.font_bold).grid(column=1, row=0, sticky=NSEW, padx=(3,3), pady=(5,5))

        i = 1
        for a,b in pairs:
            ttk.Label(frame, text=a, font=self.font).grid(column=0, row=i,sticky=NSEW, padx=(3,1), pady=(5,5))
            ttk.Label(frame, text=b, font=self.font).grid(column=1, row=i, sticky=NSEW, padx=(1,3), pady=(5,5))
            #print(a, b)
            i += 1


    def get_valid_names(self):
        valid_names = []
        for i in range(len(self.name_list)):
            check_value = self.check_vars[i].get()
            if check_value == 1:
                valid_names.append(self.name_list[i])
        return valid_names

    
    def mark_roll(self):
        if len(self.name_list) > 0:
            class_name = simpledialog.askstring(title='Roll', prompt='Enter class', parent=self)
            if class_name:
                today = datetime.date.today()
                date_string = str(today.strftime("%Y-%m-%d"))
                new_filename = class_name + '_' + date_string + '.txt'
                full_path = os.path.join(self.roll_dir, new_filename)
                valid_names = self.get_valid_names()
                with open(full_path, 'w') as f:
                    for name in valid_names:
                        f.write(name + '\n')

    
    def choose_file(self):
        filename = filedialog.askopenfilename(title='Open a file', initialdir='./')
        if filename:
            self.name_list = []
            with open(filename) as f:
                for line in f:
                    line = line.strip()
                    if len(line) > 0:
                        self.name_list.append(line)
            # add boxes for the items
            self.name_list.sort()
            self.populate_boxes()
    
    def populate_boxes(self):
        self.check_vars = []
        i = 0
        for name in self.name_list:
            column_number = i//5
            row_number = i % 5
            # create a var for this name and add it to the list
            var = IntVar()
            self.check_vars.append(var)
            Checkbutton(self, text=name, font=self.font, variable=var).grid(
                                                                    column=column_number,
                                                                    row=row_number,
                                                                    sticky=W)
            i += 1
        self.pack()
        
    
    def say_hi(self):
        print('hi')

def main():
    root = Tk()
    root.title("Class GUI")
    frame = MainView(root)
    frame.pack(side="top", fill="both", expand=True)
    # add menubar
    root.configure(menu=frame.get_menubar())
    # resize
    #root.geometry('800x500')
    root.mainloop()
    # root = Tk()
    # frm = ttk.Frame(root, padding=10)
    # frm.grid()
    # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)



    # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    # ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    # ttk.Label(frm, text="Hello World!").grid(column=0, row=1)
    # ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)
    # ttk.Label(frm, text="Hello World!").grid(column=0, row=2)
    # ttk.Button(frm, text="Print", command=print_vars).grid(column=1, row=2)

    # var1 = IntVar()
    # vars.append(var1)

    # Checkbutton(frm, text="male", variable=var1).grid(row=3, sticky=W)
    # var2 = IntVar()
    # vars.append(var2)

    # Checkbutton(frm, text="female", variable=var2).grid(row=4, sticky=W)
    # root.mainloop()

main()