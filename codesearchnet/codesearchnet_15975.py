def get_shark_field(self, fields):
        """
        :fields: str[]
        """
        out = super(BACK, self).get_shark_field(fields)
        out.update({'acked_seqs': self.acked_seqs,
                    'bitmap_str': self.bitmap_str})
        return out