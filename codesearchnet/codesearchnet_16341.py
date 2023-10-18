def cmp(self, other):
        """*Note: checks Range.start() only*
        Key: self = [], other = {}
            * [   {----]----} => -1
            * {---[---}  ] => 1
            * [---]  {---} => -1
            * [---] same as {---} => 0
            * [--{-}--] => -1
        """
        if isinstance(other, Range):
            # other has tz, I dont, so replace the tz
            start = self.start.replace(tzinfo=other.start.tz) if other.start.tz and self.start.tz is None else self.start
            end = self.end.replace(tzinfo=other.end.tz) if other.end.tz and self.end.tz is None else self.end

            if start == other.start and end == other.end:
                return 0 
            elif start < other.start:
                return -1
            else:
                return 1

        elif isinstance(other, Date):
            if other.tz and self.start.tz is None:
                return 0 if other == self.start.replace(tzinfo=other.tz) else -1 if other > self.start.replace(tzinfo=other.start.tz) else 1
            return 0 if other == self.start else -1 if other > self.start else 1
        else:
            return self.cmp(Range(other, tz=self.start.tz))