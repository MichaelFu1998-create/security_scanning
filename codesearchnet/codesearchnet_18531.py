def excel_to_html(path, sheetname='Sheet1', css_classes='', \
    caption='', details=[], row_headers=False, merge=False):
    """
    Convert an excel spreadsheet to an html table.
    This function supports the conversion of merged 
    cells. It can be used in code or run from the 
    command-line. If passed the correct arguments
    it can generate fully accessible html.

    Args:
        path: string, path to the spreadsheet.

        sheetname: string, name of the sheet
        to convert. 

        css_classes: string, space separated
        classnames to append to the table.

        caption: string, a short heading-like 
        description of the table.

        details: list of strings, where the first
        item in the list is a string for the html 
        summary element and the second item is
        a string for the details element. The 
        summary should be very short, e.g. "Help",
        where as the details element should be a 
        long description regarding the purpose or 
        how to navigate the table.

        row_headers: boolean, defaults to False.
        Does the table have row headers? If set
        to True, the first element in each row
        will be a <th scope="row"> element 
        instead of a <td> element.
 
        merge: boolean, whether or not to 
        combine cells that were merged in the 
        spreadsheet.

    Returns:
        string, html table 
    """

    def get_data_on_merged_cells():
        """
        Build a datastructure with data 
        on merged cells.
        """
        # Use this to build support for merged columns and rows???? 
        merged_cells = xls.book.sheet_by_name(sheetname).merged_cells
        ds = {}
        for crange in merged_cells:
            rlo, rhi, clo, chi = crange
            for rowx in range(rlo, rhi):
                for colx in range(clo, chi):
                    # Cell (rlo, clo) (the top left one) will carry the data and 
                    # formatting info. The remainder will be recorded as blank cells, 
                    # but a renderer will apply the formatting info for the top left 
                    # cell (e.g. border, pattern) to all cells in the range.
                    #print(str(rlo) + ' ' + str(clo))
                    #print(str(rowx) + ' ' + str(colx))
                    parent_cell = (rlo,clo)
                    child_cell = (rowx,colx)
                    if not parent_cell in ds:
                        # Return data structure is a dictionary with numeric tuples 
                        # as keys. Each tuple holds the x, y coordinates of the cell.
                        # The dictionary holds two values:
                        # 1. A list with two numbers which represent the x/y count 
                        #    starting at 1 for the current cell.
                        # 2. A set describing which direction the cells are merged.
                        ds[parent_cell] = [[1,1], set([])]
                    else:
                        if parent_cell != child_cell and child_cell[0] == parent_cell[0]:
                            ds[parent_cell][0][0] += 1
                            ds[parent_cell][1].add('right')
                        elif parent_cell != child_cell and child_cell[0] > parent_cell[0]:
                            if child_cell[1] == parent_cell[1]:
                                ds[parent_cell][0][1] += 1
                            ds[parent_cell][1].add('down')
                        else:
                            raise RuntimeError('Something went wrong')
        return ds


    def mark_cells_going_right(cell, curr_cell, merged_cells):
        """
        Add a "colspan" attribute and mark empty table 
        columns for deletion if they are part of a 
        merged cell going right.

        Args:
            cell: BeautifulSoup element tag object 
            representation of the current cell.

            curr_cell: tuple, numeric representation 
            of the current cell.

            merged_cells: dictionary of of data about 
            merged cells.
        """
        #if curr_cell in merged_cells and merged_cells[curr_cell][1] == set(['right']):
        try:
            xcount = merged_cells[curr_cell][0][0]
            if xcount > 1: # No colspans on 1
                cell['colspan'] = xcount
            col_count = xcount - 1 
            while col_count > 0:
                cell = cell.find_next_sibling()
                cell['class'] = 'delete'
                col_count -= 1
        except:
            pass

    def mark_cells_going_down(cell, curr_cell, merged_cells):
        """
        Add a "rowspan" attribute and mark empty table 
        columns for deletion if they are part of a 
        merged cell going down.

        Args:
            cell: BeautifulSoup element tag object 
            representation of the current cell.

            curr_cell: tuple, numeric representation 
            of the current cell.

            merged_cells: dictionary of of data about 
            merged cells.
        """
        if curr_cell in merged_cells and merged_cells[curr_cell][1] == set(['down']):
            ycount = merged_cells[curr_cell][0][1]
            cell['rowspan'] = ycount
            row_count = ycount
            for child_row in cell.parent.find_next_siblings(limit=row_count - 1):
                i = 0
                for child in child_row.find_all('td'):
                    if i == curr_cell[1]:
                        child['class'] = 'delete'
                    i += 1

    def mark_cells_going_down_and_right(cell, curr_cell, merged_cells):
        """
        Add "rowspan" and "colspan" attributes and mark 
        empty columns for deletion if they are part of a 
        merged cell going down and to the right diagonally.

        Args:
            cell: BeautifulSoup element tag object 
            representation of the current cell.

            curr_cell: tuple, numeric representation 
            of the current cell.

            merged_cells: dictionary of of data about 
            merged cells.
        """
        if curr_cell in merged_cells and \
            ('down' in merged_cells[curr_cell][1] and \
             'right' in merged_cells[curr_cell][1]):
            xcount = merged_cells[curr_cell][0][0]
            ycount = merged_cells[curr_cell][0][1]
            row_count = ycount
            col_count = xcount
            mark_cells_going_right(cell, curr_cell, merged_cells)
    
            flag = False
            for child_row in [cell.parent] + cell.parent.find_all_next('tr', limit=row_count - 1):
                i = 0
                for child in child_row.find_all('td'):
                    if i == curr_cell[1]:
                        mark_cells_going_right(child, curr_cell, merged_cells)
                        if not flag:
                            child['colspan'] = col_count
                            child['rowspan'] = row_count
                            flag = True
                        else:
                            child['class'] = 'delete'
                    i += 1


    def is_empty_th(string):
        """
        Detects if a table cell is left
        empty (is a merged cell).

        Args:
            string: string
        """
        if string[:8] == 'Unnamed:':
            data = string.split(' ')
            if is_numeric(data[1]):
                return True
        return False


    def mark_header_cells(html):
        """
        Mark header cells for deletion if they 
        need to be merged. Also, add colspan
        and scope attributes.

        Args: 
            html: string
        """
        th = html.find_all('th')
        for header in th:
            txt = header.string
            if not is_empty_th(txt):
                header['scope'] = 'col'
                count = 1
                for sibling in header.find_next_siblings():
                    if is_empty_th(sibling.string):
                        count += 1
                        sibling['class'] = 'delete'
                    else:
                        break
                if count > 1:
                    header['colspan'] = count
                    header['scope'] = 'colgroup'


    def create_caption(html, caption):
        """
        Create a caption element for an 
        accessible table and append it
        to the right part of the tree.
    
        Args:
            html: string

            caption: string
        """
        ctag = html.new_tag('caption')
        ctag.insert(0, caption)
        html.table.insert(0, ctag)


    def create_summary_and_details(html, details):
        """
        Create a summary and details element
        for an accessible table and insert 
        it into the right part of the tree.

        Args:
            html: string

            details: string
        """
        if len(details) != 2:
            msg = 'The "details" argument should be a list with two items. ' \
                + 'The first item should be a string for the html summary ' \
                + 'and the second should be a long description for the details ' \
                + 'element. Both of those must be included and nothing else.'
            raise RuntimeError(msg)

        summary = details[0]
        details = details[1]

        if not caption:
            create_caption(html, caption)

        dtag = html.new_tag('details')
        stag = html.new_tag('summary')
        ptag = html.new_tag('p')
        stag.insert(0, summary)
        ptag.insert(0, details)
        dtag.insert(0, stag)
        dtag.append(ptag) 
        html.table.caption.insert(1, dtag)   


    def format_properly(html):
        """
        Fix bad formatting from beautifulsoup.

        Args:
            html: string of html representing 
            a table.
        """
        return html.replace('\n    ', '').replace('\n   </td>', \
            '</td>').replace('\n   </th>', '</th>').replace('\n   </summary>', \
            '</summary>').replace('\n   </p>', '</p>')


    def add_row_headers(html):
        """
        Convert <td>s to <th>s if row_headers
        is set to True.

        Args:
            html: string, table.
        """
        for row in html.tbody.find_all('tr'):
            spans_rows = 'rowspan' in row.td.attrs
            spans_columns = 'colspan' in row.td.attrs
            new_tag = html.new_tag('th')
            new_tag['scope'] = 'row'
            new_tag.string = row.td.string
            if spans_rows:
                new_tag['rowspan'] = row.td.attrs['rowspan']
                new_tag['scope'] = 'rowgroup'
            if spans_columns:
                new_tag['colspan'] = row.td.attrs['colspan']
            row.td.replace_with(new_tag)


    def beautify(html):
        """
        Beautify the html from pandas.

        Args:
            html: table markup from pandas.
        """
        table = html.find('table')
        first_tr = table.find('tr')
        del table['border']
        del first_tr['style']

        return format_properly(html.prettify(formatter='minimal'))


    def parse_html(html, caption, details):
        """
        Use BeautifulSoup to correct the 
        html for merged columns and rows.
        What could possibly go wrong?

        Args:
            html: string

            caption: string

            details: list of strings lenght of two

        Returns:
            string, modified html
        """
        new_html = BeautifulSoup(html, 'html.parser')
        if merge:
            row_num = 1
            # e.g. {(4, 3): [1, 'right'], (2, 1): [1, 'down']}
            merged_cells = get_data_on_merged_cells()
            rows = new_html.find('table').find('tbody').find_all('tr')
            for row in rows:
                cell_num = 0 # Why are we off by 1? Maybe because we set index to False in to_html?
                cells = row.find_all('td')
                for cell in cells:
                    #cell['class'] = str(row_num) + ' ' + str(cell_num) # DEBUG
                    curr_cell = (row_num, cell_num)

                    # Mark merged cells for deletion
                    mark_cells_going_right(cell, curr_cell, merged_cells)  
                    mark_cells_going_down(cell, curr_cell, merged_cells)
                    mark_cells_going_down_and_right(cell, curr_cell, merged_cells)
     
                    cell_num += 1
                row_num += 1

            # Mark header cells for deletion
            mark_header_cells(new_html)

            # Delete all the renegade cells at once
            destroy = new_html.find_all(attrs={'class' : 'delete' })
            for item in destroy:
                item.extract()

        # Convert <td>s to <th>s if needed.
        if row_headers:
            add_row_headers(new_html)

        # Add caption if applicable
        if caption:
            create_caption(new_html, caption)

        # Add summary and details if possible
        if details:
            create_summary_and_details(new_html, details)
        
        return beautify(new_html)

    # Set options for pandas and load the excel file
    pd.options.display.max_colwidth = -1
    xls = pd.ExcelFile(path)

    # Parse the sheet you're interested in, results in a Dataframe
    df = xls.parse(sheetname)

    # Convert the dataframe to html
    panda_html = df.to_html(classes=css_classes, index=False, na_rep='')
  
    # Parse the panda html to merge cells and beautify the markup 
    return parse_html(panda_html, caption, details)