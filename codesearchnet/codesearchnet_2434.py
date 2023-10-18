def threadFunc(root):
    """
    If you want to use functionalities related to Controls and Patterns in a new thread.
    You must call InitializeUIAutomationInCurrentThread first in the thread
        and call UninitializeUIAutomationInCurrentThread when the thread exits.
    But you can't use use a Control or a Pattern created in a different thread.
    So you can't create a Control or a Pattern in main thread and then pass it to a new thread and use it.
    """
    #print(root)# you cannot use root because it is root control created in main thread
    th = threading.currentThread()
    auto.Logger.WriteLine('\nThis is running in a new thread. {} {}'.format(th.ident, th.name), auto.ConsoleColor.Cyan)
    time.sleep(2)
    auto.InitializeUIAutomationInCurrentThread()
    auto.GetConsoleWindow().CaptureToImage('console_newthread.png')
    newRoot = auto.GetRootControl()    #ok, root control created in new thread
    auto.EnumAndLogControl(newRoot, 1)
    auto.UninitializeUIAutomationInCurrentThread()
    auto.Logger.WriteLine('\nThread exits. {} {}'.format(th.ident, th.name), auto.ConsoleColor.Cyan)