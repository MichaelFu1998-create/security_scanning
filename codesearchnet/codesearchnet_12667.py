def sort(self, sort_list):
        """ Sort """
        order = []
        for sort in sort_list:
            if sort_list[sort] == "asc":
                order.append(asc(getattr(self.model, sort, None)))
            elif sort_list[sort] == "desc":
                order.append(desc(getattr(self.model, sort, None)))
        return order