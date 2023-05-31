import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta

mydb = mysql.connector.connect(
    host="h23.seohost.pl",
    user="srv38973_projekt_python",
    password="projekt_python",
    database="srv38973_projekt_python"
)

mycursor = mydb.cursor()


class MenuItem:
    def __init__(self, name, calories, protein, carbs, fat):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

    def __str__(self):
        return f"{self.name} - {self.calories}kcal, {self.protein}g, {self.carbs}g, {self.fat}g"

max_calories = 0
max_protein = 0
max_fat = 0
max_carbs = 0

def add_button_clicked():
    def add_item():
        def askWeight(): 
            def grams_submitted():
                weight = float(entry.get()) / 100
                name = item.split(" - ")[0]
                kcal = float(item.split(" - ")[1].split("kcal")[0])
                carb = float(item.split(" - ")[1].split("kcal, ")[1].split("g, ")[0])
                fat = float(item.split(" - ")[1].split("kcal, ")[1].split("g, ")[1])
                prot = float(item.split(" - ")[1].split("kcal, ")[1].split("g, ")[2].split("g")[0])
                print(name)
                print(kcal)
                print(prot)
                print(carb)
                print(fat)
                tempitem = MenuItem(name, kcal * weight, prot * weight, carb * weight, fat * weight)
                main_listbox.insert(tk.END, tempitem)
                update_totals()
                add_window.destroy()
                askweight_window.destroy()
            askweight_window = tk.Tk()
            askweight_window.title("Grams Input")

            label = tk.Label(askweight_window, text="Enter grams:")
            label.pack()

            entry = tk.Entry(askweight_window)
            entry.pack()

            submit_button = tk.Button(askweight_window, text="Submit", command=grams_submitted)
            submit_button.pack()
        selected_index = listbox.curselection()
        if selected_index:
            item = listbox.get(selected_index)
            askWeight()

    def filter_items(event=None):
        search_term = search_entry.get().lower()
        listbox.delete(0, tk.END)
        for item in item_list:
            if search_term in item.name.lower():
                listbox.insert(tk.END, str(item))

    add_window = tk.Toplevel(root)
    add_window.geometry("400x350")
    item_list = []

    mycursor.execute("SELECT * FROM main")
    myresult = mycursor.fetchall()
    for x in myresult:
        item_list.append(MenuItem(x[1], int(x[3]), int(x[2]), int(x[4]), int(x[5])))

    search_label = tk.Label(add_window, text="Search:")
    search_label.pack(side=tk.TOP, padx=5, pady=5)

    search_entry = tk.Entry(add_window)
    search_entry.pack(side=tk.TOP, padx=5)
    search_entry.bind('<KeyRelease>', filter_items)

    listbox = tk.Listbox(add_window)
    
    for item in item_list:
        listbox.insert(tk.END, str(item))
    listbox.pack(side=tk.TOP, fill=tk.BOTH)
    search_label = tk.Label(add_window, text="We have " + str(len(item_list)) + " products in database")
    search_label.pack(side=tk.TOP, padx=5, pady=5)
    add_button = tk.Button(add_window, text="Add to Day", command=add_item)
    add_button.pack(side=tk.BOTTOM, padx=5, pady=5)


def remove_button_clicked():
    selected_index = main_listbox.curselection()
    if selected_index:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this item?")
        if confirmation:
            main_listbox.delete(selected_index)
            update_totals()


def clear_button_clicked():
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to clear the list?")
    if confirmation:
        main_listbox.delete(0, tk.END)
        update_totals()

class macroSet:
    def __init__(self, calories, fat, protein, carbs) -> None:
        self.calories = calories
        self.fat = fat
        self.protein = protein
        self.carbs = carbs

ms = []

