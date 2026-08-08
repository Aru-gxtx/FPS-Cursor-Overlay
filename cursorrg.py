from tkinter import *
from PIL import Image, ImageTk
from pynput import mouse
import os
import random
import sys


EXE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
DATA_DIR = EXE_DIR

root = Tk()

with open(os.path.join(DATA_DIR, "save.txt"), "r", encoding="utf-8") as f:
    image_path = f.read().strip()
if image_path and not os.path.isabs(image_path):
    image_path = os.path.join(DATA_DIR, image_path)
image = Image.open(image_path)
w, h = image.size
resized_image = image.resize((w, h))

img = ImageTk.PhotoImage(resized_image)

canvas = Canvas(root, bg="#17166A", highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)
item = canvas.create_image(root.winfo_screenwidth() * .5, root.winfo_screenheight() * .5, image=img, anchor=CENTER)

root.config(bg="#17166A")

root.attributes("-transparentcolor", "#17166A")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

held = False
rimg = None

def tick():
    global img, rimg
    if held:
        rexpand = random.randint(8, 16)
        recoil = image.resize((w + rexpand, h + rexpand))
        rimg = ImageTk.PhotoImage(recoil)
        canvas.itemconfig(item, image=rimg)
    else:
        canvas.itemconfig(item, image=img)
    rtick = random.randint(8, 20)
    root.after(rtick, tick)

def on_click(x, y, button, pressed):
    global held
    if button == mouse.Button.left:
        held = pressed

def reset_image():
    global img
    img = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(item, image=img)

b1listener = mouse.Listener(on_click=on_click)
b1listener.start()
tick()

root.mainloop()