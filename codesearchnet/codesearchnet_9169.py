def get_context_data(self, **kwargs):
        """
        Injects variables necessary for rendering the calendar into the context.

        Variables added are: `calendar`, `weekdays`, `month`, `next_month` and `previous_month`.
        """
        data = super(BaseCalendarMonthView, self).get_context_data(**kwargs)

        year = self.get_year()
        month = self.get_month()

        date = _date_from_string(year, self.get_year_format(),
                                 month, self.get_month_format())

        cal = Calendar(self.get_first_of_week())

        month_calendar = []
        now = datetime.datetime.utcnow()

        date_lists = defaultdict(list)
        multidate_objs = []

        for obj in data['object_list']:
            obj_date = self.get_start_date(obj)
            end_date_field = self.get_end_date_field()

            if end_date_field:
                end_date = self.get_end_date(obj)
                if end_date and end_date != obj_date:
                    multidate_objs.append({
                        'obj': obj,
                        'range': [x for x in daterange(obj_date, end_date)]
                    })
                    continue  # We don't put multi-day events in date_lists
            date_lists[obj_date].append(obj)

        for week in cal.monthdatescalendar(date.year, date.month):
            week_range = set(daterange(week[0], week[6]))
            week_events = []

            for val in multidate_objs:
                intersect_length = len(week_range.intersection(val['range']))

                if intersect_length:
                    # Event happens during this week
                    slot = 1
                    width = intersect_length  # How many days is the event during this week?
                    nowrap_previous = True  # Does the event continue from the previous week?
                    nowrap_next = True  # Does the event continue to the next week?

                    if val['range'][0] >= week[0]:
                        slot = 1 + (val['range'][0] - week[0]).days
                    else:
                        nowrap_previous = False
                    if val['range'][-1] > week[6]:
                        nowrap_next = False

                    week_events.append({
                        'event': val['obj'],
                        'slot': slot,
                        'width': width,
                        'nowrap_previous': nowrap_previous,
                        'nowrap_next': nowrap_next,
                    })

            week_calendar = {
                'events': week_events,
                'date_list': [],
            }
            for day in week:
                week_calendar['date_list'].append({
                    'day': day,
                    'events': date_lists[day],
                    'today': day == now.date(),
                    'is_current_month': day.month == date.month,
                })
            month_calendar.append(week_calendar)

        data['calendar'] = month_calendar
        data['weekdays'] = [DAYS[x] for x in cal.iterweekdays()]
        data['month'] = date
        data['next_month'] = self.get_next_month(date)
        data['previous_month'] = self.get_previous_month(date)

        return data