import tkinter
from tkinter import ttk, messagebox
from cities import NCR_cities
import datetime

"""
Getting Data from Data Entry Form
"""
def get_loan_details():
    try:
        principal = float(principal_entry.get().replace(',', ''))
        interest_rate = float(interest_rate_string.get().replace('%', '')) / 100
        term = int(numberofpayment_entry.get())
        monthly_payment = float(monthly_payment_entry.get().replace(',', ''))

        if principal <= 0 or term <= 0 or monthly_payment <= 0:
            print("Principal or term is <= 0")
            messagebox.showerror(title='Error', message='Invalid numerical input')
            return None
        
        print("Returning loan details")
        return principal, interest_rate, term, monthly_payment
    except ValueError:
        print("ValueError caught")
        messagebox.showerror(title='Error', message='Invalid numerical input')
        return None

"""
Generating Payment Schedule Table
"""
def generate_table():
    loan_details = get_loan_details()
    if loan_details is None:
        return
    principal, interest_rate, term, monthly_payment = loan_details

    payment_schedule_window = tkinter.Toplevel()
    payment_schedule_window.title('Payment Schedule')

    schedule_frame = tkinter.Frame(payment_schedule_window)
    schedule_frame.pack()

    """
    Loan Details
    """
    legend = ttk.Treeview(schedule_frame, columns=('parameters', 'input'))
    legend.column('parameters', width=150, anchor='w')
    legend.column('input', width=150, anchor='e')
    legend['show'] = 'headings'
    legend.heading('parameters')
    legend.heading('input')
    legend.insert('', 'end', values=('Name', f'{first_name_entry.get()} {last_name_entry.get()}'))
    legend.insert('', 'end', values=('Principal', f'{principal:,.2f}'))
    legend.insert('', 'end', values=('Interest Rate', f"{interest_rate:.2%}"))
    legend.insert('', 'end', values=('Term', term))
    legend.insert('', 'end', values=('Monthly Payment', f'{monthly_payment:,.2f}'))

    legend.pack(fill='both', expand=True)

    """
    Payment Schedule
    """

    table = ttk.Treeview(schedule_frame, 
                         columns=('date', 'amount_due', 'balance', 'interest_on_balance', 'interest_amount', 'total_obligation'),
                         show='headings')
    
    table.heading("date", text="Date")
    table.heading("amount_due", text="Amount Due")
    table.heading("balance", text="Balance After Payment")
    table.heading("interest_on_balance", text="Interest on Balance")
    table.heading("interest_amount", text="Amount of Interest")
    table.heading("total_obligation", text="Total Obligation")

    """
    Computation of table entries
    """
    total_obligation = principal + float(initial_interest_string.get().replace(',', ''))
    initial_interest = float(initial_interest_entry.get().replace(',', ''))
    interest_amount = initial_interest

    amount_due = monthly_payment
    start_date = datetime.date.today()
    date_option = period_payment_combobox.get()

    def get_next_date(current_date):
        if date_option == "every 15th":
            next_month = current_date.replace(day=1) + datetime.timedelta(days=32)
            return next_month.replace(day=15)
        elif date_option == "every end of the month":
            next_month = current_date.replace(day=1) + datetime.timedelta(days=32)
            return next_month - datetime.timedelta(days=1)
        else:
            return None
    
    current_date = start_date
    table.insert('', 'end', values=(current_date,
                                    '0.00',
                                    f'{principal:,.2f}',
                                    f'{interest_rate:.2%}',
                                    f'{initial_interest_entry.get()}',
                                    f'{total_obligation:,.2f}'
                                    )
                )
    current_date = get_next_date(current_date)
    
    while total_obligation > 0:
        balance  = total_obligation - amount_due
        interest_amount = balance * interest_rate
        total_obligation = balance + interest_amount

        if current_date:
            date_str = current_date.strftime("%Y-%m-%d")
        else:
            date_str = ''
        
        data = (date_str, f'{amount_due:,.2f}', f'{balance:,.2f}', f'{interest_rate:.2%}', f'{interest_amount:,.2f}', f'{total_obligation:,.2f}')
        table.insert('', 'end', values=data)
        current_date = get_next_date(current_date)
        if total_obligation < amount_due:
            amount_due = total_obligation

    table.pack(fill="both", expand=True)

    # Make the window modal
    payment_schedule_window.grab_set()

    # Define what happens when the window is closed
    payment_schedule_window.protocol("WM_DELETE_WINDOW", payment_schedule_window.destroy)
    
    return payment_schedule_window

def check_membership():
    if reg_member_var.get() == 'Not Member':
        interest_rate_string.set('3%')
    else:
        interest_rate_string.set('1%')
    compute_interest()

def format_principal(*args):
    #Format principal
    value = principal_string.get()
    value = ''.join(char for char in value if char.isdigit())
    try:
        value = int(value)
        formatted_value = f"{value:,}" #Adds a thousand operator
    except ValueError:
        formatted_value = ""
    principal_string.set(formatted_value)
    compute_interest()

