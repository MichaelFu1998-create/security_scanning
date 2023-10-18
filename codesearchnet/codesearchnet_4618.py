def visualize(self, display=True):
        """!
        @brief Display KD-tree to console.
        
        @param[in] display (bool): If 'True' then tree will be shown in console.
        
        @return (string) Text representation of the KD-tree.
        
        """

        kdnodes = self.__get_nodes()
        level = kdnodes[0]
        
        for kdnode in kdnodes:
            self.__print_node(level, kdnode)

        self.__tree_text += self.__tree_level_text
        if display is True:
            print(self.__tree_text)
        
        return self.__tree_text