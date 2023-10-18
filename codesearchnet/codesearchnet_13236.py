def to_html(self, max_rows=None):
        '''Render this annotation list in HTML

        Returns
        -------
        rendered : str
            An HTML table containing this annotation's data.
        '''
        n = len(self.data)

        div_id = _get_divid(self)

        out = r'''  <div class="panel panel-default">
                        <div class="panel-heading" role="tab" id="heading-{0}">
                            <button
                                type="button"
                                data-toggle="collapse"
                                data-parent="#accordion"
                                href="#{0}"
                                aria-expanded="false"
                                class="collapsed btn btn-info btn-block"
                                aria-controls="{0}">
                                {1:s}
                                <span class="badge pull-right">{2:d}</span>
                            </button>
                        </div>'''.format(div_id, self.namespace, n)

        out += r'''     <div id="{0}" class="panel-collapse collapse"
                             role="tabpanel" aria-labelledby="heading-{0}">
                            <div class="panel-body">'''.format(div_id)

        out += r'''<div class="pull-right">
                        {}
                    </div>'''.format(self.annotation_metadata._repr_html_())
        out += r'''<div class="pull-right clearfix">
                        {}
                    </div>'''.format(self.sandbox._repr_html_())

        # -- Annotation content starts here
        out += r'''<div><table border="1" class="dataframe">
                    <thead>
                        <tr style="text-align: right;">
                            <th></th>
                            <th>time</th>
                            <th>duration</th>
                            <th>value</th>
                            <th>confidence</th>
                        </tr>
                    </thead>'''.format(self.namespace, n)

        out += r'''<tbody>'''

        if max_rows is None or n <= max_rows:
            out += self._fmt_rows(0, n)
        else:
            out += self._fmt_rows(0, max_rows//2)
            out += r'''<tr>
                            <th>...</th>
                            <td>...</td>
                            <td>...</td>
                            <td>...</td>
                            <td>...</td>
                        </tr>'''
            out += self._fmt_rows(n-max_rows//2, n)

        out += r'''</tbody>'''

        out += r'''</table></div>'''

        out += r'''</div></div></div>'''
        return out