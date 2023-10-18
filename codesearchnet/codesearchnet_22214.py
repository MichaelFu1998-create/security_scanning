def delete_past_events(self):
        """
        Removes old events. This is provided largely as a convenience for maintenance
        purposes (daily_cleanup). if an Event has passed by more than X days
        as defined by Lapsed and has no related special events it will be deleted
        to free up the event name and remove clutter.
        For best results, set this up to run regularly as a cron job.
        """
        lapsed = datetime.datetime.now() - datetime.timedelta(days=90)
        for event in self.filter(start_date__lte=lapsed, featured=0, recap=''):
            event.delete()