def payout(address):
        """returns all received transactions between the address and registered delegate accounts
        ORDER by timestamp ASC."""
        qry = DbCursor().execute_and_fetchall("""
                SELECT DISTINCT transactions."id", transactions."amount",
                       transactions."timestamp", transactions."recipientId",
                       transactions."senderId", transactions."rawasset",
                       transactions."type", transactions."fee"
                FROM transactions, delegates
                WHERE transactions."senderId" IN (
                  SELECT transactions."senderId" 
                  FROM transactions, delegates 
                  WHERE transactions."id" = delegates."transactionId"
                )
                AND transactions."recipientId" = '{}'
                ORDER BY transactions."timestamp" ASC""".format(address))

        Transaction = namedtuple(
            'transaction',
            'id amount timestamp recipientId senderId rawasset type fee')
        named_transactions = []

        for i in qry:
            tx_id = Transaction(
                id=i[0],
                amount=i[1],
                timestamp=i[2],
                recipientId=i[3],
                senderId=i[4],
                rawasset=i[5],
                type=i[6],
                fee=i[7],
            )

            named_transactions.append(tx_id)
        return named_transactions