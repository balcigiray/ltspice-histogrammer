# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 2022

@author: giraybalci
"""

import data_processor as engine
import tkinter as tk
# import PyPDF2
# from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
# import os



#start of GUI
root = tk.Tk()
root.title("LTspice Histogrammer")

tk.Frame(root)

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=4)


#logo image placeholder


font_name = "Arial"

instructions = tk.Label(root, text="Select the .log file", font=font_name)
instructions.grid(columnspan=3, column=0, row=1)


def open_file():
    browse_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', title="Chose a file", filetype=[("Log file", "*.log")])
    if file:
        print("file is succesfully loaded")
        engine.__importFile()
        message = tk.Label(root, text="Succesfully analyzed. Check img/ folder", font=font_name, fg="green" )
        message.grid(columnspan=3, column=0, row=4)          

    browse_text.set("browse")


#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font=font_name, bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=1, row=2)

canvas = tk.Canvas(root, width=600, height=50)
canvas.grid(columnspan=3)


#End of GUI
root.mainloop()
