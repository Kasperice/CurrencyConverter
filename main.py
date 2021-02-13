import tkinter as tk
from tkinter import ttk
from currency_converter import CurrencyRates
from tkcalendar import DateEntry
import datetime


c = CurrencyRates()
choices = [f"{element} - {c.translate_currency_symbol(element)}" for element in list(c.get_latest_rates('EUR').keys())]
choices.append("EUR - Euro")


def display(quantity_field, currency1, currency2, results_field):
    if get_currency_symbol(currency1) != get_currency_symbol(currency2):
        results_field.configure(text=f"{get_quantity(quantity_field)} {get_currency_symbol(currency1)} is equal to "
                                     f"{get_quantity(quantity_field) * get_latest_rate(c, currency1, currency2):.2f} "
                                     f"{get_currency_symbol(currency2)}")
    else:
        results_field.configure(text=f"Both currencies are the same, please change one.")


def display_hist(quantity_field, currency1, currency2, results_field, date):
    if get_currency_symbol(currency1) != get_currency_symbol(currency2):
        results_field.configure(text=f"{get_quantity(quantity_field)} {get_currency_symbol(currency1)} is equal to "
                                f"{get_quantity(quantity_field) * get_historical_rate(c, currency1, currency2, date):.2f} "
                                f"{get_currency_symbol(currency2)}")
    else:
        results_field.configure(text=f"Both currencies are the same, please change one.")


def clear(currency1, currency2, results_field, quantity_field, calendar_field=None):
    results_field.configure(text="")
    currency1.set("EUR - Euro")
    currency2.set("PLN - Polish Zloty")
    quantity_field.delete(0, 'end')
    quantity_field.insert(0, 1.0)
    if calendar_field:
        calendar_field.set_date(datetime.date.today().strftime("%-m/%-d/%y"))


def exit_converter():
    form.quit()


def get_currency_symbol(field):
    return field.get().split()[0]


def get_latest_rate(converter, currency1, currency2):
    return converter.get_latest_rate(get_currency_symbol(currency1), get_currency_symbol(currency2))


def get_historical_rate(converter, currency1, currency2, date):
    return converter.get_historical_rate(get_currency_symbol(currency1), get_currency_symbol(currency2), get_date(date))


def get_date(field):
    date = field.get()
    date = datetime.datetime.strptime(date, '%m/%d/%y')
    return date.strftime('%Y-%m-%d')


def get_quantity(field):
    return float(field.get())


form = tk.Tk()
form.title('Kasper\'s currency converter')
form.geometry("500x200")
tab_parent = ttk.Notebook(form)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Current Rates")
tab_parent.add(tab2, text="Historical Rates")

tab1_left = ttk.Frame(tab1)
tab1_right = ttk.Frame(tab1)

tab1_left.columnconfigure(0, weight=1)
tab1_left.columnconfigure(0, weight=3)

variable = tk.StringVar(tab1_left)
variable1 = tk.StringVar(tab1_left)
variable.set("EUR - Euro")
variable1.set("PLN - Polish Zloty")

ttk.Label(tab1_left, text='Quantity:').grid(column=0, row=0, sticky=tk.W)
quantity = ttk.Entry(tab1_left)
quantity.insert(0, 1.0)

ttk.Label(tab1_left, text='Currency 1:').grid(column=0, row=1, sticky=tk.W)
currency_1 = ttk.Combobox(tab1_left, textvariable=variable, values=choices)

ttk.Label(tab1_left, text='Currency 2:').grid(column=0, row=2, sticky=tk.W)
currency_2 = ttk.Combobox(tab1_left, textvariable=variable1, values=choices)

ttk.Label(tab1_left, text='Result:').grid(column=0, row=3, sticky=tk.W)
labelTest = ttk.Label(tab1_left, text="")


quantity.grid(column=1, row=0, sticky=tk.W)
currency_1.grid(column=1, row=1, sticky=tk.W)
currency_2.grid(column=1, row=2, sticky=tk.W)
labelTest.grid(column=1, row=3, sticky=tk.W)

