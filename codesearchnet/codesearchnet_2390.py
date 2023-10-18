def GetColorfulSearchPropertiesStr(self, keyColor='DarkGreen', valueColor='DarkCyan') -> str:
        """keyColor, valueColor: str, color name in class ConsoleColor"""
        strs = ['<Color={}>{}</Color>: <Color={}>{}</Color>'.format(keyColor if k in Control.ValidKeys else 'DarkYellow', k, valueColor,
                ControlTypeNames[v] if k == 'ControlType' else repr(v)) for k, v in self.searchProperties.items()]
        return '{' + ', '.join(strs) + '}'