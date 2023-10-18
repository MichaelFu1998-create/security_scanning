def generate_chart(self, properties):
        """
        Function:
            Generate and save chart to specific sheet.
        Input:
            sheet: If already exists, new chart will be added below.
                   Otherwise, it would create a new sheet;
            x_axis: Specify x axis;
            y_axis: Specify y axis;
            series: Specify series;
            filters: dict type, use to filter useful data from original data;
            title: if None, the chart will create without title;
            x_axis_name: if None, use x_axis instead;
            y_axis_name: if None, use y_axis instead;
        """
        # check input parameters
        if not {'x_axis', 'y_axis', 'series', 'filters'}.issubset(set(properties.keys())):
            raise RuntimeError("Error properties: %s" % properties.keys())

        # generate chart
        mask = self.__filter_data(properties['filters'])
        chart = self.__generate_chart(mask, properties)
        sheet = properties['sheet']

        # Add work sheet
        if sheet in self.sheet_dict.keys():
            self.sheet_dict[sheet] += 1
            worksheet = self.workbook.get_worksheet_by_name(sheet)
        else:
            self.sheet_dict[sheet] = 1
            worksheet = self.workbook.add_worksheet(sheet)
        worksheet.insert_chart('B%d' % (5 + (self.sheet_dict[sheet] - 1) * 35), chart)