for widget in tab1_left.winfo_children():
    widget.grid(padx=0, pady=3)

tab1_right.columnconfigure(0, weight=1)

ttk.Button(tab1_right,
           text='1 -> 2',
           command=lambda: display(quantity, currency_1, currency_2, labelTest)).grid(column=0, row=0)
ttk.Button(tab1_right,
           text='1 <- 2',
           command=lambda: display(quantity, currency_2, currency_1, labelTest)).grid(column=0, row=1)
ttk.Button(tab1_right,
           text='Clear',
           command=lambda: clear(variable, variable1, labelTest, quantity)).grid(column=0, row=2)
ttk.Button(tab1_right,
           text='Exit',
           command=exit_converter).grid(column=0, row=3)

for widget in tab1_right.winfo_children():
    widget.grid(padx=0, pady=7)

tab1_left.columnconfigure(0, weight=1)
tab1_left.columnconfigure(0, weight=3)

tab1_left.grid(column=0, row=0)
tab1_right.grid(column=1, row=0)

tab1.columnconfigure(0, weight=4)
tab1.columnconfigure(1, weight=1)


tab2_left = ttk.Frame(tab2)
tab2_right = ttk.Frame(tab2)

tab2_left.columnconfigure(0, weight=1)
tab2_left.columnconfigure(0, weight=3)

variable2 = tk.StringVar(tab2_left)
variable3 = tk.StringVar(tab2_left)
variable2.set("EUR - Euro")
variable3.set("PLN - Polish Zloty")

ttk.Label(tab2_left, text='Date:').grid(column=0, row=0, sticky=tk.W)
cal = DateEntry(tab2_left, background='darkblue', foreground='white', borderwidth=2)

ttk.Label(tab2_left, text='Quantity:').grid(column=0, row=1, sticky=tk.W)
quantity_history = ttk.Entry(tab2_left)
quantity_history.insert(0, 1.0)

ttk.Label(tab2_left, text='Currency 1:').grid(column=0, row=2, sticky=tk.W)
currency_history_1 = ttk.Combobox(tab2_left, textvariable=variable2, values=choices)

ttk.Label(tab2_left, text='Currency 2:').grid(column=0, row=3, sticky=tk.W)
currency_history_2 = ttk.Combobox(tab2_left, textvariable=variable3, values=choices)

ttk.Label(tab2_left, text='Result:').grid(column=0, row=4, sticky=tk.W)
labelTest2 = ttk.Label(tab2_left, text="")


cal.grid(column=1, row=0, sticky=tk.W)
quantity_history.grid(column=1, row=1, sticky=tk.W)
currency_history_1.grid(column=1, row=2, sticky=tk.W)
currency_history_2.grid(column=1, row=3, sticky=tk.W)
labelTest2.grid(column=1, row=4, sticky=tk.W)

for widget in tab2_left.winfo_children():
    widget.grid(padx=0, pady=5)

tab2_right.columnconfigure(0, weight=1)

ttk.Button(tab2_right,
           text='1 -> 2',
           command=lambda: display_hist(quantity_history, currency_history_1, currency_history_2, labelTest2, cal)).grid(column=0, row=0)
ttk.Button(tab2_right,
           text='1 <- 2',
           command=lambda: display_hist(quantity_history, currency_history_2, currency_history_1, labelTest2, cal)).grid(column=0, row=1)
ttk.Button(tab2_right,
           text='Clear',
           command=lambda: clear(variable2, variable3, labelTest2, quantity_history, cal)).grid(column=0, row=2)
ttk.Button(tab2_right,
           text='Exit',
           command=exit_converter).grid(column=0, row=3)

for widget in tab2_right.winfo_children():
    widget.grid(padx=0, pady=7)

tab2_left.grid(column=0, row=0)
tab2_right.grid(column=1, row=0)

tab2.columnconfigure(0, weight=4)
tab2.columnconfigure(1, weight=1)


tab_parent.pack(expand=1, fill='both')
form.mainloop()
