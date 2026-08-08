from tkinter import *
from PIL import Image, ImageTk
import os
from tktooltip import ToolTip
import subprocess
import random
import sys

root = Tk()
root.title("Select and Run a cursor:")

EXE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
if getattr(sys, "frozen", False):
    BUILD_DIR = os.path.join(EXE_DIR, "build")
    DATA_DIR = BUILD_DIR if os.path.exists(os.path.join(BUILD_DIR, "save.txt")) else EXE_DIR
else:
    DATA_DIR = EXE_DIR
CURSOR_DIR = os.path.join(DATA_DIR, "icons", "cursors")
OVERLAY_EXE = os.path.join(DATA_DIR, "cursorrg.exe") if getattr(sys, "frozen", False) else None

def cursor_image(color, size=(50, 50)):
    image = Image.new("RGB", size)
    return ImageTk.PhotoImage(image)

def cursor_image_path(path):
    image = Image.open(path)
    return ImageTk.PhotoImage(image)

images = []
labels = []
current_files = set()
selected_frame = None
selected_path = None
run_proc = None


def stop_run_process():
    global run_proc
    proc = run_proc
    run_proc = None
    if proc is None or proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                check=False,
                capture_output=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            proc.terminate()
            try:
                proc.wait(timeout=1)
            except Exception:
                proc.kill()
    except Exception:
        try:
            proc.terminate()
        except Exception:
            pass

def select_frame(f, path=None):
    global selected_frame, selected_path
    try:
        if selected_frame is not None and selected_frame is not f:
            # restore visual state for previously selected frame
            selected_frame.config(borderwidth=2, relief=RAISED, highlightthickness=0)
    except Exception:
        pass
    try:
        # make selection visually obvious: use both relief and highlight
        f.config(borderwidth=4, relief=SUNKEN, highlightthickness=0, highlightbackground="black")
        # store selected path for other parts of the program
        selected_path = path
        # persist selection to a small file
        if path is not None:
            with open(os.path.join(DATA_DIR, "save.txt"), "w", encoding="utf-8") as fh:
                fh.write(path)
    except Exception:
        pass
    selected_frame = f

def load_images():
    global images, labels, current_files
    # remove old widgets
    for lbl in labels:
        try:
            lbl.destroy()
        except Exception:
            pass
    images = []
    labels = []

    try:
        files = sorted(os.listdir(CURSOR_DIR))
    except Exception:
        files = []

    current_files = set(files)

    for idx, filename in enumerate(files):
        path = os.path.join(CURSOR_DIR, filename)
        try:
            img = cursor_image_path(path)
        except Exception:
            continue
        images.append(img)

        # create a fixed-size frame and prevent it shrinking to child
        frame_w = 60
        frame_h = 60
        frame = Frame(root, relief=RAISED, borderwidth=2, width=frame_w, height=frame_h, highlightthickness=0)
        frame.grid(row=0, column=idx, padx=10, pady=10)
        frame.grid_propagate(False)

        # put the label inside the frame and center it
        lbl = Label(frame, image=img, bg=root.cget("bg"))
        lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        # bind hover and click to the frame so the whole box responds
        frame.bind("<Enter>", lambda e, f=frame, l=lbl: (f.config(bg="lightblue"), l.config(bg="lightblue")))
        frame.bind("<Leave>", lambda e, f=frame, l=lbl: (f.config(bg=root.cget("bg")), l.config(bg=root.cget("bg"))))
        frame.bind("<Button-1>", lambda e, f=frame, p=path: (select_frame(f, p)))
        # also bind label so hovering the image triggers the same
        lbl.bind("<Enter>", lambda e, f=frame, l=lbl: (f.config(bg="lightblue"), l.config(bg="lightblue")))
        lbl.bind("<Leave>", lambda e, f=frame, l=lbl: (f.config(bg=root.cget("bg")), l.config(bg=root.cget("bg"))))
        lbl.bind("<Button-1>", lambda e, f=frame, p=path: (select_frame(f, p)))
        labels.append(lbl)
    # reposition the add button/label if it already exists (use add_frame)
    if 'add_frame' in globals():
        try:
            add_frame.grid_configure(row=0, column=len(images), padx=10, pady=10)
        except Exception:
            add_frame.grid(row=0, column=len(images), padx=10, pady=10)

