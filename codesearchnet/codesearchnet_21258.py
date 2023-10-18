def draw_interface(objects, callback, callback_text):
    """
        Draws a ncurses interface. Based on the given object list, every object should have a "string" key, this is whats displayed on the screen, callback is called with the selected object.
        Rest of the code is modified from:
        https://stackoverflow.com/a/30834868
    """
    screen = curses.initscr()
    height, width = screen.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlightText = curses.color_pair( 1 )
    normalText = curses.A_NORMAL
    screen.border( 0 )
    curses.curs_set( 0 )
    max_row = height - 15 # max number of rows
    box = curses.newwin( max_row + 2, int(width - 2), 1, 1 )
    box.box()
    fmt = PartialFormatter()

    row_num = len( objects )

    pages = int( ceil( row_num / max_row ) )
    position = 1
    page = 1
    for i in range( 1, max_row + 1 ):
        if row_num == 0:
            box.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if (i == position):
                box.addstr( i, 2, str( i ) + " - " + objects[ i - 1 ]['string'], highlightText )
            else:
                box.addstr( i, 2, str( i ) + " - " + objects[ i - 1 ]['string'], normalText )
            if i == row_num:
                break

    screen.refresh()
    box.refresh()

    x = screen.getch()
    while x != 27:
        if x == curses.KEY_DOWN:
            if page == 1:
                if position < i:
                    position = position + 1
                else:
                    if pages > 1:
                        page = page + 1
                        position = 1 + ( max_row * ( page - 1 ) )
            elif page == pages:
                if position < row_num:
                    position = position + 1
            else:
                if position < max_row + ( max_row * ( page - 1 ) ):
                    position = position + 1
                else:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
        if x == curses.KEY_UP:
            if page == 1:
                if position > 1:
                    position = position - 1
            else:
                if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                    position = position - 1
                else:
                    page = page - 1
                    position = max_row + ( max_row * ( page - 1 ) )

        screen.erase()
        if x == ord( "\n" ) and row_num != 0:
            screen.erase()
            screen.border( 0 )
            service = objects[position -1]
            text = fmt.format(callback_text, **service)
            screen.addstr( max_row + 4, 3, text)
            text  = callback(service)
            count = 0
            for line in text:
                screen.addstr( max_row + 5 + count, 3, line)
                count += 1

        box.erase()
        screen.border( 0 )
        box.border( 0 )

        for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
            if row_num == 0:
                box.addstr( 1, 1, "There aren't strings",  highlightText )
            else:
                if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + objects[ i - 1 ]['string'], highlightText )
                else:
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + objects[ i - 1 ]['string'], normalText )
                if i == row_num:
                    break

        screen.refresh()
        box.refresh()
        x = screen.getch()

    curses.endwin()
    exit()