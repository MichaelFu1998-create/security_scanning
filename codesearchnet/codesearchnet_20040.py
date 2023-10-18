def gui_getFolder():
    """
    Launch a folder selection dialog.
    This is smart, and remembers (through reboots) where you last were.
    """
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk() # this is natively supported by python
    root.withdraw() # hide main window
    root.wm_attributes('-topmost', 1) # always on top
    fname = filedialog.askdirectory(title = "select folder of ABFs",
                                       initialdir=os.path.dirname(abfFname_Load()))
    if len(fname)>3:
        abfFname_Save(fname+"/_._")
        return fname
    else:
        print("didn't select an ABF!")
        return None