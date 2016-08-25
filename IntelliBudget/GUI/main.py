""" Main GUI file. Launches all other widgets. """

import tkinter as tk
import tkinter.messagebox

from . import style as sty
from .constants import TITLE, MONTH, fonts, debug
from .menu import Menu
from .budgetdata import BudgetData
from .newlimits import NewLimits
from .expensedisplay import ExpenseDisplay

from .. import budget
from ..budget import NoneNotAllowed


class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        FIRST_USE = False

        try:
            self.Budget = budget.Budget()
        except NoneNotAllowed:
            FIRST_USE = True
            self.Budget = budget.Budget(0)

        self.master = master
        self.master.title(TITLE)

        Menu(self)

        row = 0

        self.topFrame = tk.Frame(self)
        self.topFrame.grid(row=row, columnspan=5); row += 1

        self.TopTitle(self.topFrame)

        # frame1 is the leftmost frame
        frame1 = tk.Frame(self, width=700, height=200)
        frame1.grid(row=row, column=0)

        frame1_Lbuffer = tk.Frame(frame1, width=sty.width)
        frame1_Lbuffer.pack(side='left')
        frame1_Rbuffer = tk.Frame(frame1, width=sty.width)
        frame1_Rbuffer.pack(side='right')

        self.BD = BudgetData(frame1, self.Budget)
        self.BD.pack()

        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=row, column=1)

        self.ED = ExpenseDisplay(self.frame2, self)
        self.ED.pack()

        self.frame3 = tk.Frame(self, width=200, height=200)
        self.frame3.grid(row=row, column=2)

        # Left buffer for fframe3
        self.frame3_Lbuffer = tk.Frame(self.frame3, width=sty.width)
        self.frame3_Lbuffer.grid()

        # Right buffer for fframe3
        self.frame3_Rbuffer = tk.Frame(self.frame3, width=sty.width)
        self.frame3_Rbuffer.grid(column=100)

        # frame3 is used for the Expense form
        self.form_frame = tk.Frame(self.frame3)
        self.form_frame.grid(row=0, column=1)
        self.ExpenseForm(self.form_frame)

        # frame3 is used for Submit button.
        # Spacing is added by creating multiple inner frames within frame3.
        self.submit_frame = tk.Frame(self.frame3)
        self.submit_frame.grid(row=1, column=1)
        self._createSubmit(self.submit_frame)

        # Asks user to setup limits if this is the first time the program's
        # been run this month.
        if FIRST_USE:
            message = "It looks like this is your first time using {0} in " \
                      "the month of {1}! \n\nBefore you get started, let's " \
                      "setup this month's spending limits!"
            message = message.format(TITLE, MONTH)

            tkinter.messagebox.showinfo("FIRST USE IN " + MONTH + "!!!",
                                        message)
            NL = NewLimits(self)
            NL.Make()

    def TopTitle(self, frame):
        TopTitle = tk.Label(frame,
                            text=TITLE,
                            font='Verdana 40 underline')
        TopTitle.pack(side='top')
        TT_bbuffer = tk.Frame(frame, height=20)
        TT_bbuffer.pack(side='bottom')


    def ExpenseForm(self, frame):
        """ Creates the form that the user uses to input a new expense into
        the database.
        """
        OPTIONS = ['Food', 'Entertainment', 'Monthly Bills', 'Fuel', 'Other']

        frame = tk.Frame(frame)
        frame.grid(row=0, column=1)

        row = 0

        text = "New Expense"
        ExpenseFormTitle = tk.Label(frame, text=text,
                                    font=fonts.title())
        ExpenseFormTitle.grid(row=row, columnspan=2); row += 1

        # Bottom buffer space between expense form title and the actual form
        ETitle_bbuffer = tk.Frame(frame, height=5)
        ETitle_bbuffer.grid(row=row); row += 1

        self.expense_choice = tk.StringVar(frame)

        # Setting the default value
        self.expense_choice.set('Food')

        ExpenseOptions = tk.OptionMenu(frame, self.expense_choice, *OPTIONS)

        def DropdownConfigs():
            """ Sets all dropdown configurations """

            arrow = tk.PhotoImage(file='img/arrow.gif')

            # Config options for the dropdown expense box
            ExpenseOptions.config(indicatoron=0,
                                  activebackground=sty.abcolor,
                                  compound='right',
                                  image=arrow)

            # Needed or the image will not appear
            ExpenseOptions.image = arrow

            # Config options for the menu items in the dropdown expense box
            ExpenseOptions['menu'].config(activebackground=sty.abcolor)

        DropdownConfigs()

        # Dropdown width and expense width, respectively
        dwidth = 115
        ewidth = 18

        Lab_Expense_Type = tk.Label(frame, text='Expense Type: ')
        Lab_Expense_Type.grid(row=row, column=0)
        ExpenseOptions.grid(row=row, column=1)
        row += 1

        # Amount Label
        Lab_Amount = tk.Label(frame, text='Amount: ')
        Lab_Amount.grid(row=row, column=0)

        self.ValueEntry = tk.Entry(frame)
        self.ValueEntry.bind('<Return>', self.SubmitFuncBind)
        self.ValueEntry.grid(row=row, column=1)
        row += 1

        Lab_Notes = tk.Label(frame, text='Notes: ')
        Lab_Notes.grid(row=row, column=0)

        self.NotesEntry = tk.Entry(frame)
        self.NotesEntry.bind('<Return>', self.SubmitFuncBind)
        self.NotesEntry.grid(row=row, column=1)
        row += 1

        # Set widths of all entrys and dropdowns
        ExpenseOptions.config(width=dwidth)
        self.ValueEntry.config(width=ewidth)
        self.NotesEntry.config(width=ewidth)

    def _createSubmit(self, frame):
        """ Creates the Expense form Submit button """

        # submit_Tbuffer is used to create vertical space between the submit
        # button and the expense form.
        submit_Tbuffer = tk.Frame(frame, height=15)
        submit_Tbuffer.grid(row=0, column=1)

        # submit_Lbuffer is used to create horizontal space between the submit
        # button and the expense list.
        submit_Lbuffer = tk.Frame(frame, width=100)
        submit_Lbuffer.grid(row=1, column=0)

        # In order to have complete control of the Submit button's horizontal
        # positioning, the columns of frame3 must be seperate from the columns
        # in the Submit button's encapsulating frame. The submit_container
        # fulfills this purpose.
        submit_container = tk.Frame(frame)
        submit_container.grid(row=1, column=1)

        SubmitButton = tk.Button(submit_container,
                                 text='Submit',
                                 activebackground=sty.abcolor,
                                 command=self.SubmitFunc,
                                 font=fonts.button())
        SubmitButton.grid()


    def SubmitFunc(self):
        """ This function is called if the Expense form's 'Submit' button
        is pressed.
        """
        try:
            self.Budget.add_expense('DATE', self.expense_choice.get(),
                                    self.ValueEntry.get(),
                                    self.NotesEntry.get())

            self.ValueEntry.delete(0, 'end')
            self.NotesEntry.delete(0, 'end')

            self.refresh_screen()

        except AttributeError:
            tkinter.messagebox.showinfo("ERROR",
                                        "You must select an expense type!")
            raise

        # Catches error if user enters string into 'Value' entrybox
        except ValueError:
            message = "The formatting of this entry is invalid!"
            tkinter.messagebox.showinfo("ERROR", message)

            raise

    def SubmitFuncBind(self, event):
        """ Used to allow 'Entry' widgets to bind to the SubmitFunc. Binded
        widgets require that the function they are binded to have an 'event'
        argument.
        """
        self.SubmitFunc()

    def refresh_screen(self):
        """ This function is used to refresh the main GUI window. """
        self.master.title(TITLE)
        self.BD.set_dynamic_data()
        self.ED.Make()
