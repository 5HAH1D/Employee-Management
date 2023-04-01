import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import csv
import customtkinter as ctk
import mysql.connector
from PIL import Image


class AdminLogin:
    def __init__(self):
        self.CURRENT_USER = None
        self.PRIVILEGE = None

    def login(self, user, passwrd):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_login')
        data = cursor.fetchall()
        for person in data:
            if (user == person[1]) and (passwrd == person[2]):
                self.CURRENT_USER = person[1]
                self.PRIVILEGE = person[0]
                return True
        else:
            return False

    def toggle(self, check, p_entry):
        if check:
            p_entry.configure(show='*')
        else:
            p_entry.configure(show='')


class AdminPanel:
    def __init__(self, window, admin, current):
        self.main = window
        self.ADMIN = admin
        self.CURRENT_USER = current
        self.frame = None
        self.photo = None
        self.UPDATE = {'ID': '', 'Found': False}
        self.cursor = connection.cursor()
        self.panel_window()

    def panel_window(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        width = 500
        height = 330
        _x = (self.main.winfo_screenwidth() / 2) - (width / 2)
        _y = (self.main.winfo_screenheight() / 2) - (height / 2)
        self.main.geometry(f"{width}x{height}+{int(_x)}+{int(_y)}")
        self.main.title("Employee Management")
        self.navigation_panel()
        self.home()

    def navigation_panel(self):
        f1 = ctk.CTkFrame(self.main)
        ctk.CTkButton(f1, text='Home', width=130, font=('Maiandra GD', 15), command=self.home).grid(row=0, column=0, pady=3)
        ctk.CTkButton(f1, text='Show All Data', width=130, font=('Maiandra GD', 15), command=self.show_all_data).grid(row=1, column=0, pady=3)
        ctk.CTkButton(f1, text='Add Employee', width=130, font=('Maiandra GD', 15), command=self.add_employee).grid(row=2, column=0, pady=3)
        button1 = ctk.CTkButton(f1, text='Fire Employee', width=130, font=('Maiandra GD', 15),
                                command=lambda: self.search_employee(False))
        button1.grid(row=3, column=0, pady=3)
        ctk.CTkButton(f1, text='Update Data', width=130, font=('Maiandra GD', 15),
                      command=lambda: self.search_employee(True)).grid(row=4, column=0, pady=3)
        ctk.CTkButton(f1, text='Export Data', width=130, font=('Maiandra GD', 15), command=self.export_data).grid(row=5, column=0, pady=3)
        button2 = ctk.CTkButton(f1, text='Add New User', width=130, font=('Maiandra GD', 15), command=self.add_new_user)
        button2.grid(row=6, column=0, pady=3)
        if not self.ADMIN:
            button1.configure(state='disabled')
            button2.configure(state='disabled')
        ctk.CTkButton(f1, text='Change Password', width=130, font=('Maiandra GD', 15), command=self.change_password).grid(row=7, column=0, pady=3)
        ctk.CTkButton(f1, text='Logout', width=130, font=('Maiandra GD', 15), command=self.logout).grid(row=8, column=0, pady=3)
        f1.pack(padx=4, pady=4, fill='y', side='left')

    def home(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = ctk.CTkFrame(self.main)
        self.photo = ctk.CTkImage(Image.open('images/home_image.png'), size=(470, 300))
        ctk.CTkLabel(self.frame, image=self.photo, text='').pack(fill='both', expand=True)
        self.frame.pack(padx=5, pady=5, fill='both', side='left', expand=True)

    def show_all_data(self):
        if self.frame is not None:
            self.frame.destroy()
        # Execute a SELECT query to retrieve all data from the emp_data table
        self.cursor.execute("SELECT * FROM emp_data")
        # Fetch all rows of the result set
        rows = self.cursor.fetchall()
        header = self.cursor.column_names

        self.frame = ctk.CTkFrame(self.main)
        # Add a vertical tk.Scrollbar to the treeview widget
        scroll_y = ctk.CTkScrollbar(self.frame)
        scroll_x = ctk.CTkScrollbar(self.frame, orientation=tkinter.HORIZONTAL)
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

        scroll_y.configure(command=tree.yview)
        scroll_x.configure(command=tree.xview)
        self.frame.pack(padx=5, pady=5, fill='both', side='left', expand=True)

    def add_employee(self):
        data = None
        if self.frame is not None:
            self.frame.destroy()
        if self.UPDATE['Found']:
            _id = self.UPDATE['ID']
            select = "SELECT * FROM emp_data WHERE ID=%s"
            self.cursor.execute(select, (_id,))
            data = self.cursor.fetchone()
        entries = []
        ph_index = 0
        place_holders = ['First Name', 'Last Name', '92XXXXXXXXX', 'example@123', 'House/Street/Area']
        labels = ['First Name', 'Last Name', 'Gender', 'Job Position', 'Contact', 'Email', 'Address']
        gender_list = ['Male', 'Female', 'Rather not say']
        job_positions = ['Accountant', 'Hiring Manager(HR)', 'Senior Developer', 'IT Incharge', 'Trainee']
        self.frame = ctk.CTkFrame(self.main)
        for index, label in enumerate(labels):
            ctk.CTkLabel(self.frame, text=label, font=('arial', 15)).grid(row=index, column=0, padx=20)
            if label == 'Gender':
                gender = ctk.CTkComboBox(self.frame, font=('arial', 15), values=gender_list, state='readonly')
                gender.grid(row=index, column=2, pady=3)
                if self.UPDATE['Found']:
                    gender.set(gender_list[data.index(index + 1)])
                else:
                    gender.set(gender_list[0])
                entries.append(gender)
            elif label == 'Job Position':
                position = ctk.CTkComboBox(self.frame, font=('arial', 15), values=job_positions, state='readonly')
                position.grid(row=index, column=2, pady=3)
                if self.UPDATE['Found']:
                    position.set(job_positions[data.index(index + 1)])
                else:
                    position.set(job_positions[0])
                entries.append(position)
            else:
                entry = ctk.CTkEntry(self.frame, font=('arial', 15), width=200, placeholder_text=place_holders[ph_index])
                entry.grid(row=index, column=1, columnspan=3, pady=3)
                ph_index += 1
                if self.UPDATE['Found']:
                    entry.insert(0, data[index + 1])
                entries.append(entry)

        ctk.CTkButton(self.frame, text='Submit', font=('arial', 15, 'bold'),
                      command=lambda: self.add_employee_db(entries)).grid(row=7, column=2, pady=5)
        self.frame.pack(side='top', fill='both', pady=5, padx=5, expand=True)

    def delete_employee(self):
        select_data = "SELECT * FROM emp_data"
        delete_record = "DELETE FROM emp_data WHERE id=?"
        _id = self.UPDATE['ID']
        self.cursor.execute(select_data)
        data = self.cursor.fetchall()
        self.search_employee()
        if self.UPDATE['Found']:
            for record in data:
                if record[0] == _id:
                    confirm = tkinter.messagebox.askyesno("Confirmation", "Are You Sure to Delete the Record?")
                    if confirm:
                        self.cursor.execute(delete_record, (_id,))
                        tkinter.messagebox.showinfo('Deleted', 'Employee Record has been deleted Successfully!')
                        break

    def export_data(self):
        self.cursor.execute("SELECT * FROM emp_data")
        data = self.cursor.fetchall()
        header = self.cursor.column_names
        with open('emp_data.csv', mode='w', newline='') as file:
            write = csv.writer(file)
            write.writerow(header)
            write.writerows(data)
        tkinter.messagebox.showinfo('Exported', 'Data has been exported Successfully!')

    def add_new_user(self):
        if self.frame is not None:
            self.frame.destroy()
        values = ['Admin', 'User']
        pass_value = tk.StringVar()
        self.frame = ctk.CTkFrame(self.main)
        ctk.CTkLabel(self.frame, text='Privilege: ', font=('lucid', 15)).grid(row=0, column=0, pady=5, padx=5)
        privilege = ctk.CTkComboBox(self.frame, font=('arial', 15), values=values, state='readonly')
        privilege.grid(row=0, column=1, pady=3)
        privilege.set(values[1])
        ctk.CTkLabel(self.frame, text='Username: ', font=('lucid', 15)).grid(row=1, column=0, pady=5, padx=5)
        username = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, placeholder_text='Username')
        username.grid(row=1, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='Password: ', font=('lucid', 15)).grid(row=2, column=0, pady=5, padx=5)
        password = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, show='*', textvariable=pass_value)
        password.grid(row=2, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='*Password Should Be\nLonger than 8 Characters', font=('lucid', 11)).grid(row=3, column=1, pady=2)
        add_btn = ctk.CTkButton(self.frame, text='Add', font=('arial', 15, 'bold'), width=100, state='disabled',
                                command=lambda: self.add_new_user_db(privilege, username, password))
        add_btn.grid(row=4, column=1, pady=10)
        self.frame.place(relx=0.6, rely=0.5, anchor='center')
        pass_value.trace(mode='w', callback=lambda *args: self.validate_password(pass_value.get(), add_btn, *args))

    def add_new_user_db(self, _privilege, _username, _password):
        if _privilege.get() == "Admin":
            confirm = tkinter.messagebox.askyesno("Confirmation", "Admin Will have All the Rights to Management System\n"
                                                                  "Are You Sure to Continue?")
        else:
            confirm = tkinter.messagebox.askyesno("Confirmation", "User will be allowed to:\n"
                                                                  "1- See All Employees Data\n"
                                                                  "2- Add a New Employee\n"
                                                                  "3- Update Employee's Data\n"
                                                                  "4- Export all Data\n"
                                                                  "Are you sure to Add a New Authentication User?\n")
        if confirm:
            add_query = "INSERT INTO user_login VALUES (%s, %s, %s)"
            self.cursor.execute(add_query, (_privilege.get(), _username.get(), _password.get()))
            connection.commit()
            _username.delete(0, tk.END)
            _password.delete(0, tk.END)
            tkinter.messagebox.showinfo("Success!", "User has been added successfully!")

    def change_password(self):
        if self.frame is not None:
            self.frame.destroy()
        pass_value = tk.StringVar()
        self.frame = ctk.CTkFrame(self.main)
        ctk.CTkLabel(self.frame, text='Username: ', font=('lucid', 15)).grid(row=0, column=0, pady=5, padx=5)
        username = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150)
        username.insert(0, self.CURRENT_USER)
        username.configure(state='readonly')
        username.grid(row=0, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='Password: ', font=('lucid', 15)).grid(row=1, column=0, pady=5, padx=5)
        password = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, textvariable=pass_value)
        password.grid(row=1, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='*Password Should Be\nLonger than 8 Characters', font=('lucid', 11)).grid(row=2, column=1, pady=2)
        change_btn = ctk.CTkButton(self.frame, text='Change', font=('arial', 15, 'bold'), width=100, state='disabled',
                                   command=lambda: self.change_password_db(username, password))
        change_btn.grid(row=3, column=1, pady=10)
        self.frame.place(relx=0.6, rely=0.5, anchor='center')
        pass_value.trace(mode='w', callback=lambda *args: self.validate_password(pass_value.get(), change_btn, *args))

    def validate_password(self, *args):
        pass_ = args[0]
        button = args[1]
        if len(pass_) >= 8:
            button.configure(state='normal')
        else:
            button.configure(state='disabled')

    def change_password_db(self, _username, _password):
        if not _password == '':
            change_password_query = "UPDATE user_login SET password=%s WHERE user_name=%s"
            self.cursor.execute(change_password_query, (_password.get(), _username.get()))
            connection.commit()
            tkinter.messagebox.showinfo('Success!', 'Your Password Has Been Changed Successfully!')
            _password.delete(0, tk.END)
        else:
            tkinter.messagebox.showerror("ERROR", "Password can Not be Empty!")

    def logout(self):
        confirm = tkinter.messagebox.askyesno('Confirm', 'Are you Sure to Logout?')
        if confirm:
            for widget in self.main.winfo_children():
                widget.destroy()
            main(self.main)

    def search_employee(self, check=0):
        if self.frame is not None:
            self.frame.destroy()
            self.UPDATE = {'ID': '', 'Found': False}
        self.frame = ctk.CTkFrame(self.main)
        ctk.CTkLabel(self.frame, text='First Name: ', font=('lucid', 15)).grid(row=0, column=0, pady=5, padx=5)
        first_name = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150)
        first_name.grid(row=0, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='Last Name: ', font=('lucid', 15)).grid(row=1, column=0, pady=5, padx=5)
        last_name = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150)
        last_name.grid(row=1, column=1, pady=5, padx=5)
        ctk.CTkButton(self.frame, text='Search', font=('arial', 15, 'bold'), width=100,
                      command=lambda: self.modify_data(first_name.get(), last_name.get(), check)) \
            .grid(row=3, column=1, pady=10)
        self.frame.place(relx=0.6, rely=0.5, anchor='center')

    def search_employee_db(self, f_name, l_name):
        query = "SELECT id,fname,lname FROM emp_data"
        self.cursor.execute(query)
        values = self.cursor.fetchall()
        for data in values:
            if data[1] == f_name and data[2] == l_name:
                self.UPDATE.update({'ID': data[0], 'Found': True})
                break
        else:
            tkinter.messagebox.showerror('Not Found!', 'No Such Employee with Given Data!')

    def modify_data(self, f_name, l_name, check):
        self.search_employee_db(f_name, l_name)
        if check:
            if self.UPDATE['Found']:
                self.add_employee()
        else:
            if self.UPDATE['Found']:
                self.delete_employee()

    def add_employee_db(self, data):
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
                update_query = "UPDATE emp_data SET fname=%s,lname=%s,gender=%s,jobposition=%s," \
                               "contact=%s,email=%s,address=%s WHERE id=%s"
                self.cursor.execute(update_query, (*tup_val, _id))
                connection.commit()
                self.UPDATE.update({'ID': '', 'Found': False})
                tkinter.messagebox.showinfo('Updated!', 'Employee data has been updated successfully!')
            else:
                query = "INSERT INTO emp_data VALUES (0,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(query, tup_val)
                connection.commit()
                tkinter.messagebox.showinfo('Success!', 'New Employee has been added successfully!')


