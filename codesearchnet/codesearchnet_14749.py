def get_resources(cls):
        """Returns Ext Resources."""
        plugin = directory.get_plugin()
        controller = SegmentAllocationRangesController(plugin)
        return [extensions.ResourceExtension(
            Segment_allocation_ranges.get_alias(),
            controller)]