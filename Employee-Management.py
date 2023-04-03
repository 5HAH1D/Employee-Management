import tkinter as tk
from tkinter.ttk import Treeview
import tkinter.messagebox
from csv import writer
import customtkinter as ctk
import mysql.connector
from PIL import Image


# It's a class that allows the user to log in to the program.
class AdminLogin:
    """
    This class represents an administrator login system.

    Attributes:
    - CURRENT_USER: A string representing the current user who is logged in.
    - PRIVILEGE: A string representing the privilege level of the current user.

    Methods:
    - login(user, passwrd): Takes a username and password as input, and checks if they match a record in the database.
    Returns: Boolean value indicating whether the login was successful.

    - toggle(check, p_entry): Takes a boolean value and a password entry widget as input.
    If true, the password entry will show '*' instead of the actual password.
    If false, it will show the actual password characters.
    """

    def __init__(self):
        self.CURRENT_USER = None
        self.PRIVILEGE = None

    def login(self, user, passwrd):
        """
        It takes a username and password, and checks if it exists in the database.
        If it does, it sets the current user to the username and the privilege to the privilege of the
        user.
        If it doesn't, it returns false.
        Returns: Boolean value.
        """
        # create a cursor object to execute SQL queries
        cursor = connection.cursor()
        select_all = "SELECT * FROM user_login"
        # execute the SQL query to select all records from the user_login table
        cursor.execute(select_all)

        # fetch all the rows from the table
        data = cursor.fetchall()

        # loop through the fetched data
        for person in data:
            # check if the given user and password match with any record in the fetched data
            if (user == person[1]) and (passwrd == person[2]):
                # if the user and password match, set the CURRENT_USER and PRIVILEGE attributes and return True
                self.CURRENT_USER = person[1]
                self.PRIVILEGE = person[0]
                return True

        # if no match is found in the loop, return False
        else:
            return False

    def toggle(self, check, p_entry):
        """
        If the checkbox is checked, then the password entry will show the password as asterisks,
        otherwise it will show the password as plain text
        """
        if check:
            # If the condition is true, then the password entry widget will show '*' instead of the actual password characters
            p_entry.configure(show='*')
        else:
            # If the condition is false, then the password entry widget will show the actual password characters
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
        """
        This method creates a new panel window for the employee management system.
        It first destroys all the child widgets of the current main window.
        Then, it calculates the dimensions and position of the new window based on the screen size.
        Finally, it sets the title and calls the navigation_panel() and home() methods to display the content.
        """

        # Destroy all child widgets of the current main window
        for widget in self.main.winfo_children():
            widget.destroy()

        # Set the dimensions and position of the new window
        width = 500  # Width of the new window
        height = 330  # Height of the new window
        _x = (self.main.winfo_screenwidth() / 2) - (width / 2)  # X position of the new window
        _y = (self.main.winfo_screenheight() / 2) - (height / 2)  # Y position of the new window
        self.main.geometry(f"{width}x{height}+{int(_x)}+{int(_y)}")  # Set the geometry of the new window

        # Set the title of the new window
        self.main.title("Employee Management")

        # Call the navigation_panel() method to display the navigation panel on the left side of the window
        self.navigation_panel()

        # Call the home() method to display the content on the right side of the window
        self.home()

    def navigation_panel(self):
        """
        This method creates the navigation panel on the left side of the employee management system window.
        It adds buttons for various actions like Home, Show All Data, Add Employee, Fire Employee, Update Data, Export Data,
        Add New User, Change Password and Logout.
        It also disables the Fire Employee and Add New User buttons if the user is not an ADMIN.
        """

        # Create a new frame for the navigation panel
        f1 = ctk.CTkFrame(self.main)

        # Add a button for the Home action
        ctk.CTkButton(f1, text='Home', width=130, font=('Maiandra GD', 15), command=self.home).grid(row=0, column=0, pady=3)

        # Add a button for the Show All Data action
        ctk.CTkButton(f1, text='Show All Data', width=130, font=('Maiandra GD', 15), command=self.show_all_data).grid(row=1, column=0, pady=3)

        # Add a button for the Add Employee action
        ctk.CTkButton(f1, text='Add Employee', width=130, font=('Maiandra GD', 15), command=self.add_employee).grid(row=2, column=0, pady=3)

        # Add a button for the Fire Employee action
        button1 = ctk.CTkButton(f1, text='Fire Employee', width=130, font=('Maiandra GD', 15), command=lambda: self.search_employee(False))
        button1.grid(row=3, column=0, pady=3)

        # Add a button for the Update Data action
        ctk.CTkButton(f1, text='Update Data', width=130, font=('Maiandra GD', 15), command=lambda: self.search_employee(True)).grid(row=4, column=0,
                                                                                                                                    pady=3)

        # Add a button for the Export Data action
        ctk.CTkButton(f1, text='Export Data', width=130, font=('Maiandra GD', 15), command=self.export_data).grid(row=5, column=0, pady=3)

        # Add a button for the Add New User action
        button2 = ctk.CTkButton(f1, text='Add New User', width=130, font=('Maiandra GD', 15), command=self.add_new_user)
        button2.grid(row=6, column=0, pady=3)

        # Disable the Fire Employee and Add New User buttons if the user is not an ADMIN
        if not self.ADMIN:
            button1.configure(state='disabled')
            button2.configure(state='disabled')

        # Add a button for the Change Password action
        ctk.CTkButton(f1, text='Change Password', width=130, font=('Maiandra GD', 15), command=self.change_password).grid(row=7, column=0, pady=3)

        # Add a button for the Logout action
        ctk.CTkButton(f1, text='Logout', width=130, font=('Maiandra GD', 15), command=self.logout).grid(row=8, column=0, pady=3)

        # Pack the frame into the window
        f1.pack(padx=4, pady=4, fill='y', side='left')

    def home(self):
        """This function sets up the home page of the application, displaying an image and text.
        Args:
            self: An instance of the main application class.
        Returns: None
        """

        # If the frame already exists, destroy it to start with a fresh frame
        if self.frame is not None:
            self.frame.destroy()

        # Create a new frame and set it as the main frame for the application
        self.frame = ctk.CTkFrame(self.main)

        # Load an image from a file and create a Tkinter-compatible image object
        self.photo = ctk.CTkImage(Image.open('images/home_image.png'), size=(470, 300))

        # Create a label and pack it into the frame, displaying the image and hiding any text
        ctk.CTkLabel(self.frame, image=self.photo, text='').pack(fill='both', expand=True)

        # Pack the frame into the main window, filling and expanding it to take up all available space
        self.frame.pack(padx=5, pady=5, fill='both', side='left', expand=True)

    def show_all_data(self):
        """This function retrieves all data from the database and displays it in a table.
        Args:
            self: An instance of the main application class.
        Returns: None
        """

        # If the frame already exists, destroy it to start with a fresh frame
        if self.frame is not None:
            self.frame.destroy()

        # Execute a SELECT statement to retrieve all rows from the database
        self.cursor.execute("SELECT * FROM emp_data")
        rows = self.cursor.fetchall()

        # Get the column names from the cursor object
        header = self.cursor.column_names

        # Create a new frame to hold the table and scrollbars
        self.frame = ctk.CTkFrame(self.main)

        # Create vertical and horizontal scrollbars for the table
        scroll_y = ctk.CTkScrollbar(self.frame)
        scroll_x = ctk.CTkScrollbar(self.frame, orientation=tk.HORIZONTAL)
        scroll_y.pack(side=tk.RIGHT, fill='y')
        scroll_x.pack(side=tk.BOTTOM, fill='x')

        # Create a Treeview object to display the data in a table format
        tree = Treeview(self.frame, columns=header, show="headings", yscrollcommand=scroll_y.set,
                        xscrollcommand=scroll_x.set)

        # Set the column headings and widths
        for column in header:
            tree.heading(column, text=column)
            if column == header[0]:
                tree.column(column, width=50, anchor='center')
            elif column == header[-1]:
                tree.column(column, width=200, anchor='center')
            else:
                tree.column(column, width=100, anchor='center')
        tree.pack(fill='both', expand=True)
        # Insert each row of data into the table
        for row in rows:
            tree.insert("", "end", values=row)

        # Configure the scrollbars to work with the table
        scroll_y.configure(command=tree.yview)
        scroll_x.configure(command=tree.xview)

        # Pack the frame into the main window, filling and expanding it to take up all available space
        self.frame.pack(padx=5, pady=5, fill='both', side='left', expand=True)

    def add_employee(self):
        """
        This method creates a form to add a new employee's data to the database.

        If the self.UPDATE['Found'] flag is True, it pre-populates the form with the data of the employee to be updated.
        Otherwise, it generates a new employee ID and pre-populates the Employee ID field with it.

        Once the user fills out the form and clicks the 'Submit' button, the method calls the add_employee_db() method to add
        the new employee data to the database.

        Parameters: None
        Returns: None
        """
        # Initialize data and new_id variables to None
        data = None
        new_id = None
        # Destroy the frame if it exists
        if self.frame is not None:
            self.frame.destroy()
        # Check if an employee is being updated
        if self.UPDATE['Found']:
            # Get the ID of the employee being updated
            _id = self.UPDATE['ID']
            # Select the employee data from the database using the ID
            select = "SELECT * FROM emp_data WHERE ID=%s"
            self.cursor.execute(select, (_id,))
            # Get the selected data
            data = self.cursor.fetchone()
        else:
            # If not updating, get the data of the last employee in the database
            query = "SELECT * FROM emp_data ORDER BY ID DESC LIMIT 1"
            self.cursor.execute(query)
            # Get the data
            row = self.cursor.fetchone()
            # Create a new ID for the new employee
            create_new_id = int(row[0].split('P')[1]) + 1
            # Check if the ID is less than or equal to 9
            if create_new_id <= 9:
                # Format the new ID
                new_id = f"EMP0{create_new_id}"
            else:
                # Format the new ID
                new_id = f"EMP{create_new_id}"
        # Initialize entries list and placeholder index
        entries = []
        ph_index = 0
        # Set placeholder texts and labels
        place_holders = ['First Name', 'Last Name', '92XXXXXXXXX', 'example@123', 'House / Street / Area']
        labels = ['First Name', 'Last Name', 'Gender', 'Job Position', 'Contact', 'Email', 'Address']
        # Set options for gender and job positions
        gender_list = ['Male', 'Female', 'Rather not say']
        job_positions = ['Accountant', 'Hiring Manager(HR)', 'Senior Developer', 'IT Incharge', 'Trainee']

        # Create a new frame
        self.frame = ctk.CTkFrame(self.main)
        # Add the label for the employee ID
        ctk.CTkLabel(self.frame, text='Employee ID', font=('arial', 15)).grid(row=0, column=0, padx=20)
        emp_id = ctk.CTkEntry(self.frame, font=('arial', 15), width=150)
        emp_id.grid(row=0, column=1, pady=3)
        # Check if updating an employee
        if self.UPDATE['Found']:
            # Set the employee ID as the ID of the employee being updated
            emp_id.insert(0, data[0])
            emp_id.configure(state='readonly')
        else:
            # Set the employee ID as the newly generated ID
            emp_id.insert(0, new_id)
            emp_id.configure(state='readonly')
            # Add the employee ID entry to the entries list
            entries.append(emp_id)

        # Loop through each label and its index in the labels list
        for index, label in enumerate(labels):
            # Create a label widget and place it on the grid
            ctk.CTkLabel(self.frame, text=label, font=('arial', 15)).grid(row=index + 1, column=0, padx=20)
            # If the label is 'Gender', create a combo box with gender options and place it on the grid
            if label == 'Gender':
                gender = ctk.CTkComboBox(self.frame, font=('arial', 15), values=gender_list, state='readonly')
                gender.grid(row=index + 1, column=1, pady=3)
                # If the UPDATE dictionary contains data, set the combo box value to the corresponding data value
                if self.UPDATE['Found']:
                    gender.set(data[index + 1])
                # Otherwise, set the combo box value to the first gender option
                else:
                    gender.set(gender_list[0])
                # Append the combo box widget to the entries list
                entries.append(gender)
            # If the label is 'Job Position', create a combo box with job position options and place it on the grid
            elif label == 'Job Position':
                position = ctk.CTkComboBox(self.frame, font=('arial', 15), values=job_positions, state='readonly')
                position.grid(row=index + 1, column=1, pady=3)
                # If the UPDATE dictionary contains data, set the combo box value to the corresponding data value
                if self.UPDATE['Found']:
                    position.set(data[index + 1])
                # Otherwise, set the combo box value to the first job position option
                else:
                    position.set(job_positions[0])
                # Append the combo box widget to the entries list
                entries.append(position)
            # For all other labels, create an entry widget with a placeholder text and place it on the grid
            else:
                entry = ctk.CTkEntry(self.frame, font=('arial', 15), width=150, placeholder_text=place_holders[ph_index])
                entry.grid(row=index + 1, column=1, pady=3)
                ph_index += 1
                # If the UPDATE dictionary contains data, set the entry value to the corresponding data value
                if self.UPDATE['Found']:
                    entry.insert(0, data[index + 1])
                # Append the entry widget to the entries list
                entries.append(entry)

        # Create a button widget and place it on the grid with a lambda function that calls the add_employee_db method with the entries list as its
        # argument
        ctk.CTkButton(self.frame, text='Submit', font=('arial', 15, 'bold'), command=lambda: self.add_employee_db(entries)).grid(row=8, column=1,
                                                                                                                                 pady=5)
        # Pack the frame widget to display all the widgets in it
        self.frame.pack(side='top', fill='both', pady=5, padx=5, expand=True)

    def add_employee_db(self, data):
        """
        Adds a new employee to the database or updates an existing employee record.

        Args:
        self (object): The tkinter object.
        data (list): A list of tkinter Entry objects.

        Returns: None
        """
        # create an empty list to hold the values of the employee data
        values = []

        # iterate over the list of tkinter Entry objects to check if any field is empty
        for value in data:
            # if the value is empty, show an error message and break the loop
            if value.get() == '':
                tkinter.messagebox.showerror('Empty Fields!', 'Fields cannot be empty!')
                break
            else:
                # if the value is not empty, append it to the values list
                values.append(value.get())
        else:
            # if no empty fields, convert values to a tuple to use in the SQL query
            tup_val = tuple(values)

            # if an existing employee record is being updated
            if self.UPDATE['Found']:
                _id = self.UPDATE['ID']
                # SQL query to update existing employee record with the new values
                update_query = "UPDATE emp_data SET fname=%s,lname=%s,gender=%s,jobposition=%s," \
                               "contact=%s,email=%s,address=%s WHERE id=%s"
                # execute the SQL query with the new values and the ID of the employee to update
                self.cursor.execute(update_query, (*tup_val, _id))
                connection.commit()
                # clear the UPDATE dictionary for next use
                self.UPDATE.update({'ID': '', 'Found': False})
                # show a success message to the user that the employee record has been updated
                tkinter.messagebox.showinfo('Updated!', 'Employee data has been updated successfully!')
            else:
                # SQL query to insert a new employee record with the values
                query = "INSERT INTO emp_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                # execute the SQL query with the new values
                self.cursor.execute(query, tup_val)
                connection.commit()
                # re-run add_employee() to recreate the new Employee ID and reset the form
                self.add_employee()
                # show a success message to the user that a new employee record has been added
                tkinter.messagebox.showinfo('Success!', 'New Employee has been added successfully!')

    def delete_employee(self, first_name, last_name):
        """
        This function retrieves the ID of the employee record to be deleted from the UPDATE dictionary and
        Delete an employee record from the database.

        Returns: None
        """
        # SQL query to select all employee data from the database
        select_data = "SELECT * FROM emp_data"

        # SQL query to delete an employee record from the database
        delete_record = "DELETE FROM emp_data WHERE id=%s"

        # get the ID of the employee record to be deleted from the UPDATE dictionary
        _id = self.UPDATE['ID']

        # execute the select_data SQL query to get all employee data from the database
        self.cursor.execute(select_data)
        data = self.cursor.fetchall()
        # iterate over all the employee records retrieved from the database
        for record in data:
            # check if the ID of the current record matches the ID of the employee record to be deleted
            if record[0] == _id:
                # prompt the user for confirmation to delete the employee record
                confirm = tkinter.messagebox.askyesno("Confirmation", "Are You Sure to Delete the Record?")
                # if the user confirms, execute the delete_record SQL query with the ID of the employee record to be deleted
                if confirm:
                    self.cursor.execute(delete_record, (_id,))
                    connection.commit()
                    # clear the entry widgets of search_employee
                    first_name.delete(0, tk.END)
                    last_name.delete(0, tk.END)
                    # display a success message to the user that the employee record has been deleted
                    tkinter.messagebox.showinfo('Deleted', 'Employee Record has been deleted Successfully!')
                    # reset the dictionary values to avoid resubmission of values
                    self.UPDATE = {'ID': '', 'Found': False}
                    break
                else:
                    # if the user cancels the deletion, break out of the loop
                    break

    def export_data(self):
        """
        Export all employee data from the database table 'emp_data' to a CSV file named 'emp_data.csv'.
        Display a success message to the user after successful export.

        Args:
            self: The instance of the class.

        Returns: None
        """
        # SQL query to select all employee data from the database
        self.cursor.execute("SELECT * FROM emp_data")

        # fetch all the data retrieved from the database
        data = self.cursor.fetchall()

        # get the column names of the database table
        header = self.cursor.column_names

        # open a new CSV file named "emp_data.csv" in write mode
        with open('emp_data.csv', mode='w', newline='') as file:
            # create a CSV writer object
            write = writer(file)
            # write the column names to the CSV file
            write.writerow(header)
            # write the employee data to the CSV file
            write.writerows(data)

        # display a success message to the user that the data has been exported successfully
        tkinter.messagebox.showinfo('Exported', 'Data has been exported Successfully!')

    def add_new_user(self):
        """
        Creates a form for adding a new user to the system

        The form includes the following fields:
        - Privilege selection dropdown
        - Username entry field
        - Password entry field
        - Add button (disabled by default)

        When the password is entered, a callback function is triggered to validate the password and enable the add button when it meets the criteria.

        Args:
            self: The instance of the class

        Returns: None
        """

        # Check if the frame exists and destroy it if it does
        if self.frame is not None:
            self.frame.destroy()

        # Create a list of values for the privilege dropdown
        values = ['Admin', 'User']

        # Create a StringVar to store the password value
        pass_value = tk.StringVar()

        # Create a new frame
        self.frame = ctk.CTkFrame(self.main)

        # Create a label and dropdown for the privilege selection
        ctk.CTkLabel(self.frame, text='Privilege: ', font=('lucid', 15)).grid(row=0, column=0, pady=5, padx=5)
        privilege = ctk.CTkComboBox(self.frame, font=('arial', 15), values=values, state='readonly')
        privilege.grid(row=0, column=1, pady=3)
        privilege.set(values[1])

        # Create a label and entry field for the username
        ctk.CTkLabel(self.frame, text='Username: ', font=('lucid', 15)).grid(row=1, column=0, pady=5, padx=5)
        username = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, placeholder_text='Username')
        username.grid(row=1, column=1, pady=5, padx=5)

        # Create a label and entry field for the password
        ctk.CTkLabel(self.frame, text='Password: ', font=('lucid', 15)).grid(row=2, column=0, pady=5, padx=5)
        password = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, show='*', textvariable=pass_value)
        password.grid(row=2, column=1, pady=5, padx=5)
        ctk.CTkLabel(self.frame, text='*Password Should Be\nLonger than 8 Characters', font=('lucid', 11)).grid(row=3, column=1, pady=2)

        # Create a button to add the new user and disable it by default
        add_btn = ctk.CTkButton(self.frame, text='Add', font=('arial', 15, 'bold'), width=100, state='disabled',
                                command=lambda: self.add_new_user_db(privilege, username, password))
        add_btn.grid(row=4, column=1, pady=10)

        # Place the frame in the center of the window
        self.frame.place(relx=0.6, rely=0.5, anchor='center')

        # Add a callback to validate the password and enable the add button when it meets the criteria
        pass_value.trace(mode='w', callback=lambda *args: self.validate_password(pass_value.get(), add_btn, *args))

    def add_new_user_db(self, _privilege, _username, _password):
        """
        Adds a new user to the user_login table in the database.

        Args:
            _privilege : A customtkinter ComboBox containing the selected privilege for the new user.
            _username : A customtkinter Entry widget containing the new user's desired username.
            _password : A customtkinter Entry widget containing the new user's desired password.

        Returns: None
        Raises: None
        """
        # check if username field is not empty
        if not _username.get() == '':
            # if privilege is admin, ask for confirmation to continue
            if _privilege.get() == "Admin":
                confirm = tkinter.messagebox.askyesno("Confirmation", "Admin Will have All the Rights to Management System\n"
                                                                      "Are You Sure to Continue?")
            # if privilege is user, ask for confirmation and show the user what actions they are allowed to perform
            else:
                confirm = tkinter.messagebox.askyesno("Confirmation", "User will be allowed to:\n"
                                                                      "1- See All Employees Data\n"
                                                                      "2- Add a New Employee\n"
                                                                      "3- Update Employee's Data\n"
                                                                      "4- Export all Data\n"
                                                                      "Are you sure to Add a New Authentication User?\n")
            # if confirmation is given, add the new user to the database
            if confirm:
                add_query = "INSERT INTO user_login VALUES (%s, %s, %s)"
                self.cursor.execute(add_query, (_privilege.get(), _username.get(), _password.get()))
                connection.commit()
                # clear the input fields
                _username.delete(0, tk.END)
                _password.delete(0, tk.END)
                # show success message
                tkinter.messagebox.showinfo("Success!", "User has been added successfully!")
        # if username field is empty, show error message
        else:
            tkinter.messagebox.showerror("ERROR!", "Username Can not be Empty!")

    def change_password(self):
        """
        This function creates a new frame to change the user's password.
        The change button is initially disabled until the user enters a valid password.
        When the user enters a valid password, the change button is enabled and
        can be clicked to change the user's password in the database.
        """

        # Destroy the existing frame if there is one
        if self.frame is not None:
            self.frame.destroy()

        # Create a new string variable for password field
        pass_value = tk.StringVar()

        # Create a new frame and add username and password fields and a change button
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
                                   command=lambda: self.change_password_db(username.get(), password.get()))
        change_btn.grid(row=3, column=1, pady=10)

        # Place the frame on the center right of the main window
        self.frame.place(relx=0.6, rely=0.5, anchor='center')

        # Add a callback function to the password field to enable/disable the change button
        # depending on the length of the password
        pass_value.trace(mode='w', callback=lambda *args: self.validate_password(pass_value.get(), change_btn, *args))

    def validate_password(self, *args):
        """
        This function is a callback function for the password field's textvariable.
        It enables/disables the change button based on the length of the password.
        """
        pass_ = args[0]
        button = args[1]
        if len(pass_) >= 8:
            button.configure(state='normal')
        else:
            button.configure(state='disabled')

    def change_password_db(self, _username, _password):
        """
        This function updates the password of the currently logged-in user in the database.
        If the password is empty, it shows an error message.
        """
        change_password_query = "UPDATE user_login SET password=%s WHERE user_name=%s"
        self.cursor.execute(change_password_query, (_password, _username))
        connection.commit()
        tkinter.messagebox.showinfo('Success!', 'Your Password Has Been Changed Successfully!')
        _password.delete(0, tk.END)

    def logout(self):
        """
        This function logs out the currently logged-in user by destroying all the widgets in the main frame and
        calling the main function to start the login screen again.
        """
        confirm = tkinter.messagebox.askyesno('Confirm', 'Are you Sure to Logout?')
        if confirm:
            # Destroy all the widgets in the main frame
            for widget in self.main.winfo_children():
                widget.destroy()
            # Call the main function to start the login screen again
            main(self.main)

    def search_employee(self, check=0):
        """
        This method creates a GUI to search for an employee by first name and last name.

        Args:
            check (int): Optional argument to indicate if this search is being performed as part of a data modification.
                        Defaults to 0.

        Returns: None
        """
        # If there is an existing search GUI, destroy it and reset the UPDATE dictionary.
        if self.frame is not None:
            self.frame.destroy()
            self.UPDATE = {'ID': '', 'Found': False}

        # Create a new frame for the search GUI.
        self.frame = ctk.CTkFrame(self.main)

        # Add a label and entry widget for the employee's first name.
        ctk.CTkLabel(self.frame, text='First Name: ', font=('lucid', 15)).grid(row=0, column=0, pady=5, padx=5)
        first_name = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, placeholder_text='First Name')
        first_name.grid(row=0, column=1, pady=5, padx=5)

        # Add a label and entry widget for the employee's last name.
        ctk.CTkLabel(self.frame, text='Last Name: ', font=('lucid', 15)).grid(row=1, column=0, pady=5, padx=5)
        last_name = ctk.CTkEntry(self.frame, font=('lucid', 15), width=150, placeholder_text='Last Name')
        last_name.grid(row=1, column=1, pady=5, padx=5)

        # Add a button to initiate the search using the employee's first and last name.
        # The lambda function passes the first and last name to the modify_data() method.
        ctk.CTkButton(self.frame, text='Search', font=('arial', 15, 'bold'), width=100,
                      command=lambda: self.modify_data(first_name, last_name, check)) \
            .grid(row=3, column=1, pady=10)

        # Position the search GUI in the center of the main window.
        self.frame.place(relx=0.6, rely=0.5, anchor='center')

    def search_employee_db(self, f_name, l_name):
        """
        Searches for an employee with the given first and last name in the database and updates the UPDATE dictionary
        with the employee's ID and sets the 'Found' key to True if found, or displays an error message if not found.

        param f_name: str, the first name of the employee to search for
        param l_name: str, the last name of the employee to search for
        return: None
        """
        # SQL query to fetch all employee data
        query = "SELECT id,fname,lname FROM emp_data"
        self.cursor.execute(query)
        values = self.cursor.fetchall()

        # Loop through all the employee data and check if the first and last name match with the given input
        for data in values:
            if data[1] == f_name.get() and data[2] == l_name.get():
                # If found, update the UPDATE dictionary with the employee's ID and set the 'Found' key to True
                self.UPDATE.update({'ID': data[0], 'Found': True})
                break
        else:
            # If not found, display an error message
            tkinter.messagebox.showerror('Not Found!', 'No Such Employee with Given Data!')

    def modify_data(self, f_name, l_name, check):
        """
        Function to modify employee data based on first name and last name

        Args:
            f_name (entry): First name of the employee
            l_name (entry): Last name of the employee
            check (int): Integer value to check if the function is called to update or delete an employee

        Returns: None
        """

        # Call function to search for employee data
        self.search_employee_db(f_name, l_name)

        # If check value is 1, call function to add employee if data is found
        if check:
            if self.UPDATE['Found']:
                self.add_employee()
        # If check value is 0, call function to delete employee if data is found
        else:
            if self.UPDATE['Found']:
                self.delete_employee(f_name, l_name)


