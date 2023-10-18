def getEncodedValues(self, input):
    """ See method description in base.py """

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return numpy.array([None])

    assert isinstance(input, datetime.datetime)
    values = []

    # -------------------------------------------------------------------------
    # Get the scalar values for each sub-field
    timetuple = input.timetuple()
    timeOfDay = timetuple.tm_hour + float(timetuple.tm_min)/60.0

    if self.seasonEncoder is not None:
      dayOfYear = timetuple.tm_yday
      # input.timetuple() computes the day of year 1 based, so convert to 0 based
      values.append(dayOfYear-1)

    if self.dayOfWeekEncoder is not None:
      dayOfWeek = timetuple.tm_wday + timeOfDay / 24.0
      values.append(dayOfWeek)

    if self.weekendEncoder is not None:
      # saturday, sunday or friday evening
      if timetuple.tm_wday == 6 or timetuple.tm_wday == 5 \
          or (timetuple.tm_wday == 4 and timeOfDay > 18):
        weekend = 1
      else:
        weekend = 0
      values.append(weekend)

    if self.customDaysEncoder is not None:
      if timetuple.tm_wday in self.customDays:
        customDay = 1
      else:
        customDay = 0
      values.append(customDay)
    if self.holidayEncoder is not None:
      # A "continuous" binary value. = 1 on the holiday itself and smooth ramp
      #  0->1 on the day before the holiday and 1->0 on the day after the holiday.
      # Currently the only holiday we know about is December 25
      # holidays is a list of holidays that occur on a fixed date every year
      if len(self.holidays) == 0:
        holidays = [(12, 25)]
      else:
        holidays = self.holidays
      val = 0
      for h in holidays:
        # hdate is midnight on the holiday
        if len(h) == 3:
          hdate = datetime.datetime(h[0], h[1], h[2], 0, 0, 0)
        else:
          hdate = datetime.datetime(timetuple.tm_year, h[0], h[1], 0, 0, 0)
        if input > hdate:
          diff = input - hdate
          if diff.days == 0:
            # return 1 on the holiday itself
            val = 1
            break
          elif diff.days == 1:
            # ramp smoothly from 1 -> 0 on the next day
            val = 1.0 - (float(diff.seconds) / 86400)
            break
        else:
          diff = hdate - input
          if diff.days == 0:
            # ramp smoothly from 0 -> 1 on the previous day
            val = 1.0 - (float(diff.seconds) / 86400)

      values.append(val)

    if self.timeOfDayEncoder is not None:
      values.append(timeOfDay)

    return values