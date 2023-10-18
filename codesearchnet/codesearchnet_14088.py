def context_to_rgb(self, str):
        """ Returns the colors that have the given word in their context.

        For example, the word "anger" appears
        in black, orange and red contexts,
        so the list will contain those three colors.

        """
        matches = []
        for clr in context:
            tags = context[clr]
            for tag in tags:
                if tag.startswith(str) \
                        or str.startswith(tag):
                    matches.append(clr)
                    break

        matches = [color(name) for name in matches]
        return matches