def open_set_macro_window():
    def save_macro():
        gender = gender_entry.get()
        weight = float(weight_entry.get())
        age = int(age_entry.get())
        growth = float(growth_entry.get())

        if gender.lower() == "male":
            max_calories = round((10 * weight) + (6.25 * growth) - (5 * age) + 5)
        elif gender.lower() == "female":
            max_calories = round((10 * weight) + (6.25 * growth) - (5 * age) - 161)

        max_protein = round(weight * 1.5)
        max_fat = round(max_calories * (25 / 100) * 0.1)
        max_carbs = round((max_calories - max_fat * 9 - max_protein * 4)/4)
        
        ms.append(macroSet(max_calories, max_fat, max_protein, max_carbs))

        calorie_text.config(text=f"0/{max_calories}kcal")
        protein_label.config(text=f"0/{max_protein}g protein")
        carb_label.config(text=f"0/{max_carbs}g carbs")
        fat_label.config(text=f"0/{max_fat}g fat")
        add_button.config(state=tk.NORMAL)
        remove_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)
        load_button.config(state=tk.DISABLED)
        save_button.config(state=tk.NORMAL)
        nextDay_button.config(state=tk.DISABLED)
        prevDay_button.config(state=tk.DISABLED)
        set_macro_button.config(state=tk.DISABLED)
        set_macro_window.destroy()

    def sprawdzBmi():
        def calculate_bmi():
            weight = float(weight_entry.get())
            height = float(height_entry.get()) / 100  # Convert height from cm to meters
            bmi = weight / (height ** 2)
            
            # Determine the weight status based on BMI
            if bmi < 18.5:
                weight_status = "underweight"
            elif 18.5 <= bmi < 25:
                weight_status = "normal weight"
            elif 25 <= bmi < 30:
                weight_status = "overweight"
            else:
                weight_status = "obese"
            
            message = f"Your BMI is {bmi:.2f}.\nYou are {weight_status}."
            messagebox.showinfo("BMI Calculation", message)
            window.destroy()

        # Create the Tkinter window
        window = tk.Tk()
        window.title("BMI Calculator")

        # Gender selection
        gender_label = tk.Label(window, text="Gender:")
        gender_label.pack()
        gender_var = tk.StringVar()
        gender_radio_male = tk.Radiobutton(window, text="Male", variable=gender_var, value="Male")
        gender_radio_male.pack()
        gender_radio_female = tk.Radiobutton(window, text="Female", variable=gender_var, value="Female")
        gender_radio_female.pack()

        # Height entry
        height_label = tk.Label(window, text="Height (cm):")
        height_label.pack()
        height_entry = tk.Entry(window)
        height_entry.pack()

        # Weight entry
        weight_label = tk.Label(window, text="Weight (kg):")
        weight_label.pack()
        weight_entry = tk.Entry(window)
        weight_entry.pack()

        # Submit button
        submit_button = tk.Button(window, text="Submit", command=calculate_bmi)
        submit_button.pack()


    def setCustom():
        def submit_custom_macro():
            ms.append(macroSet(float(kcal_entry.get()), float(fat_entry.get()), float(protein_entry.get()), float(carbs_entry.get())))

            calorie_text.config(text=f"0/{float(kcal_entry.get())}kcal")
            protein_label.config(text=f"0/{float(protein_entry.get())}g protein")
            carb_label.config(text=f"0/{float(carbs_entry.get())}g carbs")
            fat_label.config(text=f"0/{float(fat_entry.get())}g fat")
            add_button.config(state=tk.NORMAL)
            remove_button.config(state=tk.NORMAL)
            clear_button.config(state=tk.NORMAL)
            load_button.config(state=tk.DISABLED)
            save_button.config(state=tk.NORMAL)
            nextDay_button.config(state=tk.DISABLED)
            prevDay_button.config(state=tk.DISABLED)
            set_macro_button.config(state=tk.DISABLED)
            update_totals()
            set_macro_window.destroy()
            custom_macro_window.destroy()
        custom_macro_window = tk.Tk()
        custom_macro_window.title("Custom macro")

        # Kcal input
        kcal_label = tk.Label(custom_macro_window, text="Kcal:")
        kcal_label.pack()
        kcal_entry = tk.Entry(custom_macro_window)
        kcal_entry.pack()

        # Protein input
        protein_label = tk.Label(custom_macro_window, text="Protein:")
        protein_label.pack()
        protein_entry = tk.Entry(custom_macro_window)
        protein_entry.pack()

        # Carbs input
        carbs_label = tk.Label(custom_macro_window, text="Carbs:")
        carbs_label.pack()
        carbs_entry = tk.Entry(custom_macro_window)
        carbs_entry.pack()

        # Fat input
        fat_label = tk.Label(custom_macro_window, text="Fat:")
        fat_label.pack()
        fat_entry = tk.Entry(custom_macro_window)
        fat_entry.pack()

        # Submit button
        submit_button = tk.Button(custom_macro_window, text="Submit", command=submit_custom_macro)
        submit_button.pack()

    set_macro_window = tk.Toplevel(root)
    set_macro_window.title("Set Macro")
    set_macro_window.geometry("300x300")

    save_button = tk.Button(set_macro_window, text="Calculate BMI", command=sprawdzBmi)
    save_button.pack()

    gender_label = tk.Label(set_macro_window, text="Gender:")
    gender_label.pack()

    gender_options = ["Male", "Female"]
    gender_entry = ttk.Combobox(set_macro_window, values=gender_options)
    gender_entry.pack()

    weight_label = tk.Label(set_macro_window, text="Weight:")
    weight_label.pack()

    weight_entry = tk.Entry(set_macro_window)
    weight_entry.pack()

    age_label = tk.Label(set_macro_window, text="Age:")
    age_label.pack()

    age_entry = tk.Entry(set_macro_window)
    age_entry.pack()

    growth_label = tk.Label(set_macro_window, text="Growth:")
    growth_label.pack()

    growth_entry = tk.Entry(set_macro_window)
    growth_entry.pack()

    bottom_buttons = tk.Frame(set_macro_window)
    bottom_buttons.pack(side=tk.LEFT, expand=True, fill=tk.X)

    save_macro_button = tk.Button(bottom_buttons, text="Save", command=save_macro)
    save_macro_button.pack()

    set_macro_button = tk.Button(bottom_buttons, text="Set custom", command=setCustom)
    set_macro_button.pack()


