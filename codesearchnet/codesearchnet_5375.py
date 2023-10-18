def parse_node(self):
        """
        Parse this node, and all children, returning the connected task spec.
        """

        try:
            self.task = self.create_task()

            self.task.documentation = self.parser._parse_documentation(
                self.node, xpath=self.xpath, task_parser=self)

            boundary_event_nodes = self.process_xpath(
                './/bpmn:boundaryEvent[@attachedToRef="%s"]' % self.get_id())
            if boundary_event_nodes:
                parent_task = _BoundaryEventParent(
                    self.spec, '%s.BoundaryEventParent' % self.get_id(),
                    self.task, lane=self.task.lane)
                self.process_parser.parsed_nodes[
                    self.node.get('id')] = parent_task

                parent_task.connect_outgoing(
                    self.task, '%s.FromBoundaryEventParent' % self.get_id(),
                    None, None)
                for boundary_event in boundary_event_nodes:
                    b = self.process_parser.parse_node(boundary_event)
                    parent_task.connect_outgoing(
                        b,
                        '%s.FromBoundaryEventParent' % boundary_event.get(
                            'id'),
                        None, None)
            else:
                self.process_parser.parsed_nodes[
                    self.node.get('id')] = self.task

            children = []
            outgoing = self.process_xpath(
                './/bpmn:sequenceFlow[@sourceRef="%s"]' % self.get_id())
            if len(outgoing) > 1 and not self.handles_multiple_outgoing():
                raise ValidationException(
                    'Multiple outgoing flows are not supported for '
                    'tasks of type',
                    node=self.node,
                    filename=self.process_parser.filename)
            for sequence_flow in outgoing:
                target_ref = sequence_flow.get('targetRef')
                target_node = one(
                    self.process_xpath('.//*[@id="%s"]' % target_ref))
                c = self.process_parser.parse_node(target_node)
                children.append((c, target_node, sequence_flow))

            if children:
                default_outgoing = self.node.get('default')
                if not default_outgoing:
                    (c, target_node, sequence_flow) = children[0]
                    default_outgoing = sequence_flow.get('id')

                for (c, target_node, sequence_flow) in children:
                    self.connect_outgoing(
                        c, target_node, sequence_flow,
                        sequence_flow.get('id') == default_outgoing)

            return parent_task if boundary_event_nodes else self.task
        except ValidationException:
            raise
        except Exception as ex:
            exc_info = sys.exc_info()
            tb = "".join(traceback.format_exception(
                exc_info[0], exc_info[1], exc_info[2]))
            LOG.error("%r\n%s", ex, tb)
            raise ValidationException(
                "%r" % (ex), node=self.node,
                filename=self.process_parser.filename)