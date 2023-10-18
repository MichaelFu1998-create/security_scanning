def gui_getFile():
    """
    Launch an ABF file selection file dialog.
    This is smart, and remembers (through reboots) where you last were.
    """
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk() # this is natively supported by python
    root.withdraw() # hide main window
    root.wm_attributes('-topmost', 1) # always on top
    fname = filedialog.askopenfilename(title = "select ABF file",
                                       filetypes=[('ABF Files', '.abf')],
                                       initialdir=os.path.dirname(abfFname_Load()))
    if fname.endswith(".abf"):
        abfFname_Save(fname)
        return fname
    else:
        print("didn't select an ABF!")
        return None