def main(root):
    """
    A function that sets up the admin login GUI.

    :param root: A Tkinter object representing the root window.
    """
    # Create an instance of the AdminLogin class
    admin = AdminLogin()

    # Define the function that is called when the login button is clicked
    def clicked():
        """
        This function is called when the login button is clicked. It retrieves the username and password from the entry
        fields, calls the login() function of AdminLogin class to verify the credentials and determine the user role.
        It then opens the appropriate panel based on the user role.

        :return: None
        """

        # Call login function of AdminLogin class to verify the credentials and determine the user role
        authorized = admin.login(user_entry.get(), pass_entry.get())

        if authorized:
            role = admin.PRIVILEGE
            current_user = admin.CURRENT_USER

            # Open AdminPanel with appropriate admin privileges based on user role
            if role == "Admin":
                AdminPanel(window=root, admin=True, current=current_user)
            else:
                AdminPanel(window=root, admin=False, current=current_user)

        else:
            # Display error message and ask for retry or cancel
            ask_retry = tkinter.messagebox.askretrycancel("Wrong Credentials!", "Username or Password is Incorrect!")

            # If user wants to retry, clear the entry fields and wait for input again
            if ask_retry:
                user_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)
                user_entry.update()
                pass_entry.update()

            # If user cancels, exit the program
            else:
                exit()

    app_width = 300  # Set the width of the application window
    app_height = 180  # Set the height of the application window

    # Center the application window on the screen
    x = (root.winfo_screenwidth() / 2) - (app_width / 2)
    y = (root.winfo_screenheight() / 2) - (app_height / 2)

    # Set the window geometry, title, and icon
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    root.resizable(False, False)
    root.iconbitmap('images/icon.ico')
    root.title('Admin Login')

    # Create a Tkinter BooleanVar to track the password visibility state
    show_pass = tk.BooleanVar(value=True)

    # Create a custom Tkinter Frame and add UI elements to it
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
    f.pack(pady=15, ipadx=10, ipady=20)  # Pack the custom Tkinter Frame into the root window

    # Start the main event loop of the Tkinter application
    root.mainloop()


# Define the entry point for the script
if __name__ == '__main__':

    # Try to connect to the database, and handle any potential errors
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='employee-management')
    except mysql.connector.errors.ProgrammingError:
        # Handle the case where the database doesn't exist, or the credentials are wrong
        tkinter.messagebox.showerror("Database ERROR!", "1- Database 'employee-management' Doesn't Exists\n"
                                                        "2- Wrong 'user' OR 'password'\n"
                                                        "Try to Check Database and Credentials OR Contact the Developer")
        # Exit the program
        exit()
    except mysql.connector.errors.InterfaceError:
        # Handle the case where the connection to the database cannot be established
        tkinter.messagebox.showerror("Connection ERROR!", "Unable to Connect to Database 'employee-management'\n"
                                                          "Try to Check Connection and Retry")
        # Exit the program
        exit()
    except Exception as error:
        # Handle any other errors that may occur
        tkinter.messagebox.showerror("ERROR!", f"An Unhandled Error!\n{error}\nPlease Contact the Developer")
        # Exit the program
        exit()

    # Set the appearance mode and color theme for the tkinter application
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    # Create the tkinter application
    app = ctk.CTk()
    app.configure(background='grey')

    # Call the main() function of the app
    main(root=app)
