def Select(self, itemName: str = '', condition: Callable = None, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Show combobox's popup menu and select a item by name.
        itemName: str.
        condition: Callable function(comboBoxItemName: str)->bool, if condition is valid, ignore itemName.
        waitTime: float.
        Some comboboxs doesn't support SelectionPattern, here is a workaround.
        This method tries to and selection support.
        It may not work for some comboboxes, such as comboboxes in older Qt version.
        If it doesn't work, you should write your own version Select, or it doesn't support selection at all.
        """
        expandCollapsePattern = self.GetExpandCollapsePattern()
        if expandCollapsePattern:
            expandCollapsePattern.Expand()
        else:
            #Windows Form's ComboBoxControl doesn't support ExpandCollapsePattern
            self.Click(x=-10, ratioY=0.5, simulateMove=False)
        find = False
        if condition:
            listItemControl = self.ListItemControl(Compare=lambda c, d: condition(c.Name))
        else:
            listItemControl = self.ListItemControl(Name=itemName)
        if listItemControl.Exists(1):
            scrollItemPattern = listItemControl.GetScrollItemPattern()
            if scrollItemPattern:
                scrollItemPattern.ScrollIntoView(waitTime=0.1)
            listItemControl.Click(waitTime=waitTime)
            find = True
        else:
            #ComboBox's popup window is a child of root control
            listControl = ListControl(searchDepth= 1)
            if listControl.Exists(1):
                if condition:
                    listItemControl = self.ListItemControl(Compare=lambda c, d: condition(c.Name))
                else:
                    listItemControl = self.ListItemControl(Name=itemName)
                if listItemControl.Exists(0, 0):
                    scrollItemPattern = listItemControl.GetScrollItemPattern()
                    if scrollItemPattern:
                        scrollItemPattern.ScrollIntoView(waitTime=0.1)
                    listItemControl.Click(waitTime=waitTime)
                    find = True
        if not find:
            Logger.ColorfullyWriteLine('Can\'t find <Color=Cyan>{}</Color> in ComboBoxControl or it does not support selection.'.format(itemName), ConsoleColor.Yellow)
            if expandCollapsePattern:
                expandCollapsePattern.Collapse(waitTime)
            else:
                self.Click(x=-10, ratioY=0.5, simulateMove=False, waitTime=waitTime)
        return find