def increment(cls, name):
        """Call this method to increment the named counter.  This is atomic on
        the database.

        :param name:
            Name for a previously created ``Counter`` object 
        """
        with transaction.atomic():
            counter = Counter.objects.select_for_update().get(name=name)
            counter.value += 1
            counter.save()

        return counter.value