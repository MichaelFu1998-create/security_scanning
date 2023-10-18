def TK_askPassword(title="input",msg="type here:"):
    """use the GUI to ask for a string."""
    root = tkinter.Tk()
    root.withdraw() #hide tk window
    root.attributes("-topmost", True) #always on top
    root.lift() #bring to top
    value=tkinter.simpledialog.askstring(title,msg)
    root.destroy()
    return value