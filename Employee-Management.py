import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import csv
import mysql.connector


class AdminLogin:
    def __init__(self, main):
        self.main = main
        self.AUTHORIZED = False

    def login(self):
        if user_entry.get() == '':
            tkinter.messagebox.showerror("ERROR", "Username cannot be empty!")
        else:
            con = mysql.connector.connect(host='localhost', user='root', password='', database='employee-management')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userlogin')
            data = cursor.fetchall()
            for user in data:
                if (user_entry.get().capitalize() == user[0]) and (pass_entry.get() == user[1]):
                    self.AUTHORIZED = True
                    cursor.close()
                    con.close()
                    break
            else:
                ask_retry = tkinter.messagebox.askretrycancel("Wrong Credentials!",
                                                              "Username or Password is Incorrect!")
                if ask_retry:
                    user_value.set("")
                    pass_value.set("")
                    user_entry.update()
                    pass_entry.update()
                else:
                    self.main.destroy()

    def toggle(self, check, p_entry):
        if check:
            p_entry.configure(show='*')
        else:
            p_entry.configure(show='')

    def validate(self, *args):
        pass_ = args[0]
        btn = args[1]
        if len(pass_) >= 8:
            btn.configure(state='normal', background='orange')
        else:
            btn.configure(state='disabled', background='grey')


