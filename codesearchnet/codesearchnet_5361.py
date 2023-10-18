def get_event_definition(self):
        """
        Parse the event definition node, and return an instance of Event
        """
        messageEventDefinition = first(
            self.xpath('.//bpmn:messageEventDefinition'))
        if messageEventDefinition is not None:
            return self.get_message_event_definition(messageEventDefinition)

        timerEventDefinition = first(
            self.xpath('.//bpmn:timerEventDefinition'))
        if timerEventDefinition is not None:
            return self.get_timer_event_definition(timerEventDefinition)

        raise NotImplementedError(
            'Unsupported Intermediate Catch Event: %r', ET.tostring(self.node))