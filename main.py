from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import urllib.request
import xml.dom.minidom
import matplotlib.pyplot as plt

site = 'https://www.cbr.ru/scripts/XML_daily.asp'
response = urllib.request.urlopen(site)

dom = xml.dom.minidom.parse(response)
dom.normalize()
node_array = dom.getElementsByTagName("Valute")

data = {}
names = []

for node in node_array:
    arr = []
    name = ''
    arr.append(node.getAttribute('ID'))
    child_list = node.childNodes

    for child in child_list:
        if child.nodeName == 'Name':
            name = child.childNodes[0].nodeValue
            names.append(child.childNodes[0].nodeValue)
        elif child.nodeName == 'Value':
            arr.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
        else:
            arr.append(child.childNodes[0].nodeValue)
    data[name] = arr

result_label_1 = None
result_label_2 = None


def calc():
    global result_label_1, result_label_2

    try:
        val_1 = combo.get()
        val_2 = combo2.get()

        if not val_1 or not val_2:
            messagebox.showwarning("Ошибка", "Выберите обе валюты.")
            return

        amount = float(txt.get())
        koef = data[val_1][-2] / data[val_2][-2]
        result = amount * koef

        if result_label_1:
            result_label_1.destroy()
        if result_label_2:
            result_label_2.destroy()

        result_label_1 = Label(tab1, text=f"Результат: {result:.3f}")
        result_label_1.grid(column=2, row=1, columnspan=2, sticky='w', padx=5, pady=2)

        result_label_2 = Label(tab1, text=f"Курс: 1 {val_1} = {koef:.3f} {val_2}")
        result_label_2.grid(column=2, row=2, columnspan=2, sticky='w', padx=5, pady=2)

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Введите корректное число.")


combo_period_arr = [
    {'1 неделя апрель 2024': ('07/04/2024', '01/04/2024'),
     '3 неделя апрель 2024': ('21/04/2024', '14/04/2024')},

    {'Апрель 2024': ('30/04/2024', '01/04/2024'), 'Март 2024': ('31/03/2024', '01/03/2024'),
     'Февраль 2024': ('29/02/2024', '01/02/2024')},

    {'1 квартал 2024': ('31/03/2024', '01/01/2024'), '4 квартал 2023': ('31/12/2023', '01/09/2023'),
     '3 квартал 2023': ('30/09/2023', '01/06/2023')},

    {'2023': ('01/01/2024', '01/01/2023'), '2022': ('01/01/2023', '01/01/2022'), '2021': ('01/01/2022', '01/01/2021')}
]


def period():
    a = lang.get()
    combo_period['value'] = [i for i in combo_period_arr[int(a)]]


def graph():
    plt.close()
    id = data[combo_gr.get()][0]

    if not combo_period.get():
        messagebox.showerror("Ошибка", "Выберите период")
        return
    if not combo_gr.get():
        messagebox.showerror("Ошибка", "Выберите валюту")
        return

    a = combo_period_arr[int(lang.get())][combo_period.get()]
    graf_data = f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={a[1]}&date_req2={a[0]}&VAL_NM_RQ={id}'

    try:
        response = urllib.request.urlopen(graf_data)
    except Exception as e:
        messagebox.showerror("Ошибка загрузки данных", str(e))
        return

    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    node_array = dom.getElementsByTagName("Record")
    x = []
    y = []

    for node in node_array:
        y.append(node.getAttribute('Date')[:5])
        for child in node.childNodes:
            if child.nodeName == 'Value':
                x.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
                break

    if len(x) > 100:
        x, y = x[::30], y[::30]
    elif len(x) > 50:
        x, y = x[::9], y[::9]
    elif len(x) > 10:
        x, y = x[::3], y[::3]

    plt.figure(figsize=(8, 5))
    plt.plot(y, x, marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Курс')
    plt.title(f'Динамика курса: {combo_gr.get()}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


window = Tk()
window.title("Валюты")
position = {"padx": 6, "pady": 6, "anchor": NW}
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")

combo = ttk.Combobox(tab1)
combo["values"] = names
combo.grid(column=0, row=0, padx=12, pady=12)

combo2 = ttk.Combobox(tab1)
combo2['values'] = names
combo2.grid(column=0, row=1, padx=12, pady=5)

txt = Entry(tab1)
txt.grid(column=2, row=0, padx=5, pady=12)

btn = Button(tab1, text="Конвертировать", command=calc)
btn.grid(column=4, row=0, padx=12, pady=12)

combo_gr = ttk.Combobox(tab2)
combo_gr['values'] = names
combo_gr.grid(column=0, row=1, padx=12, pady=12)

header = ttk.Label(tab2, text='Выберите все, чтобы построить график')
header.grid(column=1, row=0)

btn_gr = Button(tab2, text="Построить график", command=graph)
btn_gr.grid(column=3, row=3, padx=12, pady=12)

lang = StringVar()

a = ttk.Radiobutton(tab2, text='Неделя', value='0', command=period, variable=lang)
a.grid(column=0, row=2, padx=5)
b = ttk.Radiobutton(tab2, text='Месяц', value='1', command=period, variable=lang)
b.grid(column=1, row=2, padx=5)
c = ttk.Radiobutton(tab2, text='Квартал', value='2', command=period, variable=lang)
c.grid(column=2, row=2, padx=5)
d = ttk.Radiobutton(tab2, text='Год', value='3', command=period, variable=lang)
d.grid(column=3, row=2, padx=5)

combo_period = ttk.Combobox(tab2)
combo_period.grid(column=3, row=1, padx=12, pady=12)

tab_control.pack(expand=1, fill='both')
window.mainloop()
