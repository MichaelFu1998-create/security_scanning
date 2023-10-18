def get_timer_event_definition(self, timerEventDefinition):
        """
        Parse the timerEventDefinition node and return an instance of
        TimerEventDefinition

        This currently only supports the timeDate node for specifying an expiry
        time for the timer.
        """
        timeDate = first(self.xpath('.//bpmn:timeDate'))
        return TimerEventDefinition(
            self.node.get('name', timeDate.text),
            self.parser.parse_condition(
                timeDate.text, None, None, None, None, self))