def format_monthly(*args):
    #Format principal
    value = monthly_string.get()
    value = ''.join(char for char in value if char.isdigit())
    try:
        value = int(value)
        formatted_value = f"{value:,}" #Adds a thousand operator
    except ValueError:
        formatted_value = ""
    monthly_string.set(formatted_value)

def compute_interest():
    try:
        interest_rate = float(interest_rate_string.get().replace('%', '')) / 100
        principal = int(principal_string.get().replace(',', ''))
        initial_interest = principal * interest_rate
        formatted_interest = f"{initial_interest:,.2f}"
        initial_interest_string.set(formatted_interest)
    except ValueError:
        initial_interest_string.set("")


#window
window = tkinter.Tk()
window.title('Data Entry')


frame = tkinter.Frame(window)
frame.pack()

"""
User Info Frame
"""
user_info_frame = tkinter.LabelFrame(frame, text='User Infromation')
user_info_frame.grid(row=0, column=0, padx=20, pady=20)

first_name_label = tkinter.Label(user_info_frame, text='First Name')
first_name_entry = tkinter.Entry(user_info_frame)
last_name_label = tkinter.Label(user_info_frame, text='Surname')
last_name_entry = tkinter.Entry(user_info_frame)
age_label = tkinter.Label(user_info_frame, text='Age')
age_entry = tkinter.Spinbox(user_info_frame, from_=18, to=100)
city_label = tkinter.Label(user_info_frame, text='City')
city_combobox = ttk.Combobox(user_info_frame, values=NCR_cities)

reg_member_var = tkinter.StringVar(value='Not Member')
registered_member_check = tkinter.Checkbutton(user_info_frame, text='Current Member', variable=reg_member_var,
                                              onvalue='Member', offvalue='Not Member', command=check_membership)

first_name_label.grid(row=0, column=0, sticky='nws')
first_name_entry.grid(row=1, column=0)
last_name_label.grid(row=0, column=1, sticky='nws')
last_name_entry.grid(row=1, column=1)
age_label.grid(row=2, column=0, sticky='nws')
age_entry.grid(row=3, column=0)
city_label.grid(row=2, column=1, sticky='nws')
city_combobox.grid(row=3, column=1)
registered_member_check.grid(row=4, column=0, sticky='nws')

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

"""
Loan Info
"""
loan_infro_frame = tkinter.LabelFrame(frame, text='Loan Details')
loan_infro_frame.grid(row=1, column=0, sticky='news', padx=20, pady=20)

principal_label = tkinter.Label(loan_infro_frame, text='Principal Amount')
principal_string = tkinter.StringVar()
principal_string.trace_add('write', format_principal)
principal_entry = tkinter.Entry(loan_infro_frame, textvariable=principal_string)

monthly_payment_label = tkinter.Label(loan_infro_frame, text='Monthly Payment')
monthly_string = tkinter.StringVar()
monthly_string.trace_add('write', format_monthly)
monthly_payment_entry = tkinter.Entry(loan_infro_frame, textvariable=monthly_string)


initial_interest_label = tkinter.Label(loan_infro_frame, text='Initial Interest')
initial_interest_string = tkinter.StringVar()
initial_interest_entry = tkinter.Entry(loan_infro_frame, state='readonly', textvariable=initial_interest_string)


interest_rate_label = tkinter.Label(loan_infro_frame, text='Interest Rate')
interest_rate_string = tkinter.StringVar()
check_membership()
interest_rate_entry = tkinter.Entry(loan_infro_frame, textvariable=interest_rate_string, state='disabled')

numberofpayment_label = tkinter.Label(loan_infro_frame, text='Number of Payments')
numberofpayment_entry = tkinter.Entry(loan_infro_frame)

period_payment_label = tkinter.Label(loan_infro_frame, text='Period of Payment')
period_payment_combobox = ttk.Combobox(loan_infro_frame, values=['', 'every 15th', 'every end of the month'])
period_payment_combobox.bind("<<ComboboxSelected>>", generate_table)
period_payment_combobox['state']='readonly'

principal_label.grid(row=0, column=0, sticky='nws')
principal_entry.grid(row=1, column=0)
monthly_payment_label.grid(row=2, column=0, sticky='nws')
monthly_payment_entry.grid(row=3, column=0)
numberofpayment_label.grid(row=4, column=0, sticky='nws')
numberofpayment_entry.grid(row=5,column=0)
period_payment_label.grid(row=6, column=0, sticky='nws')
period_payment_combobox.grid(row=7, column=0)
interest_rate_label.grid(row=0, column=1, sticky='nws')
interest_rate_entry.grid(row=1, column=1)
initial_interest_label.grid(row=2, column=1, sticky='nws')
initial_interest_entry.grid(row=3, column=1)

generate_table_button = tkinter.Button(loan_infro_frame, text='Generate Table', width=20, height=4, command=generate_table)
generate_table_button.grid(row=5, column=1, rowspan=4)

for widget in loan_infro_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)




#run window
window.mainloop()