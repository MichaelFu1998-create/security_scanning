def get_object(self, url, month_format='%b', day_format='%d'):
        """
        Parses the date from a url and uses it in the query.  For objects which
        are unique for date.
        """
        params = self.get_params(url)
        try:
            year = params[self._meta.year_part]
            month = params[self._meta.month_part]
            day = params[self._meta.day_part]
        except KeyError:
            try:
                # named lookups failed, so try to get the date using the first
                # three parameters
                year, month, day = params['_0'], params['_1'], params['_2']
            except KeyError:
                raise OEmbedException('Error extracting date from url parameters')
        
        try:
            tt = time.strptime('%s-%s-%s' % (year, month, day),
                               '%s-%s-%s' % ('%Y', month_format, day_format))
            date = datetime.date(*tt[:3])
        except ValueError:
            raise OEmbedException('Error parsing date from: %s' % url)

        # apply the date-specific lookups
        if isinstance(self._meta.model._meta.get_field(self._meta.date_field), DateTimeField):
            min_date = datetime.datetime.combine(date, datetime.time.min)
            max_date = datetime.datetime.combine(date, datetime.time.max)
            query = {'%s__range' % self._meta.date_field: (min_date, max_date)}
        else:
            query = {self._meta.date_field: date}
        
        # apply the regular search lookups
        for key, value in self._meta.fields_to_match.iteritems():
            try:
                query[value] = params[key]
            except KeyError:
                raise OEmbedException('%s was not found in the urlpattern parameters.  Valid names are: %s' % (key, ', '.join(params.keys())))
        
        try:
            obj = self.get_queryset().get(**query)
        except self._meta.model.DoesNotExist:
            raise OEmbedException('Requested object not found')
        
        return obj