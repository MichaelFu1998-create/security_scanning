def get_summarizer(self, name):
        '''
        import summarizers on-demand
        '''
        if name in self.summarizers:
            pass
        elif name == 'lexrank':
            from . import lexrank
            self.summarizers[name] = lexrank.summarize
        elif name == 'mcp':
            from . import mcp_summ
            self.summarizers[name] = mcp_summ.summarize

        return self.summarizers[name]