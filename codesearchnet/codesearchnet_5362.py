def get_message_event_definition(self, messageEventDefinition):
        """
        Parse the messageEventDefinition node and return an instance of
        MessageEventDefinition
        """
        messageRef = first(self.xpath('.//bpmn:messageRef'))
        message = messageRef.get(
            'name') if messageRef is not None else self.node.get('name')
        return MessageEventDefinition(message)