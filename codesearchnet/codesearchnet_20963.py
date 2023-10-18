def handle_extends(self, text):
        """replace all blocks in extends with current blocks"""
        match = self.re_extends.match(text)
        if match:
            extra_text = self.re_extends.sub('', text, count=1)
            blocks = self.get_blocks(extra_text)
            path = os.path.join(self.base_dir, match.group('path'))
            with open(path, encoding='utf-8') as fp:
                return self.replace_blocks_in_extends(fp.read(), blocks)
        else:
            return None