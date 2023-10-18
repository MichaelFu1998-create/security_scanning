def summarized_name(self, name):
        """
        Produce a summarized record name
          i.e. manticore.core.executor -> m.c.executor
        """
        components = name.split('.')
        prefix = '.'.join(c[0] for c in components[:-1])
        return f'{prefix}.{components[-1]}'