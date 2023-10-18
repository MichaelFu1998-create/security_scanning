def TK_message(title,msg):
    """use the GUI to pop up a message."""
    root = tkinter.Tk()
    root.withdraw() #hide tk window
    root.attributes("-topmost", True) #always on top
    root.lift() #bring to top
    tkinter.messagebox.showwarning(title, msg)
    root.destroy()