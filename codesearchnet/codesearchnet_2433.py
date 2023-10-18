def DemoEN():
    """for other language"""
    thisWindow = auto.GetConsoleWindow()
    auto.Logger.ColorfullyWrite('I will run <Color=Cyan>cmd</Color>\n\n')
    time.sleep(3)

    auto.SendKeys('{Win}r')
    while not isinstance(auto.GetFocusedControl(), auto.EditControl):
        time.sleep(1)
    auto.SendKeys('cmd{Enter}')
    cmdWindow = auto.WindowControl(SubName = 'cmd.exe')
    rect = cmdWindow.BoundingRectangle
    auto.DragDrop(rect.left + 50, rect.top + 10, 50, 10)

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('I will run <Color=Cyan>Notepad</Color> and type <Color=Cyan>Hello!!!</Color>\n\n')
    time.sleep(3)

    subprocess.Popen('notepad')
    notepadWindow = auto.WindowControl(searchDepth = 1, ClassName = 'Notepad')
    cx, cy = auto.GetScreenSize()
    notepadWindow.MoveWindow(cx // 2, 20, cx // 2, cy // 2)
    time.sleep(0.5)
    notepadWindow.EditControl().SendKeys('Hello!!!', 0.05)
    time.sleep(1)

    dir = os.path.dirname(__file__)
    scriptPath = os.path.abspath(os.path.join(dir, '..\\automation.py'))

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('run "<Color=Cyan>automation.py -h</Color>" to display the help\n\n')
    time.sleep(3)

    cmdWindow.SendKeys('"{}" -h'.format(scriptPath) + '{Enter}', 0.05)
    time.sleep(3)

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('run "<Color=Cyan>automation.py -r -d1</Color>" to display the top level windows, desktop\'s children\n\n')
    time.sleep(3)

    cmdWindow.SendKeys('"{}" -r -d1 -t0'.format(scriptPath) + '{Enter}', 0.05)
    time.sleep(3)

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('run "<Color=Cyan>automation.py -c</Color>" to display the control under mouse cursor\n\n')
    time.sleep(3)

    cmdWindow.SendKeys('"{}" -c -t3'.format(scriptPath) + '{Enter}', 0.05)
    notepadWindow.SetActive()
    notepadWindow.MoveCursorToMyCenter()
    time.sleep(3)
    cmdWindow.SetActive(waitTime = 2)

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('run "<Color=Cyan>automation.py -a</Color>" to display the control under mouse cursor and its ancestors\n\n')
    time.sleep(3)

    cmdWindow.SendKeys('"{}" -a -t3'.format(scriptPath) + '{Enter}', 0.05)
    notepadWindow.SetActive()
    notepadWindow.MoveCursorToMyCenter()
    time.sleep(3)
    cmdWindow.SetActive(waitTime = 2)

    thisWindow.SetActive()
    auto.Logger.ColorfullyWrite('run "<Color=Cyan>automation.py</Color>" to display the active window\n\n')
    time.sleep(3)

    cmdWindow.SendKeys('"{}" -t3'.format(scriptPath) + '{Enter}', 0.05)
    notepadWindow.SetActive()
    notepadWindow.EditControl().Click()
    time.sleep(3)
    cmdWindow.SetActive(waitTime = 2)
    time.sleep(3)

    thisWindow.SetActive()
    auto.Logger.WriteLine('press Enter to exit', auto.ConsoleColor.Green)
    input()