def update_totals():
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    save_button.config(state=tk.NORMAL)
    for index in range(main_listbox.size()):
        item = main_listbox.get(index).split(" - ")[1]
        total_calories += float(item.split("kcal")[0])
        total_protein += float(item.split(", ")[1].split("g")[0])
        total_carbs += float(item.split(", ")[2].split("g")[0])
        total_fat += float(item.split(", ")[3].split("g")[0])

    calorie_text.config(text=f"{total_calories}/{ms[0].calories}kcal")
    calorie_progress['maximum'] = ms[0].calories
    calorie_progress['value'] = total_calories
    protein_label.config(text=f"{total_protein}/{ms[0].protein}g protein")
    protein_progress['maximum'] = ms[0].protein
    protein_progress['value'] = total_protein
    carb_label.config(text=f"{total_carbs}/{ms[0].carbs}g carbs")
    carb_progress['maximum'] = ms[0].carbs
    carb_progress['value'] = total_carbs
    fat_label.config(text=f"{total_fat}/{ms[0].fat}g fat")
    fat_progress['maximum'] = ms[0].fat
    fat_progress['value'] = total_fat

def load_from_file():
    filename = currentSave["text"] + ".txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
        index = 0
        while index < len(lines):
            line = lines[index]
            if line.startswith("Product:"):
                product = line.split("Product: ")[1].strip()
                main_listbox.insert(tk.END, product)
            elif line.startswith("Calories:"):
                calories = int(line.split("Calories: ")[1])
            elif line.startswith("Fat:"):
                fat = int(line.split("Fat: ")[1])
            elif line.startswith("Protein:"):
                protein = int(line.split("Protein: ")[1])
            elif line.startswith("Carbs:"):
                carbs = int(line.split("Carbs: ")[1])
            index += 1
        ms.append(macroSet(calories, fat, protein, carbs))
        update_totals()
    add_button.config(state=tk.NORMAL)
    remove_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.NORMAL)
    set_macro_button.config(state=tk.DISABLED)
    save_button.config(state=tk.NORMAL)
    load_button.config(state=tk.DISABLED)
    nextDay_button.config(state=tk.DISABLED)
    prevDay_button.config(state=tk.DISABLED)