def main(root):
    admin = AdminLogin()

    def clicked():
        authorized = admin.login(user_entry.get(), pass_entry.get())
        if authorized:
            role = admin.PRIVILEGE
            current_user = admin.CURRENT_USER
            if role == "Admin":
                AdminPanel(window=root, admin=True, current=current_user)
            else:
                AdminPanel(window=root, admin=False, current=current_user)
        else:
            ask_retry = tkinter.messagebox.askretrycancel("Wrong Credentials!",
                                                          "Username or Password is Incorrect!")
            if ask_retry:
                user_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)
                user_entry.update()
                pass_entry.update()
            else:
                exit()

    app_width = 300
    app_height = 180
    x = (root.winfo_screenwidth() / 2) - (app_width / 2)
    y = (root.winfo_screenheight() / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    root.resizable(False, False)
    root.iconbitmap('images/icon.ico')
    root.title('Admin Login')

    show_pass = tk.BooleanVar(value=True)

    f = ctk.CTkFrame(root)
    ctk.CTkLabel(f, text="UserName ", font=('lucid', 15, 'bold')).grid(row=0, column=0, pady=5, padx=5)
    user_entry = ctk.CTkEntry(f, font=('arial', 15), placeholder_text='Username')
    user_entry.grid(row=0, column=1, pady=5, padx=5)
    ctk.CTkLabel(f, text="Password ", font=('lucid', 15, 'bold')).grid(row=1, column=0, pady=5, padx=5)
    pass_entry = ctk.CTkEntry(f, font=('arial', 15), placeholder_text='Password', show='*')
    pass_entry.grid(row=1, column=1, pady=5, padx=5)
    toggle_password = ctk.CTkCheckBox(f, text="Show Password", onvalue=False, offvalue=True,
                                      variable=show_pass, command=lambda: admin.toggle(show_pass.get(), pass_entry))
    toggle_password.grid(row=3, column=1, pady=5, padx=5)
    login_button = ctk.CTkButton(f, text='Login', command=clicked)
    login_button.grid(row=4, column=1, pady=5, padx=5)
    f.pack(pady=15, ipadx=10, ipady=20)

    root.mainloop()


if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='employee-management')
    except mysql.connector.errors.ProgrammingError:
        tkinter.messagebox.showerror("Database ERROR!", "1- Database 'employee-management' Doesn't Exists\n"
                                                        "2- Wrong 'user' OR 'password'\n"
                                                        "Try to Check Database and Credentials OR Contact the Developer")
        exit()
    except mysql.connector.errors.InterfaceError:
        tkinter.messagebox.showerror("Connection ERROR!", "Unable to Connect to Database 'employee-management'\n"
                                                          "Try to Check Connection and Retry")
        exit()
    except Exception as error:
        tkinter.messagebox.showerror("ERROR!", f"An Unhandled Error!\n{error}\nPlease Contact the Developer")

    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    app = ctk.CTk()
    app.configure(background='grey')
    main(root=app)
