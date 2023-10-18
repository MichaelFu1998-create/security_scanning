def build_metagraph_list(self):
        """
        Convert MetaParams into TF Summary Format and create summary_op.

        Returns:
            Merged TF Op for TEXT summary elements, should only be executed once to reduce data duplication.

        """
        ops = []

        self.ignore_unknown_dtypes = True
        for key in sorted(self.meta_params):
            value = self.convert_data_to_string(self.meta_params[key])

            if len(value) == 0:
                continue
            if isinstance(value, str):
                ops.append(tf.contrib.summary.generic(name=key, tensor=tf.convert_to_tensor(str(value))))
            else:
                ops.append(tf.contrib.summary.generic(name=key, tensor=tf.as_string(tf.convert_to_tensor(value))))

        return ops