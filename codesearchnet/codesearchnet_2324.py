def WaitHotKeyReleased(hotkey: tuple) -> None:
    """hotkey: tuple, two ints tuple(modifierKey, key)"""
    mod = {ModifierKey.Alt: Keys.VK_MENU,
           ModifierKey.Control: Keys.VK_CONTROL,
                 ModifierKey.Shift: Keys.VK_SHIFT,
                 ModifierKey.Win: Keys.VK_LWIN
           }
    while True:
        time.sleep(0.05)
        if IsKeyPressed(hotkey[1]):
            continue
        for k, v in mod.items():
            if k & hotkey[0]:
                if IsKeyPressed(v):
                    break
        else:
            break