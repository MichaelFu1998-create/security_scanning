def age(self):
        """
        Get closer to your EOL
        """
        # 0 means this composer will never decompose
        if self.rounds == 1:
            self.do_run = False
        elif self.rounds > 1:
            self.rounds -= 1