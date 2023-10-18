def transform_courserun_schedule(self, content_metadata_item):
        """
        Return the schedule of the courseun content item.
        """
        start = content_metadata_item.get('start') or UNIX_MIN_DATE_STRING
        end = content_metadata_item.get('end') or UNIX_MAX_DATE_STRING
        return [{
            'startDate': parse_datetime_to_epoch_millis(start),
            'endDate': parse_datetime_to_epoch_millis(end),
            'active': current_time_is_in_interval(start, end)
        }]