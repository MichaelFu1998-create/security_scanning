def LogControl(control: Control, depth: int = 0, showAllName: bool = True) -> None:
    """
    Print and log control's properties.
    control: `Control` or its subclass.
    depth: int, current depth.
    showAllName: bool, if False, print the first 30 characters of control.Name.
    """
    def getKeyName(theDict, theValue):
        for key in theDict:
            if theValue == theDict[key]:
                return key
    indent = ' ' * depth * 4
    Logger.Write('{0}ControlType: '.format(indent))
    Logger.Write(control.ControlTypeName, ConsoleColor.DarkGreen)
    Logger.Write('    ClassName: ')
    Logger.Write(control.ClassName, ConsoleColor.DarkGreen)
    Logger.Write('    AutomationId: ')
    Logger.Write(control.AutomationId, ConsoleColor.DarkGreen)
    Logger.Write('    Rect: ')
    Logger.Write(control.BoundingRectangle, ConsoleColor.DarkGreen)
    Logger.Write('    Name: ')
    Logger.Write(control.Name, ConsoleColor.DarkGreen, printTruncateLen=0 if showAllName else 30)
    Logger.Write('    Handle: ')
    Logger.Write('0x{0:X}({0})'.format(control.NativeWindowHandle), ConsoleColor.DarkGreen)
    Logger.Write('    Depth: ')
    Logger.Write(depth, ConsoleColor.DarkGreen)
    supportedPatterns = list(filter(lambda t: t[0], ((control.GetPattern(id_), name) for id_, name in PatternIdNames.items())))
    for pt, name in supportedPatterns:
        if isinstance(pt, ValuePattern):
            Logger.Write('    ValuePattern.Value: ')
            Logger.Write(pt.Value, ConsoleColor.DarkGreen, printTruncateLen=0 if showAllName else 30)
        elif isinstance(pt, RangeValuePattern):
            Logger.Write('    RangeValuePattern.Value: ')
            Logger.Write(pt.Value, ConsoleColor.DarkGreen)
        elif isinstance(pt, TogglePattern):
            Logger.Write('    TogglePattern.ToggleState: ')
            Logger.Write('ToggleState.' + getKeyName(ToggleState.__dict__, pt.ToggleState), ConsoleColor.DarkGreen)
        elif isinstance(pt, SelectionItemPattern):
            Logger.Write('    SelectionItemPattern.IsSelected: ')
            Logger.Write(pt.IsSelected, ConsoleColor.DarkGreen)
        elif isinstance(pt, ExpandCollapsePattern):
            Logger.Write('    ExpandCollapsePattern.ExpandCollapseState: ')
            Logger.Write('ExpandCollapseState.' + getKeyName(ExpandCollapseState.__dict__, pt.ExpandCollapseState), ConsoleColor.DarkGreen)
        elif isinstance(pt, ScrollPattern):
            Logger.Write('    ScrollPattern.HorizontalScrollPercent: ')
            Logger.Write(pt.HorizontalScrollPercent, ConsoleColor.DarkGreen)
            Logger.Write('    ScrollPattern.VerticalScrollPercent: ')
            Logger.Write(pt.VerticalScrollPercent, ConsoleColor.DarkGreen)
        elif isinstance(pt, GridPattern):
            Logger.Write('    GridPattern.RowCount: ')
            Logger.Write(pt.RowCount, ConsoleColor.DarkGreen)
            Logger.Write('    GridPattern.ColumnCount: ')
            Logger.Write(pt.ColumnCount, ConsoleColor.DarkGreen)
        elif isinstance(pt, GridItemPattern):
            Logger.Write('    GridItemPattern.Row: ')
            Logger.Write(pt.Column, ConsoleColor.DarkGreen)
            Logger.Write('    GridItemPattern.Column: ')
            Logger.Write(pt.Column, ConsoleColor.DarkGreen)
        elif isinstance(pt, TextPattern):
            Logger.Write('    TextPattern.Text: ')
            Logger.Write(pt.DocumentRange.GetText(30), ConsoleColor.DarkGreen)
    Logger.Write('    SupportedPattern:')
    for pt, name in supportedPatterns:
        Logger.Write(' ' + name, ConsoleColor.DarkGreen)
    Logger.Write('\n')