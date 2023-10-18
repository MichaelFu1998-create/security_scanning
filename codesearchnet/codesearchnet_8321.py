def constructTx(self):
        """ Construct the actual transaction and store it in the class's dict
            store
        """
        ops = list()
        for op in self.ops:
            if isinstance(op, ProposalBuilder):
                # This operation is a proposal an needs to be deal with
                # differently
                proposal = op.get_raw()
                if proposal:
                    ops.append(proposal)
            elif isinstance(op, self.operation_class):
                ops.extend([op])
            else:
                # otherwise, we simply wrap ops into Operations
                ops.extend([self.operation_class(op)])

        # We now wrap everything into an actual transaction
        ops = self.add_required_fees(ops, asset_id=self.fee_asset_id)
        expiration = formatTimeFromNow(
            self.expiration
            or self.blockchain.expiration
            or 30  # defaults to 30 seconds
        )
        ref_block_num, ref_block_prefix = self.get_block_params()
        self.tx = self.signed_transaction_class(
            ref_block_num=ref_block_num,
            ref_block_prefix=ref_block_prefix,
            expiration=expiration,
            operations=ops,
        )
        dict.update(self, self.tx.json())
        self._unset_require_reconstruction()