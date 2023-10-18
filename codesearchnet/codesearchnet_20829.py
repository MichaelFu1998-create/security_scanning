def on_key_press(self, key, modifiers, keymap):
        '''Handle an otherwise unhandled keypress event (from a GUI).'''
        if key == keymap.ENTER:
            self.reset()
            return True