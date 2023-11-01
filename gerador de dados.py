from tkinter import *
import tkinter as tk
from faker import Faker
import random
import os
from faker.providers.person import Provider as PersonProvider
from faker.providers.job import Provider as JobProvider
from faker.providers.address import Provider as AddressProvider
import csv
import subprocess
import importlib  

def select_language():
    global PersonProvider, JobProvider, AddressProvider

    language = input("Choose your data language (PT or EN): ")
    
    if language == "PT" or "pt":
        from faker.providers.person.pt_BR import Provider as PersonProvider
        from faker.providers.job.pt_BR import Provider as JobProvider
        from faker.providers.address.pt_BR import Provider as AddressProvider
    else:
        language == "EN" or "en"
        from faker.providers.person import Provider as PersonProvider
        from faker.providers.job import Provider as JobProvider
        from faker.providers.address import Provider as AddressProvider

    return language

language = select_language()

try:
    import faker
except ImportError:
    print("Installing the Faker library...")
    subprocess.run(["pip", "install", "Faker", "--user"])
try:
    from faker import Faker
except ImportError:
    print("Installing the Faker library...")
    subprocess.run(["pip", "install", "Faker", "--user"])

language = "EN"
text = {
    "EN": {
        "title": "Data Generator",
        "lines_label": "Number of lines:",
        "label": "Welcome",
        "path_label": "Destination path:",
        "generate_button": "Generate Data",
        "result_label": "",
        "language_button": "PT-BR",
    },
    "BR": {
        "title": "Gerador de Dados",
        "label": "Bem-Vindo",
        "lines_label": "Número de linhas:",
        "path_label": "Caminho de destino:",
        "generate_button": "Gerar Dados",
        "result_label": "",
        "language_button": "EN-US",
    },
}

fake = Faker()
Faker.seed(0)
fake.add_provider(PersonProvider)
fake.add_provider(JobProvider)
fake.add_provider(AddressProvider)

def toggle_language():
    global language
    if language == "EN":
        language = "BR"
    else:
        language = "EN"
    update_ui_texts()

def update_ui_texts():
    app.title(text[language]["title"])
    label.config(text=text[language]["label"])
    label_lines.config(text=text[language]["lines_label"])
    label_path.config(text=text[language]["path_label"])
    generate_button.config(text=text[language]["generate_button"])
    result_label.config(text=text[language]["result_label"])
    language_button.config(text=text[language]["language_button"])
    language_button.config(text=text[language]["language_button"])

def fake_name():
    name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{name} {last_name}"
    return full_name

def generate_data():
    qt_data = int(entry_lines.get())
    data = []

    for _ in range(qt_data):
        data.append({
            'Name': fake_name(),
            'Age': fake_age(),
            'Salary': fake_currency(),
            'Job': fake_job(),
            'Address': fake_address()
        })

    output_path = entry_path.get()
    csv_file = os.path.join(output_path, 'Dataset.csv')

    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['Name', 'Age', 'Salary', 'Job', 'Address']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    result_label.config(text=f'Data exported to {csv_file}')

def fake_age():
    return fake.random_int(min=18, max=68)

def fake_currency():
    amount = round(random.uniform(1, 1000), 2)
    return f"{amount}"

def fake_job():
    return fake.job()

def fake_address():
    return fake.street_address()

def reset_app():
    entry_lines.delete(0, END)
    entry_path.delete(0, END)
    result_label.config(text="")

app = Tk()
app.title(text[language]["title"])
app.geometry('600x300')

app.configure(bg='lightblue')

label = tk.Label(app, text=text[language]["label"], bg='lightblue', font=("Helvetica", 20), fg='red')
label.pack()

label_lines = Label(app, text=text[language]["lines_label"], bg='lightblue')
label_lines.place(x=150, y=60)

entry_lines = Entry(app)
entry_lines.place(x=260, y=60)

label_path = Label(app, text=text[language]["path_label"], bg='lightblue')
label_path.place(x=150, y=100)

entry_path = Entry(app)
entry_path.place(x=260, y=100)

generate_button = Button(app, text=text[language]["generate_button"], command=generate_data, bg='green', fg='black')
generate_button.place(x=240, y=160)

result_label = Label(app, text=text[language]["result_label"], bg='lightblue')
result_label.place(x=120, y=130)

language_button = Button(app, text=text[language]["language_button"], command=toggle_language, bg='lightcoral', fg='black')
language_button.place(x=260, y=200)

reset_button = Button(app, text="Reset", command=reset_app, bg='red', fg='white')
reset_button.place(x=260, y=240)

app.mainloop()