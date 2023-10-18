def _try_allocate(self, context, segment_id, network_id):
        """Find a deallocated network segment id and reallocate it.

        NOTE(morgabra) This locks the segment table, but only the rows
        in use by the segment, which is pretty handy if we ever have
        more than 1 segment or segment type.
        """
        LOG.info("Attempting to allocate segment for network %s "
                 "segment_id %s segment_type %s"
                 % (network_id, segment_id, self.segment_type))

        filter_dict = {
            "segment_id": segment_id,
            "segment_type": self.segment_type,
            "do_not_use": False
        }
        available_ranges = db_api.segment_allocation_range_find(
            context, scope=db_api.ALL, **filter_dict)
        available_range_ids = [r["id"] for r in available_ranges]

        try:
            with context.session.begin(subtransactions=True):
                # Search for any deallocated segment ids for the
                # given segment.
                filter_dict = {
                    "deallocated": True,
                    "segment_id": segment_id,
                    "segment_type": self.segment_type,
                    "segment_allocation_range_ids": available_range_ids
                }

                # NOTE(morgabra) We select 100 deallocated segment ids from
                # the table here, and then choose 1 randomly. This is to help
                # alleviate the case where an uncaught exception might leave
                # an allocation active on a remote service but we do not have
                # a record of it locally. If we *do* end up choosing a
                # conflicted id, the caller should simply allocate another one
                # and mark them all as reserved. If a single object has
                # multiple reservations on the same segment, they will not be
                # deallocated, and the operator must resolve the conficts
                # manually.
                allocations = db_api.segment_allocation_find(
                    context, lock_mode=True, **filter_dict).limit(100).all()

                if allocations:
                    allocation = random.choice(allocations)

                    # Allocate the chosen segment.
                    update_dict = {
                        "deallocated": False,
                        "deallocated_at": None,
                        "network_id": network_id
                    }
                    allocation = db_api.segment_allocation_update(
                        context, allocation, **update_dict)
                    LOG.info("Allocated segment %s for network %s "
                             "segment_id %s segment_type %s"
                             % (allocation["id"], network_id, segment_id,
                                self.segment_type))
                    return allocation
        except Exception:
            LOG.exception("Error in segment reallocation.")

        LOG.info("Cannot find reallocatable segment for network %s "
                 "segment_id %s segment_type %s"
                 % (network_id, segment_id, self.segment_type))