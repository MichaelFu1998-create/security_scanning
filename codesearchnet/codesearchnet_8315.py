def get_raw(self):
        """ Returns an instance of base "Operations" for further processing
        """
        if not self.ops:
            return
        ops = [self.operations.Op_wrapper(op=o) for o in list(self.ops)]
        proposer = self.account_class(
            self.proposer, blockchain_instance=self.blockchain
        )
        data = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "fee_paying_account": proposer["id"],
            "expiration_time": formatTimeFromNow(self.proposal_expiration),
            "proposed_ops": [o.json() for o in ops],
            "extensions": [],
        }
        if self.proposal_review:
            data.update({"review_period_seconds": self.proposal_review})
        ops = self.operations.Proposal_create(**data)
        return self.operation_class(ops)