def launch(title, items, selected=None):
        """
        Launches a new menu. Wraps curses nicely so exceptions won't screw with
        the terminal too much.
        """
        resp = {"code": -1, "done": False}
        curses.wrapper(Menu, title, items, selected, resp)
        return resp