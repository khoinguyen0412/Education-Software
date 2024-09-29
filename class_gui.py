from tkinter import *
from tkinter import ttk,filedialog,simpledialog,messagebox
import random
import datetime
import os
import sqlite3
import csv
from functools import partial
import logging

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
        self.file_menu.add_command(label="Import Student List", command=self.import_file)
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


        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configuring the grid to expand and center elements
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Add a refresh button
        self.refresh_button = ttk.Button(self, text="Refresh", command=self.render_classes,padding=(3,5))
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Create a frame to hold the buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Center the button_frame within the parent
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)


        self.render_classes()

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
    
    def import_file(self):
        file_path = filedialog.askopenfilename(
        title="Select CSV File", 
        filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")] )

        if file_path:
            if file_path.lower().endswith(".csv") or file_path.lower().endswith(".txt"):
                self.__get_class_code(file_path)
            else:
                self.master.config(cursor="")
                messagebox.showerror("File Error", "The selected file is not supported. Please choose a valid CSV or TXT file.")

    def __process_file(self,filename:str,class_code):
        if filename.lower().endswith(".csv"):
            try:
                conn.execute("BEGIN")
                cur.execute("Insert INTO class (class_code) VALUES (?)", (class_code,))
                new_id = cur.lastrowid
                with open(filename, newline='', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        name = row[0]
                        if name:
                            cur.execute("Insert INTO students (name,class_id) VALUES (?,?)", (name,new_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "CSV data imported successfully!")
                    self.render_classes()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error when importing CSV file",e)
        else: 
            try:
                conn.execute("BEGIN")
                cur.execute("Insert INTO class (class_code) VALUES (?)", (class_code,))
                new_id = cur.lastrowid
                with open(filename) as f:
                    for line in f:
                        line = line.strip()
                        if len(line) > 0:
                            cur.execute("Insert INTO students (name,class_id) VALUES (?,?)", (line,new_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Text data imported successfully!")
                    self.render_classes()
            
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error when importing text file",e)
       
    def __get_class_code(self,filename):
        # root.config(cursor="watch")
        # root.update()
        modal = Toplevel(root)
        modal.title("Enter class code")
        modal.geometry("300x150")
        label = Label(modal, text="Enter the class code name", font=("Helvetica", 12))
        label.pack(pady=10)
        # root.config(cursor="")
        # root.update()
    
        # Entry field to capture user input
        user_input = Entry(modal, width=30)
        user_input.pack(pady=5)

        def on_submit():
            input_value = user_input.get()
            if input_value:
                modal.destroy()  # Close the modal
                self.__process_file(filename, input_value)  # Process the file with the additional value
            else:
                messagebox.showwarning("Input Error", "Please enter a value.")
    
        # Submit button
        submit_btn = Button(modal, text="Submit", command=on_submit)
        submit_btn.pack(pady=10)


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
        
    
    def render_classes(self):
        cur.execute("SELECT class_code FROM class")
        self.classes = cur.fetchall()

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        max_buttons_per_row = 4
        # Font size
        font_size = 12

        # Configure the style for buttons
        style = ttk.Style()
        style.configure('TButton', padding=(10, 30), font=('Arial', font_size))  # Padding affects the appearance of height

        # Configure the row and column configuration
        for col in range(max_buttons_per_row):
            self.button_frame.grid_columnconfigure(col, weight=1)

        num_rows = (len(self.classes) + max_buttons_per_row - 1) // max_buttons_per_row
        for row in range(num_rows):
            self.button_frame.grid_rowconfigure(row, weight=0)  # Set row weight to 0 to prevent expansion

        for index, item in enumerate(self.classes):
            button = ttk.Button(self.button_frame, text=item[0], style='TButton',command=partial(show_frame, "DetailClass", item[0]))
            button.bind("<Enter>", CursorUtility.on_enter)
            button.bind("<Leave>", CursorUtility.on_leave)

            # Use grid to arrange buttons in rows (one per row, centered)
            row = index // max_buttons_per_row
            col = index % max_buttons_per_row

            # Place button in the grid
            button.grid(row=row, column=col,rowspan=2 , padx=10, pady=10, sticky="nsew")
            
        # Update column configuration based on the maximum buttons per row
        for col in range(max_buttons_per_row):
            self.button_frame.grid_columnconfigure(col, weight=1)

        # Update row configuration
        # num_rows = (len(self.classes) + max_buttons_per_row - 1) // max_buttons_per_row
        # for row in range(num_rows):
        #     self.button_frame.grid_rowconfigure(row, weight=1)


class DetailClass(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

class CursorUtility:
    @staticmethod
    def on_enter(event):
        event.widget.config(cursor="hand2")

    @staticmethod
    def on_leave(event):
        event.widget.config(cursor="")

    def on_load(event):
        event.set_cursor(event.widget, "watch")

def show_frame(frame_name,*args):
    frame = frames[frame_name]

    frame.tkraise()


def main():
    global root
    global frames

    root = Tk()
    root.title("Class GUI")
    # frame = MainView(root)
    # frame.pack(side="top", fill="both", expand=True)

    frames = {}
    container = ttk.Frame(root)
    container.pack(side="top", fill="both", expand=True)

    # Initialize frames and add them to the container
    frames = {}
    frames["MainView"] = MainView(container)
    frames["GeneralPage"] = DetailClass(container)

    # Pack frames into the container (or grid)
    for frame in frames.values():
        frame.grid(row=0, column=0, sticky="nsew")

    # Configure the container to allow frames to expand
    container.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    container.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

    # Show the initial frame
    show_frame("MainView")
    
    # add menubar
    root.configure(menu=frames["MainView"].get_menubar())
    # Set the window size to screen size, but in windowed mode
    root.state("zoomed")
    # resize
    root.geometry('800x500')
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


def change_frame(frame_name, *args):
    pass

conn = sqlite3.connect("example.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NULL,
    class_id INTEGER NOT NULL
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_code TEXT NULL
)
""")
conn.commit()

if __name__ == "__main__":
    main()