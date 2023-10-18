def get_queryset(self):
        """
        Returns a queryset of models for the month requested
        """
        qs = super(BaseCalendarMonthView, self).get_queryset()

        year = self.get_year()
        month = self.get_month()

        date_field = self.get_date_field()
        end_date_field = self.get_end_date_field()

        date = _date_from_string(year, self.get_year_format(),
                                 month, self.get_month_format())

        since = date
        until = self.get_next_month(date)

        # Adjust our start and end dates to allow for next and previous
        # month edges
        if since.weekday() != self.get_first_of_week():
            diff = math.fabs(since.weekday() - self.get_first_of_week())
            since = since - datetime.timedelta(days=diff)

        if until.weekday() != ((self.get_first_of_week() + 6) % 7):
            diff = math.fabs(((self.get_first_of_week() + 6) % 7) - until.weekday())
            until = until + datetime.timedelta(days=diff)

        if end_date_field:
            # 5 possible conditions for showing an event:

            # 1) Single day event, starts after 'since'
            # 2) Multi-day event, starts after 'since' and ends before 'until'
            # 3) Starts before 'since' and ends after 'since' and before 'until'
            # 4) Starts after 'since' but before 'until' and ends after 'until'
            # 5) Starts before 'since' and ends after 'until'
            predicate1 = Q(**{
                '%s__gte' % date_field: since,
                end_date_field: None
            })
            predicate2 = Q(**{
                '%s__gte' % date_field: since,
                '%s__lt' % end_date_field: until
            })
            predicate3 = Q(**{
                '%s__lt' % date_field: since,
                '%s__gte' % end_date_field: since,
                '%s__lt' % end_date_field: until
            })
            predicate4 = Q(**{
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
                '%s__gte' % end_date_field: until
            })
            predicate5 = Q(**{
                '%s__lt' % date_field: since,
                '%s__gte' % end_date_field: until
            })
            return qs.filter(predicate1 | predicate2 | predicate3 | predicate4 | predicate5)
        return qs.filter(**{
            '%s__gte' % date_field: since
        })