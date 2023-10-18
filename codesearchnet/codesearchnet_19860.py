def TK_ask(title,msg):
    """use the GUI to ask YES or NO."""
    root = tkinter.Tk()
    root.attributes("-topmost", True) #always on top
    root.withdraw() #hide tk window
    result=tkinter.messagebox.askyesno(title,msg)
    root.destroy()
    return result