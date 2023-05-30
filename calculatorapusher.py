#!/usr/bin/python3

import tkinter as tk
import re

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry ("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression =""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            "(":(0,2), ")":(0,3),
            7:(1,1), 8:(1,2), 9: (1,3),
            4:(2,1), 5:(2,2), 6: (2,3),
            1:(3,1), 2:(3,2), 3: (3,3),
            0:(4,2), '.':(4,1)
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

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=1, sticky=tk.NSEW)
      
    def calculs(self, calc):
        s = calc
        print("prou", s)
        while len(s) > 1:
            for i in range(len(s)):
                if ('/' in s or
                    '*' in s):
                    for i in range(len(s)):
                        if s[i] == '/':
                            s[i] = int(s[i-1]) / int(s[i+1])
                            s.pop(i-1)
                            s.pop(i)
                            break
                        elif s[i] == '*':
                            s[i] = int(s[i-1]) * int(s[i+1])
                            s.pop(i-1)
                            s.pop(i)
                            print(s)
                            break
                else:
                    for i in range(len(s)):
                        if s[i] == '-':
                            s[i] = int(s[i-1]) - int(s[i+1])
                            s.pop(i-1)
                            s.pop(i)
                            break
                        elif s[i] == '+':
                            s[i] = int(s[i-1]) + int(s[i+1])
                            s.pop(i-1)
                            s.pop(i)
                            print(s)
                            break
            self.total_expression = s[0]
            print (self.total_expression)
            self.current_expression = self.total_expression

            self.total_expression = ""
            self.update_label()
            return str(s[0])

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        self.s = re.findall('[+-/*//()]|\d+', self.total_expression)
        print ("S =>", self.s)
        self.subs = []
        if "(" in self.s:
            s = self.s
            for i in range(len(s)): 
                if s[i] == '(':
                    indexdebut = i+1
                if s[i] == ')':
                    indexfin = i
                    subs = s[indexdebut:indexfin] #envoyer en recursif
                    self.subs = subs
                    print(subs)
                    res = self.calculs(subs)
                    s[indexdebut - 1] = res
                    s[indexdebut:indexfin+1] = ""
                    print("RES =>", res, subs, s)
                    s = ("").join(s)
                    while re.findall('[+-/*//()]|\d+', s):
                        s = re.findall('[+-/*//()]|\d+', s)
                        s.pop()
                        s.pop(0)
                        res = self.calculs(s)
                        s[indexdebut - 1] = res
                        s[indexdebut:indexfin+1] = ""
                        # s = ("").join(s)
                    self.current_expression = res
                    self.update_label()

        else:
            s = self.s
            print("COUCOU", s)
            self.calculs(s)
        
        
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def update_label(self):
        self.label.config(text=self.current_expression)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()