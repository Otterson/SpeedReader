from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
import subprocess
import sys
import os 
import time
import pdftotext

#TK root setup
root = Tk()
root.geometry("1280x720")
root.title("Speed Reader")

#Word display variables
REFRESH_SPEED = 0.2
speed_string = StringVar()
WORD_SIZE = 20
font_size_string = StringVar()
word_font = tkFont.Font(size = WORD_SIZE)

#GUI setup
frame = Frame(root, width = 1280, height = 100)
frame.pack(side = TOP)

file_path = ""
file_entry = Entry(frame, width = 20)
file_entry.insert(0,'Filename')
file_entry.pack(padx = 5, pady = 5, side = LEFT)

filename_disp = StringVar()
filename_disp.set("")
filename_label = Label(frame, textvariable = filename_disp)

center_frame = Frame(root, width = 1280, height = 200)
center_frame.pack()

bottom_frame = Frame(root, width = 1280, height = 300)
bottom_frame.pack(side = BOTTOM)

#word label setup
word = StringVar()
word.set("TEST STRING")
word_label = Label(center_frame, textvariable = word, justify = CENTER, font = word_font)
word_label.pack(pady = 200)

def shrink_font():
    global WORD_SIZE
    WORD_SIZE-=2
    word_font.configure(size = WORD_SIZE)
    font_size_string.set(WORD_SIZE)
    root.update()

def grow_font():
    global WORD_SIZE
    WORD_SIZE+=2
    word_font.configure(size = WORD_SIZE)
    font_size_string.set(WORD_SIZE)
    root.update()

def slow_down():
    global REFRESH_SPEED
    REFRESH_SPEED+=0.05
    speed_string.set(REFRESH_SPEED)
    root.update()

def speed_up():
    global REFRESH_SPEED
    if REFRESH_SPEED >= 0.1:
        REFRESH_SPEED-=0.05
        speed_string.set(REFRESH_SPEED)
        root.update()

#main text read loop
def display_text(file_path):
    f = open(file_path, 'rb')
    file_split = file_path.split(".")
    file_type = file_split[len(file_split)-1]
    print(file_type)
    print("File opened")
    if file_type == "txt":
        for line in f:
            for string in line.split():
                word.set(string)
                word_label.configure(textvariable=word)
                root.update()
                if string[len(string)-1] == ".":
                    time.sleep(REFRESH_SPEED)
                time.sleep(REFRESH_SPEED)
    elif file_type == "pdf":
        pdf = pdftotext.PDF(f)
        for page in pdf:
            for string in page.split():
               # for string in line.split():
                word.set(string)
                word_label.configure(textvariable=word)
                root.update()
                if string[len(string)-1] == ".":
                    time.sleep(REFRESH_SPEED)
                time.sleep(REFRESH_SPEED)
       

    f.close()

#used when entering filename to search
def open_file():
    file_path = filedialog.askopenfilename(initialdir = "/home/Documents", title = "Select File", filetypes=(("all files", "*.*"),("txt files", "*.txt")))
    filename = ""
    file_split = file_path.split("/")
    filename_disp.set("Filename: " + file_split[len(file_split)-1])
    filename_label.configure(textvariable = filename_disp)
    display_text(file_path)

#used to open file dialog to search file manually
def search_file():
    if(file_entry.get() != "Filename"):
        if os.path.exists(file_entry.get()):
            filename_disp.set("Filename: " + file_entry.get())
            filename_label.configure(textvariable = filename_disp)
            file_path = file_entry.get()
        else:
            filename_disp.set("File not found")
            filename_label.configure(textvariable = filename_disp, fg = "red")
            print("No such file '{}'".format(file_entry.get()), file=sys.stderr)


#Buttons
search_button = Button(frame, text = "Search", command = search_file)
open_button = Button(frame, text = "Open", command = open_file)
search_button.pack(padx = 5, pady = 20, side = LEFT)
open_button.pack(padx = 5, pady = 20, side = LEFT)

#play_button = Button(bottom_frame, text = "Play", command = play_pause)
#reverse_button = Button(bottom_frame, text = "Rewind", command = rewind)


#font size info/control
shrink_button = Button(bottom_frame, text = "-", command = shrink_font)
shrink_button.pack(padx = 5, pady = 50, side = LEFT)

font_size_string.set(WORD_SIZE)
font_size_label = Label(bottom_frame, textvariable = font_size_string)
font_size_label.pack(padx = 5, pady = 20, side = LEFT)

grow_button = Button(bottom_frame, text = "+", command = grow_font)
grow_button.pack(padx = 5, pady = 20, side = LEFT)
filename_label.pack(padx = 5, pady = 20, side = LEFT)


#display speed info/control
increase_speed_button = Button(bottom_frame, text = "+", command = speed_up)
increase_speed_button.pack(padx = 5, pady = 20, side = RIGHT)

speed_string.set(REFRESH_SPEED)
speed_label = Label(bottom_frame, textvariable = speed_string)
speed_label.pack(padx = 5, pady = 20, side = RIGHT)

decrease_speed_button = Button(bottom_frame, text = "-", command = slow_down)
decrease_speed_button.pack(padx = 5, pady = 20, side = RIGHT)

root.mainloop() 





