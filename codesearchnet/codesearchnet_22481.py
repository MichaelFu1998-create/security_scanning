def get_transactionlist(delegate_pubkey):
    """returns a list of named tuples of all transactions relevant to a specific delegates voters.
    Flow: finds all voters and unvoters, SELECTs all transactions of those voters, names all transactions according to
    the scheme: 'transaction', 'id amount timestamp recipientId senderId rawasset type fee blockId'"""

    res = DbCursor().execute_and_fetchall("""
        SELECT transactions."id", transactions."amount",
               blocks."timestamp", transactions."recipientId",
               transactions."senderId", transactions."rawasset",
               transactions."type", transactions."fee", transactions."blockId"
        FROM transactions 
        INNER JOIN blocks
          ON transactions."blockId" = blocks.id
        WHERE transactions."senderId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{0}')
        OR transactions."recipientId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{0}')
        ORDER BY blocks."timestamp" ASC;""".format(delegate_pubkey))

    Transaction = namedtuple(
        'transaction',
        'id amount timestamp recipientId senderId rawasset type fee')
    named_transactions = []

    for i in res:
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