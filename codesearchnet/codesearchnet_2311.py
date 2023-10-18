def SendKeys(text: str, interval: float = 0.01, waitTime: float = OPERATION_WAIT_TIME, debug: bool = False) -> None:
    """
    Simulate typing keys on keyboard.
    text: str, keys to type.
    interval: float, seconds between keys.
    waitTime: float.
    debug: bool, if True, print the keys.
    Examples:
    {Ctrl}, {Delete} ... are special keys' name in SpecialKeyNames.
    SendKeys('{Ctrl}a{Delete}{Ctrl}v{Ctrl}s{Ctrl}{Shift}s{Win}e{PageDown}') #press Ctrl+a, Delete, Ctrl+v, Ctrl+s, Ctrl+Shift+s, Win+e, PageDown
    SendKeys('{Ctrl}(AB)({Shift}(123))') #press Ctrl+A+B, type (, press Shift+1+2+3, type ), if () follows a hold key, hold key won't release util )
    SendKeys('{Ctrl}{a 3}') #press Ctrl+a at the same time, release Ctrl+a, then type a 2 times
    SendKeys('{a 3}{B 5}') #type a 3 times, type B 5 times
    SendKeys('{{}Hello{}}abc {a}{b}{c} test{} 3}{!}{a} (){(}{)}') #type: {Hello}abc abc test}}}!a ()()
    SendKeys('0123456789{Enter}')
    SendKeys('ABCDEFGHIJKLMNOPQRSTUVWXYZ{Enter}')
    SendKeys('abcdefghijklmnopqrstuvwxyz{Enter}')
    SendKeys('`~!@#$%^&*()-_=+{Enter}')
    SendKeys('[]{{}{}}\\|;:\'\",<.>/?{Enter}')
    """
    holdKeys = ('WIN', 'LWIN', 'RWIN', 'SHIFT', 'LSHIFT', 'RSHIFT', 'CTRL', 'CONTROL', 'LCTRL', 'RCTRL', 'LCONTROL', 'LCONTROL', 'ALT', 'LALT', 'RALT')
    keys = []
    printKeys = []
    i = 0
    insertIndex = 0
    length = len(text)
    hold = False
    include = False
    lastKeyValue = None
    while True:
        if text[i] == '{':
            rindex = text.find('}', i)
            if rindex == i + 1:#{}}
                rindex = text.find('}', i + 2)
            if rindex == -1:
                raise ValueError('"{" or "{}" is not valid, use "{{}" for "{", use "{}}" for "}"')
            key = text[i + 1:rindex]
            key = [it for it in key.split(' ') if it]
            if not key:
                raise ValueError('"{}" is not valid, use "{{Space}}" or " " for " "'.format(text[i:rindex + 1]))
            if (len(key) == 2 and not key[1].isdigit()) or len(key) > 2:
                raise ValueError('"{}" is not valid'.format(text[i:rindex + 1]))
            upperKey = key[0].upper()
            count = 1
            if len(key) > 1:
                count = int(key[1])
            for j in range(count):
                if hold:
                    if upperKey in SpecialKeyNames:
                        keyValue = SpecialKeyNames[upperKey]
                        if type(lastKeyValue) == type(keyValue) and lastKeyValue == keyValue:
                            insertIndex += 1
                        printKeys.insert(insertIndex, (key[0], 'KeyDown | ExtendedKey'))
                        printKeys.insert(insertIndex + 1, (key[0], 'KeyUp | ExtendedKey'))
                        keys.insert(insertIndex, (keyValue, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey))
                        keys.insert(insertIndex + 1, (keyValue, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey))
                        lastKeyValue = keyValue
                    elif key[0] in CharacterCodes:
                        keyValue = CharacterCodes[key[0]]
                        if type(lastKeyValue) == type(keyValue) and lastKeyValue == keyValue:
                            insertIndex += 1
                        printKeys.insert(insertIndex, (key[0], 'KeyDown | ExtendedKey'))
                        printKeys.insert(insertIndex + 1, (key[0], 'KeyUp | ExtendedKey'))
                        keys.insert(insertIndex, (keyValue, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey))
                        keys.insert(insertIndex + 1, (keyValue, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey))
                        lastKeyValue = keyValue
                    else:
                        printKeys.insert(insertIndex, (key[0], 'UnicodeChar'))
                        keys.insert(insertIndex, (key[0], 'UnicodeChar'))
                        lastKeyValue = key[0]
                    if include:
                        insertIndex += 1
                    else:
                        if upperKey in holdKeys:
                            insertIndex += 1
                        else:
                            hold = False
                else:
                    if upperKey in SpecialKeyNames:
                        keyValue = SpecialKeyNames[upperKey]
                        printKeys.append((key[0], 'KeyDown | ExtendedKey'))
                        printKeys.append((key[0], 'KeyUp | ExtendedKey'))
                        keys.append((keyValue, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey))
                        keys.append((keyValue, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey))
                        lastKeyValue = keyValue
                        if upperKey in holdKeys:
                            hold = True
                            insertIndex = len(keys) - 1
                        else:
                            hold = False
                    else:
                        printKeys.append((key[0], 'UnicodeChar'))
                        keys.append((key[0], 'UnicodeChar'))
                        lastKeyValue = key[0]
            i = rindex + 1
        elif text[i] == '(':
            if hold:
                include = True
            else:
                printKeys.append((text[i], 'UnicodeChar'))
                keys.append((text[i], 'UnicodeChar'))
                lastKeyValue = text[i]
            i += 1
        elif text[i] == ')':
            if hold:
                include = False
                hold = False
            else:
                printKeys.append((text[i], 'UnicodeChar'))
                keys.append((text[i], 'UnicodeChar'))
                lastKeyValue = text[i]
            i += 1
        else:
            if hold:
                if text[i] in CharacterCodes:
                    keyValue = CharacterCodes[text[i]]
                    if include and type(lastKeyValue) == type(keyValue) and lastKeyValue == keyValue:
                        insertIndex += 1
                    printKeys.insert(insertIndex, (text[i], 'KeyDown | ExtendedKey'))
                    printKeys.insert(insertIndex + 1, (text[i], 'KeyUp | ExtendedKey'))
                    keys.insert(insertIndex, (keyValue, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey))
                    keys.insert(insertIndex + 1, (keyValue, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey))
                    lastKeyValue = keyValue
                else:
                    printKeys.append((text[i], 'UnicodeChar'))
                    keys.append((text[i], 'UnicodeChar'))
                    lastKeyValue = text[i]
                if include:
                    insertIndex += 1
                else:
                    hold = False
            else:
                printKeys.append((text[i], 'UnicodeChar'))
                keys.append((text[i], 'UnicodeChar'))
                lastKeyValue = text[i]
            i += 1
        if i >= length:
            break
    hotkeyInterval = 0.01
    for i, key in enumerate(keys):
        if key[1] == 'UnicodeChar':
            SendUnicodeChar(key[0])
            time.sleep(interval)
            if debug:
                Logger.ColorfullyWrite('<Color=DarkGreen>{}</Color>, sleep({})\n'.format(printKeys[i], interval), writeToFile=False)
        else:
            scanCode = _VKtoSC(key[0])
            keybd_event(key[0], scanCode, key[1], 0)
            if debug:
                Logger.Write(printKeys[i], ConsoleColor.DarkGreen, writeToFile=False)
            if i + 1 == len(keys):
                time.sleep(interval)
                if debug:
                    Logger.Write(', sleep({})\n'.format(interval), writeToFile=False)
            else:
                if key[1] & KeyboardEventFlag.KeyUp:
                    if keys[i + 1][1] == 'UnicodeChar' or keys[i + 1][1] & KeyboardEventFlag.KeyUp == 0:
                        time.sleep(interval)
                        if debug:
                            Logger.Write(', sleep({})\n'.format(interval), writeToFile=False)
                    else:
                        time.sleep(hotkeyInterval)  #must sleep for a while, otherwise combined keys may not be caught
                        if debug:
                            Logger.Write(', sleep({})\n'.format(hotkeyInterval), writeToFile=False)
                else:  #KeyboardEventFlag.KeyDown
                    time.sleep(hotkeyInterval)
                    if debug:
                        Logger.Write(', sleep({})\n'.format(hotkeyInterval), writeToFile=False)
    #make sure hold keys are not pressed
    #win = ctypes.windll.user32.GetAsyncKeyState(Keys.VK_LWIN)
    #ctrl = ctypes.windll.user32.GetAsyncKeyState(Keys.VK_CONTROL)
    #alt = ctypes.windll.user32.GetAsyncKeyState(Keys.VK_MENU)
    #shift = ctypes.windll.user32.GetAsyncKeyState(Keys.VK_SHIFT)
    #if win & 0x8000:
        #Logger.WriteLine('ERROR: WIN is pressed, it should not be pressed!', ConsoleColor.Red)
        #keybd_event(Keys.VK_LWIN, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    #if ctrl & 0x8000:
        #Logger.WriteLine('ERROR: CTRL is pressed, it should not be pressed!', ConsoleColor.Red)
        #keybd_event(Keys.VK_CONTROL, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    #if alt & 0x8000:
        #Logger.WriteLine('ERROR: ALT is pressed, it should not be pressed!', ConsoleColor.Red)
        #keybd_event(Keys.VK_MENU, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    #if shift & 0x8000:
        #Logger.WriteLine('ERROR: SHIFT is pressed, it should not be pressed!', ConsoleColor.Red)
        #keybd_event(Keys.VK_SHIFT, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    time.sleep(waitTime)