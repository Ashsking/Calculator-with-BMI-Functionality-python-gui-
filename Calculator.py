"""
Learned and Accomplished:

Throughout this project, I gained a deeper understanding of building graphical user interfaces (GUIs) using the Tkinter library in Python.
This project involved creating a feature-rich calculator with standard arithmetic operations, a history log, and an additional BMI calculator with personalized messages. 
I focused on enhancing the user experience by incorporating keyboard bindings, error handling, and a visually appealing layout.
The significant learning aspect was the integration of multiple Tkinter windows, where the BMI calculator is invoked as a separate window with entry validations and result display. 
I also expanded my knowledge of event handling, widget styling, and layout management within Tkinter. Additionally, the implementation of personalized messages based on BMI values added a creative touch to the project.
I would like to express my gratitude to Daniel Showalter and Shravan Akula for providing this opportunity. 
Their guidance and support were invaluable in navigating the complexities of GUI development and expanding my skills in Python programming. 
This project has equipped me with practical insights into creating interactive applications, and I look forward to applying these skills in future endeavors.

# -- Modifications and Explanations --

# I added a neutral color scheme to improve the calculator's aesthetics.
# Changed the BMI calculator entry validation to ensure names contain only alphabetic characters.
# Enhanced the calculator's functionality with keyboard bindings for both digits and operators.
# Implemented personalized BMI messages for a more engaging user experience.
# Improved code readability with informative comments and consistent coding style.
"""

