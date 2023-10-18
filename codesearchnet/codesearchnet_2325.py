def RunByHotKey(keyFunctions: dict, stopHotKey: tuple = None, exitHotKey: tuple = (ModifierKey.Control, Keys.VK_D), waitHotKeyReleased: bool = True) -> None:
    """
    Bind functions with hotkeys, the function will be run or stopped in another thread when the hotkey is pressed.
    keyFunctions: hotkey function dict, like {(uiautomation.ModifierKey.Control, uiautomation.Keys.VK_1) : func}
    stopHotKey: hotkey tuple
    exitHotKey: hotkey tuple
    waitHotKeyReleased: bool, if True, hotkey function will be triggered after the hotkey is released

    def main(stopEvent):
        while True:
            if stopEvent.is_set(): # must check stopEvent.is_set() if you want to stop when stop hotkey is pressed
                break
            print(n)
            n += 1
            stopEvent.wait(1)
        print('main exit')

    uiautomation.RunByHotKey({(uiautomation.ModifierKey.Control, uiautomation.Keys.VK_1) : main}
                        , (uiautomation.ModifierKey.Control | uiautomation.ModifierKey.Shift, uiautomation.Keys.VK_2))
    """
    from threading import Thread, Event, currentThread
    import traceback

    def getModName(theDict, theValue):
        name = ''
        for key in theDict:
            if isinstance(theDict[key], int) and theValue & theDict[key]:
                if name:
                    name += '|'
                name += key
        return name
    def getKeyName(theDict, theValue):
        for key in theDict:
            if theValue == theDict[key]:
                return key
    def releaseAllKey():
        for key, value in Keys.__dict__.items():
            if isinstance(value, int) and key.startswith('VK'):
                if IsKeyPressed(value):
                    ReleaseKey(value)
    def threadFunc(function, stopEvent, hotkey, hotkeyName):
        if waitHotKeyReleased:
            WaitHotKeyReleased(hotkey)
        try:
            function(stopEvent)
        except Exception as ex:
            Logger.ColorfullyWrite('Catch an exception <Color=Red>{}</Color> in thread for hotkey <Color=DarkCyan>{}</Color>\n'.format(
                ex.__class__.__name__, hotkeyName), writeToFile=False)
            print(traceback.format_exc())
        finally:
            releaseAllKey()  #need to release keys if some keys were pressed
            Logger.ColorfullyWrite('{} for function <Color=DarkCyan>{}</Color> exits, hotkey <Color=DarkCyan>{}</Color>\n'.format(
                currentThread(), function.__name__, hotkeyName), ConsoleColor.DarkYellow, writeToFile=False)

    stopHotKeyId = 1
    exitHotKeyId = 2
    hotKeyId = 3
    registed = True
    id2HotKey = {}
    id2Function = {}
    id2Thread = {}
    id2Name = {}
    for hotkey in keyFunctions:
        id2HotKey[hotKeyId] = hotkey
        id2Function[hotKeyId] = keyFunctions[hotkey]
        id2Thread[hotKeyId] = None
        modName = getModName(ModifierKey.__dict__, hotkey[0])
        keyName = getKeyName(Keys.__dict__, hotkey[1])
        id2Name[hotKeyId] = str((modName, keyName))
        if ctypes.windll.user32.RegisterHotKey(0, hotKeyId, hotkey[0], hotkey[1]):
            Logger.ColorfullyWrite('Register hotkey <Color=DarkGreen>{}</Color> successfully\n'.format((modName, keyName)), writeToFile=False)
        else:
            registed = False
            Logger.ColorfullyWrite('Register hotkey <Color=DarkGreen>{}</Color> unsuccessfully, maybe it was allready registered by another program\n'.format((modName, keyName)), writeToFile=False)
        hotKeyId += 1
    if stopHotKey and len(stopHotKey) == 2:
        modName = getModName(ModifierKey.__dict__, stopHotKey[0])
        keyName = getKeyName(Keys.__dict__, stopHotKey[1])
        if ctypes.windll.user32.RegisterHotKey(0, stopHotKeyId, stopHotKey[0], stopHotKey[1]):
            Logger.ColorfullyWrite('Register stop hotkey <Color=DarkYellow>{}</Color> successfully\n'.format((modName, keyName)), writeToFile=False)
        else:
            registed = False
            Logger.ColorfullyWrite('Register stop hotkey <Color=DarkYellow>{}</Color> unsuccessfully, maybe it was allready registered by another program\n'.format((modName, keyName)), writeToFile=False)
    if not registed:
        return
    if exitHotKey and len(exitHotKey) == 2:
        modName = getModName(ModifierKey.__dict__, exitHotKey[0])
        keyName = getKeyName(Keys.__dict__, exitHotKey[1])
        if ctypes.windll.user32.RegisterHotKey(0, exitHotKeyId, exitHotKey[0], exitHotKey[1]):
            Logger.ColorfullyWrite('Register exit hotkey <Color=DarkYellow>{}</Color> successfully\n'.format((modName, keyName)), writeToFile=False)
        else:
            Logger.ColorfullyWrite('Register exit hotkey <Color=DarkYellow>{}</Color> unsuccessfully\n'.format((modName, keyName)), writeToFile=False)
    funcThread = None
    livingThreads = []
    stopEvent = Event()
    msg = ctypes.wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), ctypes.c_void_p(0), 0, 0) != 0:
        if msg.message == 0x0312: # WM_HOTKEY=0x0312
            if msg.wParam in id2HotKey:
                if msg.lParam & 0x0000FFFF == id2HotKey[msg.wParam][0] and msg.lParam >> 16 & 0x0000FFFF == id2HotKey[msg.wParam][1]:
                    Logger.ColorfullyWrite('----------hotkey <Color=DarkGreen>{}</Color> pressed----------\n'.format(id2Name[msg.wParam]), writeToFile=False)
                    if not id2Thread[msg.wParam]:
                        stopEvent.clear()
                        funcThread = Thread(None, threadFunc, args=(id2Function[msg.wParam], stopEvent, id2HotKey[msg.wParam], id2Name[msg.wParam]))
                        funcThread.start()
                        id2Thread[msg.wParam] = funcThread
                    else:
                        if id2Thread[msg.wParam].is_alive():
                            Logger.WriteLine('There is a {} that is already running for hotkey {}'.format(id2Thread[msg.wParam], id2Name[msg.wParam]), ConsoleColor.Yellow, writeToFile=False)
                        else:
                            stopEvent.clear()
                            funcThread = Thread(None, threadFunc, args=(id2Function[msg.wParam], stopEvent, id2HotKey[msg.wParam], id2Name[msg.wParam]))
                            funcThread.start()
                            id2Thread[msg.wParam] = funcThread
            elif stopHotKeyId == msg.wParam:
                if msg.lParam & 0x0000FFFF == stopHotKey[0] and msg.lParam >> 16 & 0x0000FFFF == stopHotKey[1]:
                    Logger.Write('----------stop hotkey pressed----------\n', ConsoleColor.DarkYellow, writeToFile=False)
                    stopEvent.set()
                    for id_ in id2Thread:
                        if id2Thread[id_]:
                            if id2Thread[id_].is_alive():
                                livingThreads.append((id2Thread[id_], id2Name[id_]))
                            id2Thread[id_] = None
            elif exitHotKeyId == msg.wParam:
                if msg.lParam & 0x0000FFFF == exitHotKey[0] and msg.lParam >> 16 & 0x0000FFFF == exitHotKey[1]:
                    Logger.Write('Exit hotkey pressed. Exit\n', ConsoleColor.DarkYellow, writeToFile=False)
                    stopEvent.set()
                    for id_ in id2Thread:
                        if id2Thread[id_]:
                            if id2Thread[id_].is_alive():
                                livingThreads.append((id2Thread[id_], id2Name[id_]))
                            id2Thread[id_] = None
                    break
    for thread, hotkeyName in livingThreads:
        if thread.is_alive():
            Logger.Write('join {} triggered by hotkey {}\n'.format(thread, hotkeyName), ConsoleColor.DarkYellow, writeToFile=False)
            thread.join(2)
    os._exit(0)