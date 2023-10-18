def main():
        """
        If a project has a Curses driver, the section "main" in the section
        "run" must be "bibliopixel.drivers.curses.Curses.main".

        """
        if not _curses:
            # https://stackoverflow.com/a/1325587/43839
            if os.name == 'nt':
                raise ValueError('curses is not supported under Windows')
            raise ValueError('Your platform does not support curses.')
        try:
            driver = next(iter(Curses.DRIVERS))
        except:
            raise ValueError('No Curses driver in project')

        _curses.wrapper(driver.run_in_curses)