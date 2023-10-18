def summarize(self, text=None, algo=u'lexrank', **summarizer_params):
        '''
        Args:
          text: text to be summarized
          algo: summarizaion algorithm
              - 'lexrank' (default) graph-based
              - 'clexrank' Continuous LexRank
              - 'divrank' DivRank (Diverse Rank)
              - 'mcp' select sentences in terms of maximum coverage problem

          summarizer_params examples:
            char_limit: summary length (the number of characters)
            sent_limit: (not supported with mcp)
              summary length (the number of sentences)
            imp_require: (lexrank only)
              cumulative LexRank score [0.0-1.0]
        '''
        try:  # TODO: generate more useful error message
            # fix parameter type
            for param, value in summarizer_params.items():
                if value == '':
                    del summarizer_params[param]
                    continue
                elif re.match(r'^\d*.\d+$', value):
                    value = float(value)
                elif re.match(r'^\d+$', value):
                    value = int(value)
                elif value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                summarizer_params[param] = value

            if algo in ('lexrank', 'clexrank', 'divrank'):
                summarizer = self.get_summarizer('lexrank')
                if algo == 'clexrank':
                    summarizer_params['continuous'] = True
                if algo == 'divrank':
                    summarizer_params['use_divrank'] = True
            elif algo == 'mcp':
                summarizer = self.get_summarizer('mcp')

            summary, debug_info = summarizer(text, **summarizer_params)

        except Exception, e:
            return json.dumps({'error': str(e)}, ensure_ascii=False, indent=2)
        else:
            res = json.dumps(
                tools.tree_encode({
                    'summary': summary, 'debug_info': debug_info
                }),
                ensure_ascii=False, indent=2
            )
            return res