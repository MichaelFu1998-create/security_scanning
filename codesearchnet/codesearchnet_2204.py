def tf_update_batch(self, loss_per_instance):
        """
        Updates priority memory by performing the following steps:

        1. Use saved indices from prior retrieval to reconstruct the batch
        elements which will have their priorities updated.
        2. Compute priorities for these elements.
        3. Insert buffer elements to memory, potentially overwriting existing elements.
        4. Update priorities of existing memory elements
        5. Resort memory.
        6. Update buffer insertion index.

        Note that this implementation could be made more efficient by maintaining
        a sorted version via sum trees.

        :param loss_per_instance: Losses from recent batch to perform priority update
        """
        # 1. We reconstruct the batch from the buffer and the priority memory via
        # the TensorFlow variables holding the respective indices.
        mask = tf.not_equal(
            x=self.batch_indices,
            y=tf.zeros(shape=tf.shape(input=self.batch_indices), dtype=tf.int32)
        )
        priority_indices = tf.reshape(tensor=tf.where(condition=mask), shape=[-1])

        # These are elements from the buffer which first need to be inserted into the main memory.
        sampled_buffer_batch = self.tf_retrieve_indices(
            buffer_elements=self.last_batch_buffer_elems,
            priority_indices=priority_indices
        )

        # Extract batch elements.
        states = sampled_buffer_batch['states']
        internals = sampled_buffer_batch['internals']
        actions = sampled_buffer_batch['actions']
        terminal = sampled_buffer_batch['terminal']
        reward = sampled_buffer_batch['reward']

        # 2. Compute priorities for all batch elements.
        priorities = loss_per_instance ** self.prioritization_weight
        assignments = list()

        # 3. Insert the buffer elements from the recent batch into memory,
        # overwrite memory if full.
        memory_end_index = self.memory_index + self.last_batch_buffer_elems
        memory_insert_indices = tf.range(
            start=self.memory_index,
            limit=memory_end_index
        ) % self.capacity

        for name in sorted(states):
            assignments.append(tf.scatter_update(
                ref=self.states_memory[name],
                indices=memory_insert_indices,
                # Only buffer elements from batch.
                updates=states[name][0:self.last_batch_buffer_elems])
            )
        for name in sorted(internals):
            assignments.append(tf.scatter_update(
                ref=self.internals_buffer[name],
                indices=memory_insert_indices,
                updates=internals[name][0:self.last_batch_buffer_elems]
            ))
        assignments.append(tf.scatter_update(
            ref=self.priorities,
            indices=memory_insert_indices,
            updates=priorities[0:self.last_batch_buffer_elems]
        ))
        assignments.append(tf.scatter_update(
            ref=self.terminal_memory,
            indices=memory_insert_indices,
            updates=terminal[0:self.last_batch_buffer_elems])
        )
        assignments.append(tf.scatter_update(
            ref=self.reward_memory,
            indices=memory_insert_indices,
            updates=reward[0:self.last_batch_buffer_elems])
        )
        for name in sorted(actions):
            assignments.append(tf.scatter_update(
                ref=self.actions_memory[name],
                indices=memory_insert_indices,
                updates=actions[name][0:self.last_batch_buffer_elems]
            ))

        # 4.Update the priorities of the elements already in the memory.
        # Slice out remaining elements - [] if all batch elements were from buffer.
        main_memory_priorities = priorities[self.last_batch_buffer_elems:]
        # Note that priority indices can have a different shape because multiple
        # samples can be from the same index.
        main_memory_priorities = main_memory_priorities[0:tf.shape(priority_indices)[0]]
        assignments.append(tf.scatter_update(
            ref=self.priorities,
            indices=priority_indices,
            updates=main_memory_priorities
        ))

        with tf.control_dependencies(control_inputs=assignments):
            # 5. Re-sort memory according to priorities.
            assignments = list()

            # Obtain sorted order and indices.
            sorted_priorities, sorted_indices = tf.nn.top_k(
                input=self.priorities,
                k=self.capacity,
                sorted=True
            )
            # Re-assign elements according to priorities.
            # Priorities was the tensor we used to sort, so this can be directly assigned.
            assignments.append(tf.assign(ref=self.priorities, value=sorted_priorities))

            # All other memory variables are assigned via scatter updates using the indices
            # returned by the sort:
            assignments.append(tf.scatter_update(
                ref=self.terminal_memory,
                indices=sorted_indices,
                updates=self.terminal_memory
            ))
            for name in sorted(self.states_memory):
                assignments.append(tf.scatter_update(
                    ref=self.states_memory[name],
                    indices=sorted_indices,
                    updates=self.states_memory[name]
                ))
            for name in sorted(self.actions_memory):
                assignments.append(tf.scatter_update(
                    ref=self.actions_memory[name],
                    indices=sorted_indices,
                    updates=self.actions_memory[name]
                ))
            for name in sorted(self.internals_memory):
                assignments.append(tf.scatter_update(
                    ref=self.internals_memory[name],
                    indices=sorted_indices,
                    updates=self.internals_memory[name]
                ))
            assignments.append(tf.scatter_update(
                ref=self.reward_memory,
                indices=sorted_indices,
                updates=self.reward_memory
            ))

        # 6. Reset buffer index and increment memory index by inserted elements.
        with tf.control_dependencies(control_inputs=assignments):
            assignments = list()
            # Decrement pointer of last elements used.
            assignments.append(tf.assign_sub(ref=self.buffer_index, value=self.last_batch_buffer_elems))

            # Keep track of memory size as to know whether we can sample from the main memory.
            # Since the memory pointer can set to 0, we want to know if we are at capacity.
            total_inserted_elements = self.memory_size + self.last_batch_buffer_elems
            assignments.append(tf.assign(
                ref=self.memory_size,
                value=tf.minimum(x=total_inserted_elements, y=self.capacity))
            )

            # Update memory insertion index.
            assignments.append(tf.assign(ref=self.memory_index, value=memory_end_index))

            # Reset batch indices.
            assignments.append(tf.assign(
                ref=self.batch_indices,
                value=tf.zeros(shape=tf.shape(self.batch_indices), dtype=tf.int32)
            ))

        with tf.control_dependencies(control_inputs=assignments):
            return tf.no_op()