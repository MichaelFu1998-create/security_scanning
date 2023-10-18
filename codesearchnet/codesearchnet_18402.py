def parse(self, file):
        """Parse text blocks from a file."""
        if isinstance(file, basestring):
            file = open(file)
        line_number = 0
        label = None
        block = self.untagged
        for line in file:
            line_number += 1
            line = line.rstrip('\n')
            if self.tabsize > 0:
                line = line.replace('\t', ' ' * self.tabsize)
            if self.decommenter:
                line = self.decommenter.decomment(line)
                if line is None:
                    continue
            tag = line.split(':', 1)[0].strip()
            # Still in the same block?
            if tag not in self.names:
                if block is None:
                    if line and not line.isspace():
                        raise ParseError(file.name, line, "garbage before first block: %r" % line)
                    continue
                block.addline(line)
                continue
            # Open a new block.
            name = self.names[tag]
            label = line.split(':',1)[1].strip()
            if name in self.labelled_classes:
                if not label:
                    raise ParseError(file.name, line, "missing label for %r block" % name)
                block = self.blocks[name].setdefault(label, self.labelled_classes[name]())
            else:
                if label:
                    msg = "label %r present for unlabelled block %r" % (label, name)
                    raise ParseError(file.name, line_number, msg)
                block = self.blocks[name]
            block.startblock()