def save_to_file():
    filename = currentSave["text"] + ".txt"
    with open(filename, 'w') as file:
        # Save added products
        for index in range(main_listbox.size()):
            product = main_listbox.get(index)
            file.write(f"Product: {product}\n")
        
        # Save macros
        if ms:
            macros = ms[0]
            file.write(f"Calories: {macros.calories}\n")
            file.write(f"Protein: {macros.protein}\n")
            file.write(f"Carbs: {macros.carbs}\n")
            file.write(f"Fat: {macros.fat}\n")
    
    print("Data saved to file.")

def changeDayNext():
    date_string = currentSave["text"]
    date = datetime.strptime(date_string, '%d-%m-%Y')
    next_day = date + timedelta(days=1)
    next_day_string = next_day.strftime('%d-%m-%Y')
    currentSave["text"] = next_day_string

def changeDayPrev():
    date_string = currentSave["text"]
    date = datetime.strptime(date_string, '%d-%m-%Y')
    next_day = date + timedelta(days=-1)
    next_day_string = next_day.strftime('%d-%m-%Y')
    currentSave["text"] = next_day_string

# Create main window
root = tk.Tk()
root.title("FitU")
root.geometry("520x450")

buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.TOP)

add_button = tk.Button(buttons_frame, text="Add", command=add_button_clicked, state=tk.DISABLED)
add_button.pack(side=tk.LEFT)

# Remove button
remove_button = tk.Button(buttons_frame, text="Remove", command=remove_button_clicked, state=tk.DISABLED)
remove_button.pack(side=tk.LEFT)

# Clear button
clear_button = tk.Button(buttons_frame, text="Clear", command=clear_button_clicked, state=tk.DISABLED)
clear_button.pack(side=tk.LEFT)

# Set Macro button
set_macro_button = tk.Button(buttons_frame, text="Set Macro", command=open_set_macro_window)
set_macro_button.pack(side=tk.LEFT)


save_frame = tk.Frame(root)
save_frame.pack(side=tk.TOP)

prevDay_button = tk.Button(save_frame, text="<-", command=changeDayPrev)
prevDay_button.pack(side=tk.LEFT)

setDay = datetime.now().strftime('%d-%m-%Y')
currentSave = tk.Label(save_frame, text=setDay)
currentSave.pack(side=tk.LEFT)

nextDay_button = tk.Button(save_frame, text="->", command=changeDayNext)
nextDay_button.pack(side=tk.LEFT)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.TOP)

save_button = tk.Button(bottom_frame, text="Save", command=save_to_file, state=tk.DISABLED)
save_button.pack(side=tk.LEFT)

load_button = tk.Button(bottom_frame, text="Load", command=load_from_file)
load_button.pack(side=tk.LEFT)

# Main listbox
main_listbox = tk.Listbox(root)
main_listbox.pack(side=tk.TOP, fill=tk.BOTH)

# Scrollable list
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

main_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=main_listbox.yview)

# Total calorie text
calorie_text = tk.Label(root, text="0/0kcal")
calorie_text.pack(side=tk.TOP)

calorie_progress = ttk.Progressbar(root, orient="horizontal", length=200)
calorie_progress.pack()

# Macro nutrient texts
macro_text = tk.Frame(root)
macro_text.pack(side=tk.TOP)

protein_label = tk.Label(macro_text, text="0/0g protein")
protein_label.pack(side=tk.LEFT)

carb_label = tk.Label(macro_text, text="0/0g carbs")
carb_label.pack(side=tk.LEFT)

fat_label = tk.Label(macro_text, text="0/0g fat")
fat_label.pack(side=tk.LEFT)

macro_progress = tk.Frame(root)
macro_progress.pack(side=tk.LEFT, expand=True, fill=tk.X)

protein_progress = ttk.Progressbar(macro_progress, orient="horizontal", length=100)
protein_progress.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

carb_progress = ttk.Progressbar(macro_progress, orient="horizontal", length=100)
carb_progress.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

fat_progress = ttk.Progressbar(macro_progress, orient="horizontal", length=100)
fat_progress.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)



root.mainloop()