class AdminPanel:
    def __init__(self, main):
        self.main = main
        self.frame = None
        self.UPDATE = {'ID': '', 'Found': False}
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee-management"
        )
        self.cursor = self.connection.cursor()
        self.panel_window()
        self.side_menu()

    def panel_window(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        width = 500
        height = 300
        _x = (root.winfo_screenwidth() / 2) - (width / 2)
        _y = (root.winfo_screenheight() / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(_x)}+{int(_y)}')
        self.main.resizable(False, False)
        self.main.title('Employee Management')

    def side_menu(self):
        f1 = tk.Frame(self.main, pady=10, padx=10, width=15, relief='raised')
        tk.Button(f1, text='Show All Data', width=14, height=2, command=self.show_all_data).grid(row=0, column=0, pady=3)
        tk.Button(f1, text='Add an Employee', width=14, height=2, command=self.add_employee).grid(row=1, column=0, pady=3)
        tk.Button(f1, text='Fire Employee', width=14, height=2,
                  command=lambda: self.search_employee(False)).grid(row=2, column=0, pady=3)
        tk.Button(f1, text='Update Data', width=14, height=2,
                  command=lambda: self.search_employee(True)).grid(row=3, column=0, pady=3)
        tk.Button(f1, text='Export Data', width=14, height=2, command=self.export_data).grid(row=4, column=0, pady=3)
        tk.Button(f1, text='Logout', width=14, height=2, command=self.logout).grid(row=5, column=0, pady=3)
        f1.pack(padx=4, pady=4, fill=tk.Y, side='left')

    def show_all_data(self):
        if self.frame is not None:
            self.frame.destroy()
        # Execute a SELECT query to retrieve all data from the empdata table
        self.cursor.execute("SELECT * FROM empdata")
        # Fetch all rows of the result set
        rows = self.cursor.fetchall()
        header = self.cursor.column_names

        self.frame = tk.Frame(self.main, pady=10, padx=10, relief='raised', bg='sky blue')
        # Add a vertical tk.Scrollbar to the treeview widget
        scroll_y = tk.Scrollbar(self.frame)
        scroll_x = tk.Scrollbar(self.frame, orient=tkinter.HORIZONTAL)
        scroll_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scroll_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        tree = ttk.Treeview(self.frame, columns=header, show="headings", yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set)
        for column in header:
            tree.heading(column, text=column)
            if column == header[0]:
                tree.column(column, width=30, anchor='center')
            elif column == header[-1]:
                tree.column(column, width=200, anchor='center')
            else:
                tree.column(column, width=100, anchor='center')

        tree.pack(fill='both', expand=True)
        # Insert the data into the treeview widget
        for row in rows:
            tree.insert("", "end", values=row, )

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        self.frame.pack(padx=5, pady=5, fill='both', side='left', expand=True)

    def add_employee(self):
        data = None
        if self.frame is not None:
            self.frame.destroy()
        if self.UPDATE['Found']:
            _id = self.UPDATE['ID']
            select = "SELECT * FROM empdata WHERE ID=%s"
            self.cursor.execute(select, (_id,))
            data = self.cursor.fetchone()
        entries = []
        labels = ['First Name', 'Last Name', 'Gender', 'Job Position', 'Contact', 'Email', 'Address']
        gender_list = ['Male', 'Female', 'Rather not say']
        job_positions = ['Accountant', 'Hiring Manager(HR)', 'Senior Developer', 'IT Incharge', 'Trainee']
        self.frame = tk.Frame(self.main, padx=10, pady=10, background='sky blue')
        for index, label in enumerate(labels):
            tk.Label(self.frame, text=label, font='arial 15').grid(row=index, column=0, pady=3)
            if label == 'Gender':
                gender = ttk.Combobox(self.frame, font='arial 12', values=gender_list, state='readonly', width=16)
                gender.grid(row=index, column=1, pady=3)
                gender.set(gender_list[0])
                if self.UPDATE['Found']:
                    gender.insert(0, data[index + 1])
                entries.append(gender)
            elif label == 'Job Position':
                position = ttk.Combobox(self.frame, font='arial 12', values=job_positions, width=16, state='readonly')
                position.grid(row=index, column=1, pady=3)
                position.set(job_positions[0])
                if self.UPDATE['Found']:
                    position.insert(0, data[index + 1])
                entries.append(position)
            else:
                entry = tk.Entry(self.frame, font='arial 15', width=18)
                entry.grid(row=index, column=1, pady=3)
                if self.UPDATE['Found']:
                    entry.insert(0, data[index + 1])
                entries.append(entry)

        tk.Button(self.frame, text='Submit', font='arial 10 bold', pady=5, padx=10, cursor='hand2',
                  command=lambda: self.save_employee_data(entries)).grid(row=7, column=1)
        self.frame.pack(side='top', fill='both', pady=5, padx=5)

    def delete_employee(self):
        select_data = "SELECT * FROM empdata"
        delete_record = "DELETE FROM empdata WHERE id=?"
        _id = self.UPDATE['ID']
        self.cursor.execute(select_data)
        data = self.cursor.fetchall()
        self.search_employee()
        if self.UPDATE['Found']:
            for record in data:
                if record[0] == _id:
                    self.cursor.execute(delete_record, (_id,))
                    tkinter.messagebox.showinfo('Deleted', 'Employee Record has been deleted Successfully!')
                    break

    def update_employee(self):
        self.search_employee()
        print(self.UPDATE['Found'])
        if self.UPDATE['Found']:
            # self.add_employee()
            print(self.UPDATE['Found'])

    def export_data(self):
        self.cursor.execute("SELECT * FROM empdata")
        data = self.cursor.fetchall()
        header = self.cursor.column_names
        with open('empData.csv', mode='w', newline='') as file:
            write = csv.writer(file)
            write.writerow(header)
            write.writerows(data)
        tkinter.messagebox.showinfo('Exported', 'Data has been exported Successfully!')

    def logout(self):
        confirm = tkinter.messagebox.askyesno('Confirm', 'Are you Sure to Logout?')
        if confirm:
            self.connection.close()
            self.main.destroy()

    def search_employee(self, check=0):
        if self.frame is not None:
            self.frame.destroy()
            self.UPDATE = {'ID': '', 'Found': False}
        self.frame = tk.Frame(self.main, pady=10, padx=10, relief='raised')
        tk.Label(self.frame, text='First Name: ').grid(row=0, column=0)
        first_name = tk.Entry(self.frame, font='lucid 15', width=15)
        first_name.grid(row=0, column=1)
        tk.Label(self.frame, text='Last Name: ').grid(row=1, column=0)
        last_name = tk.Entry(self.frame, font='lucid 15', width=15)
        last_name.grid(row=1, column=1)
        tk.Button(self.frame, text='Search', font='arial 10 bold', pady=3, padx=5, cursor='hand2',
                  command=lambda: self.modify_data(first_name.get(), last_name.get(), check)) \
            .grid(row=3, column=1, pady=10)
        self.frame.place(relx=0.6, rely=0.5, anchor='center')

    def search_from_database(self, f_name, l_name):
        query = "SELECT id,fname,lname FROM empdata"
        self.cursor.execute(query)
        values = self.cursor.fetchall()
        for data in values:
            if data[1] == f_name and data[2] == l_name:
                self.UPDATE.update({'ID': data[0], 'Found': True})
                break
        else:
            tkinter.messagebox.showerror('Not Found!', 'No Such Employee with Given Data!')

    def modify_data(self, f_name, l_name, check):
        self.search_from_database(f_name, l_name)
        if check:
            if self.UPDATE['Found']:
                self.add_employee()
        else:
            if self.UPDATE['Found']:
                self.delete_employee()

    def save_employee_data(self, data):
        values = []
        for value in data:
            if value.get() == '':
                tkinter.messagebox.showerror('Empty Fields!', 'Fields cannot be empty!')
                break
            else:
                values.append(value.get())
        else:
            tup_val = tuple(values)
            if self.UPDATE['Found']:
                _id = self.UPDATE['ID']
                update_query = "UPDATE empdata SET fname=%s,lname=%s,gender=%s,jobposition=%s," \
                               "contact=%s,email=%s,address=%s WHERE id=%s"
                self.cursor.execute(update_query, (*tup_val, _id))
                self.connection.commit()
                self.UPDATE.update({'ID': '', 'Found': False})
                tkinter.messagebox.showinfo('Updated!', 'Employee data has been updated successfully!')
            else:
                query = "INSERT INTO empdata VALUES (0,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(query, tup_val)
                self.connection.commit()
                tkinter.messagebox.showinfo('Success!', 'New Employee has been added successfully!')


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='grey')
    app_width = 300
    app_height = 170
    x = (root.winfo_screenwidth() / 2) - (app_width / 2)
    y = (root.winfo_screenheight() / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    root.resizable(False, False)
    root.iconbitmap('icon.ico')
    root.title('Admin Login')
    admin = AdminLogin(main=root)

    def clicked():
        admin.login()
        if admin.AUTHORIZED:
            AdminPanel(root)

    user_value = tk.StringVar()
    pass_value = tk.StringVar()
    show_pass = tk.BooleanVar(value=True)

    f = tk.Frame(root, pady=15, padx=10)
    tk.Label(f, text="UserName ", font='lucid 15 bold').grid(row=0, column=0)
    user_entry = tk.Entry(f, font='arial 10')
    user_entry.grid(row=0, column=1)
    tk.Label(f, text="Password ", font='lucid 15 bold').grid(row=1, column=0)
    pass_entry = tk.Entry(f, font='arial 10', textvariable=pass_value, show='*')
    pass_entry.grid(row=1, column=1)
    toggle_password = tk.Checkbutton(f, text="Show Password", onvalue=False, offvalue=True,
                                     variable=show_pass, command=lambda: admin.toggle(show_pass.get(), pass_entry))
    toggle_password.grid(row=3, column=1)
    login_button = tk.Button(f, text='Login', background='grey', padx=5, font='lucid 10 bold', cursor='hand2',
                             state='disabled', command=clicked)
    login_button.grid(row=4, column=1)
    f.pack(pady=15)

    pass_value.trace(mode='w', callback=lambda *args: admin.validate(pass_value.get(), login_button, *args))

    root.mainloop()
