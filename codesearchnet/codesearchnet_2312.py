def GetPatternIdInterface(patternId: int):
    """
    Get pattern COM interface by pattern id.
    patternId: int, a value in class `PatternId`.
    Return comtypes._cominterface_meta.
    """
    global _PatternIdInterfaces
    if not _PatternIdInterfaces:
        _PatternIdInterfaces = {
            # PatternId.AnnotationPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationAnnotationPattern,
            # PatternId.CustomNavigationPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationCustomNavigationPattern,
            PatternId.DockPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationDockPattern,
            # PatternId.DragPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationDragPattern,
            # PatternId.DropTargetPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationDropTargetPattern,
            PatternId.ExpandCollapsePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationExpandCollapsePattern,
            PatternId.GridItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationGridItemPattern,
            PatternId.GridPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationGridPattern,
            PatternId.InvokePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationInvokePattern,
            PatternId.ItemContainerPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationItemContainerPattern,
            PatternId.LegacyIAccessiblePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationLegacyIAccessiblePattern,
            PatternId.MultipleViewPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationMultipleViewPattern,
            # PatternId.ObjectModelPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationObjectModelPattern,
            PatternId.RangeValuePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationRangeValuePattern,
            PatternId.ScrollItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationScrollItemPattern,
            PatternId.ScrollPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationScrollPattern,
            PatternId.SelectionItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationSelectionItemPattern,
            PatternId.SelectionPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationSelectionPattern,
            # PatternId.SpreadsheetItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetItemPattern,
            # PatternId.SpreadsheetPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetPattern,
            # PatternId.StylesPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationStylesPattern,
            PatternId.SynchronizedInputPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationSynchronizedInputPattern,
            PatternId.TableItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTableItemPattern,
            PatternId.TablePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTablePattern,
            # PatternId.TextChildPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTextChildPattern,
            # PatternId.TextEditPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTextEditPattern,
            PatternId.TextPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTextPattern,
            # PatternId.TextPattern2: _AutomationClient.instance().UIAutomationCore.IUIAutomationTextPattern2,
            PatternId.TogglePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTogglePattern,
            PatternId.TransformPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationTransformPattern,
            # PatternId.TransformPattern2: _AutomationClient.instance().UIAutomationCore.IUIAutomationTransformPattern2,
            PatternId.ValuePattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationValuePattern,
            PatternId.VirtualizedItemPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationVirtualizedItemPattern,
            PatternId.WindowPattern: _AutomationClient.instance().UIAutomationCore.IUIAutomationWindowPattern,
        }
        debug = False
        #the following patterns dosn't exist on Windows 7 or lower
        try:
            _PatternIdInterfaces[PatternId.AnnotationPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationAnnotationPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have AnnotationPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.CustomNavigationPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationCustomNavigationPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have CustomNavigationPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.DragPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationDragPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have DragPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.DropTargetPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationDropTargetPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have DropTargetPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.ObjectModelPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationObjectModelPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have ObjectModelPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.SpreadsheetItemPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetItemPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have SpreadsheetItemPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.SpreadsheetPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have SpreadsheetPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.StylesPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationStylesPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have StylesPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.TextChildPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationTextChildPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have TextChildPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.TextEditPattern] = _AutomationClient.instance().UIAutomationCore.IUIAutomationTextEditPattern
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have TextEditPattern.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.TextPattern2] = _AutomationClient.instance().UIAutomationCore.IUIAutomationTextPattern2
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have TextPattern2.', ConsoleColor.Yellow)
        try:
            _PatternIdInterfaces[PatternId.TransformPattern2] = _AutomationClient.instance().UIAutomationCore.IUIAutomationTransformPattern2
        except:
            if debug: Logger.WriteLine('UIAutomationCore does not have TransformPattern2.', ConsoleColor.Yellow)
    return _PatternIdInterfaces[patternId]