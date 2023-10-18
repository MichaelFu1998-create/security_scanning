def update_batch(self, loss_per_instance):
        """
        Computes priorities according to loss.

        Args:
            loss_per_instance:

        """
        if self.batch_indices is None:
            raise TensorForceError("Need to call get_batch before each update_batch call.")
        # if len(loss_per_instance) != len(self.batch_indices):
        #     raise TensorForceError("For all instances a loss value has to be provided.")

        for index, loss in zip(self.batch_indices, loss_per_instance):
            # Sampling priority is proportional to the largest absolute temporal difference error.
            new_priority = (np.abs(loss) + self.prioritization_constant) ** self.prioritization_weight
            self.observations._move(index, new_priority)
            self.none_priority_index += 1