import tkinter as tk
from tkinter import Menu, Label, Button, StringVar, Entry, Frame, N, W, Toplevel, Listbox, Scrollbar, messagebox

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"
SILVER_GRAY = "#C0C0C0"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("196x255")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Create a menu bar
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        # Create a "Calculator" menu
        calculator_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="≡", menu=calculator_menu)  # Use the ≡ symbol as the menu label

        calculator_menu.add_command(label="BMI Calculator", command=self.show_bmi_calculator) 
        calculator_menu.add_command(label="History", command=self.show_history)
        calculator_menu.add_separator()
        calculator_menu.add_command(label="Exit", command=self.window.destroy)

        # Calculator widgets and variables
        self.total_expression = ""
        self.current_expression = ""
        self.history = []  # List to store the history of calculations
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

        # Initialize the selected calculator
        self.current_calculator = None

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        

    def create_display_labels(self):
        total_label = Label(self.display_frame, text=self.total_expression, anchor="e", bg="lightgray",
                            fg="black", padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = Label(self.display_frame, text=self.current_expression, anchor="e", bg="lightgray",
                      fg="black", padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = Frame(self.window, bg="lightgray")
        frame.grid(row=1, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = Button(self.buttons_frame, text=str(digit), bg="white", fg="black",
                             font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=N + W + "E" + "S")

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg="black",
                             font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=N + W + "E" + "S")
            i += 1
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg="black",
                        font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=N + W + "E" + "S")

    def square(self):
        try:
            result = eval(f"{self.current_expression}**2")
            # Format the result to display decimals only if needed
            self.current_expression = f"{result:.3f}" if result % 1 != 0 else f"{int(result)}"
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()


    def create_square_button(self):
        button = Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg="black",
                        font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=N + W + "E" + "S")

    def sqrt(self):
        try:
            result = eval(f"{self.current_expression}**0.5")
            # Format the result to display decimals only if needed
            self.current_expression = f"{result:.3f}" if result % 1 != 0 else f"{int(result)}"
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_sqrt_button(self):
        button = Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg="black",
                        font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=N + W + "E" + "S")

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            result = str(eval(self.total_expression))
            self.current_expression = result
            self.history.append(f"{self.total_expression} = {result}")
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg="black",
                        font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=N + W + "E" + "S")

    def create_buttons_frame(self):
        frame = Frame(self.window)
        frame.grid(row=2, column=0, sticky="nsew")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()

    def show_history(self):
        history_window = Toplevel(self.window)
        history_window.title("History")
        history_window.geometry("300x400")

        history_listbox = Listbox(history_window, font=DEFAULT_FONT_STYLE)
        history_listbox.pack(fill="both", expand=True)

        scrollbar = Scrollbar(history_window, orient="vertical")
        scrollbar.config(command=history_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        for item in self.history:
            history_listbox.insert("end", item)

    def show_bmi_calculator(self):
        if self.current_calculator:
            self.current_calculator.destroy()

        # Create an instance of BMICalculator
        self.current_calculator = BMICalculator(self.window,self)

class BMICalculator:
    def __init__(self, main_window, calculator_instance):
        self.main_window = main_window
        self.calculator_instance = calculator_instance
        self.main_window.withdraw()

        self.bmi_window = Toplevel(main_window)
        self.bmi_window.geometry("350x360")
        
        self.bmi_window.title("BMI Calculator")
        self.bmi_window.protocol("WM_DELETE_WINDOW", self.on_close_bmi)

        # Apply a neutral color scheme
        self.bmi_window.configure(bg="lightgray")
        self.name_var = StringVar()
        self.height_var = StringVar()
        self.weight_var = StringVar()

        
        self.create_entry_with_border("HEIGHT (cm):", self.height_var, row=1)
        self.create_entry_with_border("WEIGHT (kg):", self.weight_var, row=3)
        self.create_entry_with_border("NAME:", self.name_var, row=5)

        # Button with silver border
        self.create_button_with_border("Calculate BMI", self.find_bmi, row=7)
        self.create_button_with_border("Return to Calculator", self.return_to_calculator, row=9)

    def create_entry_with_border(self, label_text, text_variable, row):
        label = Label(self.bmi_window, text=label_text, font=("Arial", 20, "bold"), bg="lightgray", fg="black")
        label.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)

        entry = Entry(self.bmi_window, bg="white", textvariable=text_variable, font=("Arial", 20, "bold"), fg="black", bd=3, relief=tk.SOLID)
        entry.grid(row=row + 1, column=0, ipadx=40, padx=10, pady=5, sticky=tk.N + tk.W + tk.E + tk.S)

    def create_button_with_border(self, text, command, row):
        button = Button(self.bmi_window, text=text, font=("Arial", 20, "bold"), bg=SILVER_GRAY, fg="black", command=command, bd=3, relief=tk.SOLID)
        button.grid(row=row, column=0, pady=5)
    def validate_name(self):
        name = self.name_var.get()
        return name.isalpha()
    
    def find_bmi(self):
        if not self.validate_name():
            messagebox.showerror("Invalid Input", "Name should contain only alphabetic characters.")
            return

        name = self.name_var.get()
        height = self.height_var.get()
        weight = self.weight_var.get()

        if name and height and weight:
            height = float(height) / 100.0
            bmi = round(float(weight) / height ** 2, 2)
            result = f"{name} , your BMI: {bmi}"
            self.calculator_instance.history.append(result)  # Add the BMI result to the history
            self.show_bmi_result(result)
        else:
            # Handle invalid input (height or weight not provided)
            pass

    def show_bmi_result(self, result):
        result_window = Toplevel(self.bmi_window)
        result_window.title("BMI Result")
        result_window.geometry("600x150")

        # Apply a neutral color scheme
        result_window.configure(bg="lightgray")

        bmi_label = Label(result_window, text=result, font=("Arial", 20, "bold"), bg="lightgray", fg="black")
        bmi_label.pack()

        # Add a personalized message based on the BMI value
        bmi_value = float(result.split(":")[1].strip())
        message = self.get_personalized_message(bmi_value)

        message_label = Label(result_window, text=message, font=("Arial", 14), bg="lightgray", fg="black")
        message_label.pack()

    def get_personalized_message(self, bmi_value):
      message_font = ("Times New Roman", 14, "bold")
      if 18.5 <= bmi_value < 25:
        message = "Great news! Your BMI is in the sweet spot – like hitting the jackpot! 🎉\n"
        message += "Here are some tips to keep riding the wave:\n"
        message += "• Mix it up with a rainbow of foods – fruits, veggies, and whole grains are your BFFs.\n"
        message += "• Keep the vibe going with lean proteins and healthy fats – they’re the real MVPs.\n"
        message += "• Stay groovy with activities you love – dancing, walking, or maybe some funky yoga!"
        return message
      elif 25 <= bmi_value < 30:
        message = "Guess what? Your BMI is throwing a party – just a little extra celebration! 🎈\n"
        message += "Here's your backstage pass to shine in the spotlight:\n"
        message += "• Dazzle with nutrient-packed foods – colorful veggies and tasty proteins.\n"
        message += "• Turn up the energy with activities you enjoy – it's all about the good vibes.\n"
        message += "• Need an encore? A chat with a nutritionist is like getting VIP access!"
        return message
      elif bmi_value >= 30:
        message = "Hold up! Your BMI is saying 'hello, abundance' – no biggie, you’re a star! ✨\n"
        message += "Embrace your abundance with style:\n"
        message += "• Feast on a variety of tasty foods – fruits, veggies, and whole grains steal the show.\n"
        message += "• Dance through the menu, keeping lean proteins in the limelight – sayonara, less cool stuff.\n"
        message += "• Manage portions like a pro – it's your own abundance party, after all!"
        return message
        
    def return_to_calculator(self):
        self.main_window.deiconify()
        self.bmi_window.destroy()

    def on_close_bmi(self):
        self.main_window.withdraw()
 
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
