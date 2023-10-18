def scale_context_and_center(self, cr):
        """
        Scale context based on difference between bot size and widget
        """
        bot_width, bot_height = self.bot_size
        if self.width != bot_width or self.height != bot_height:
            # Scale up by largest dimension
            if self.width < self.height:
                scale_x = float(self.width) / float(bot_width)
                scale_y = scale_x
                cr.translate(0, (self.height - (bot_height * scale_y)) / 2.0)
            elif self.width > self.height:
                scale_y = float(self.height) / float(bot_height)
                scale_x = scale_y
                cr.translate((self.width - (bot_width * scale_x)) / 2.0, 0)
            else:
                scale_x = 1.0
                scale_y = 1.0
            cr.scale(scale_x, scale_y)
            self.input_device.scale_x = scale_y
            self.input_device.scale_y = scale_y