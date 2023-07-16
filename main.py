from tkinter import *
import random
import pandas
import time

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
random_row = {}

# ------------------------- Data ----------------------------#
try:

    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:   # read from a fresh csv file
    original_data = pandas.read_csv("./data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")
# print(data_dict[0]["French"])
# print(random.choice(data_dict)["French"])
# ------------------------- Functions ----------------------------#


def new_word():
    global random_row, flip_timer
    window.after_cancel(flip_timer)
    random_row = random.choice(data_dict)
    foreign_key = [key for key in random_row.keys()][0]
    foreign_word = random_row[foreign_key]
    canvas.itemconfig(canvas_image, image=image_front)
    canvas.itemconfig(canvas_word, text=foreign_word, fill="black")
    canvas.itemconfig(canvas_key, text=foreign_key, fill="black")
    flip_timer = window.after(3000, func=new_word)


def turn_card():
    global random_row
    english_key = [key for key in random_row.keys()][1]
    english_word = random_row[english_key]
    canvas.itemconfig(canvas_image, image=image_back)
    canvas.itemconfig(canvas_key, text=english_key, fill="white")
    canvas.itemconfig(canvas_word, text=english_word, fill="white")


def know_word():
    data_dict.remove(random_row)
    words_to_learn_dict = pandas.DataFrame(data_dict)
    print(len(data_dict))
    words_to_learn_dict.to_csv("./data/words_to_learn.csv", index=False)
    new_word()
# ------------------------- GUI ----------------------------#


window = Tk()
window.title("Language Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=new_word)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
image_front = PhotoImage(file="images/card_front.png")
image_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=image_front)
canvas.grid(row=0, column=0, columnspan=2)

# --------------------
canvas_key = canvas.create_text(400, 150, text="Language", font=FONT_LANGUAGE)
canvas_word = canvas.create_text(400, 263, text="Word", font=FONT_WORD)
# --------------------

image_no = PhotoImage(file="./images/wrong.png")
button_no = Button(image=image_no, highlightthickness=0, command=turn_card)
button_no.grid(row=1, column=0)

image_yes = PhotoImage(file="./images/right.png")
button_yes = Button(image=image_yes, highlightthickness=0, command=know_word)
button_yes.grid(row=1, column=1)


new_word()



window.mainloop()