def poll_changes():
    try:
        files = set(os.listdir(CURSOR_DIR))
    except Exception:
        files = set()
    if files != current_files:
        load_images()
    root.after(1000, poll_changes)

# initial load and start polling
load_images()
root.after(1000, poll_changes)

# add icon inside a fixed-size frame so it behaves like the other items
add_frame = Frame(root, width=60, height=60, relief=RAISED, borderwidth=2, bg=root.cget("bg"), highlightthickness=0)
add_frame.grid_propagate(False)
add_frame.grid(row=0, column=len(images), padx=10, pady=10)

def start_run_process():
    global run_proc
    try:
        if OVERLAY_EXE and os.path.exists(OVERLAY_EXE):
            run_proc = subprocess.Popen([OVERLAY_EXE])
        else:
            run_proc = subprocess.Popen([sys.executable, os.path.join(EXE_DIR, "cursorrg.py")])
    except Exception:
        run_proc = None

def _wait_and_restart(old_proc):
    # poll until old_proc has exited, then start a new one
    if old_proc.poll() is None:
        root.after(100, lambda: _wait_and_restart(old_proc))
    else:
        start_run_process()
        run_btn.config(state=NORMAL)

def run_clicked():
    global run_proc
    # ensure selection persisted
    if selected_path is not None:
        try:
            with open(os.path.join(DATA_DIR, "save.txt"), "w", encoding="utf-8") as fh:
                fh.write(selected_path)
        except Exception:
            pass
    # if no process running, start one
    if run_proc is None or run_proc.poll() is not None:
        start_run_process()
    else:
        # a process is running: restart it to act as a refresh
        run_btn.config(state=DISABLED)
        old_proc = run_proc
        stop_run_process()
        _wait_and_restart(old_proc)

def close_clicked():
    stop_run_process()

# Run/Close buttons
run_btn = Button(root, text="Run cursor", command=run_clicked)
run_btn.grid(row=1, column=0, padx=10, pady=10)
close_btn = Button(root, text="Close cursor", command=close_clicked)
close_btn.grid(row=1, column=1, padx=10, pady=10)

# hover effects for buttons (only when enabled)
run_btn_default_bg = run_btn.cget("bg")
close_btn_default_bg = close_btn.cget("bg")
run_btn.bind("<Enter>", lambda e: run_btn.config(bg="lightblue") if run_btn['state'] != DISABLED else None)
run_btn.bind("<Leave>", lambda e: run_btn.config(bg=run_btn_default_bg))
close_btn.bind("<Enter>", lambda e: close_btn.config(bg="lightblue") if close_btn['state'] != DISABLED else None)
close_btn.bind("<Leave>", lambda e: close_btn.config(bg=close_btn_default_bg))

def add_clicked(f):
    f.config(borderwidth=0, relief=SUNKEN)
    subprocess.Popen(["explorer", os.path.abspath(CURSOR_DIR)])
    rtick = random.randint(16, 40)
    root.after(rtick, lambda: f.config(borderwidth=2, relief=RAISED))


# bind both frame and icon so hover/click behave consistently
add_frame.bind("<Enter>", lambda event, f=add_frame: (f.config(bg="lightblue")))
add_frame.bind("<Leave>", lambda event, f=add_frame: (f.config(bg=root.cget("bg"))))
add_frame.bind("<Button-1>", lambda event, f=add_frame: add_clicked(f))

ToolTip(add_frame, msg="Open cursors folder")

# ensure external process is stopped when the UI is closed
def _on_window_close():
    stop_run_process()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", _on_window_close)

root.mainloop()