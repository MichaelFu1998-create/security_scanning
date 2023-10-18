def get_events(delegate_pubkey):
    """returns a list of named tuples of all transactions relevant to a specific delegates voters.
    Flow: finds all voters and unvoters, SELECTs all transactions of those voters, names all transactions according to
    the scheme: 'transaction', 'id amount timestamp recipientId senderId rawasset type fee blockId'"""

    res = DbCursor().execute_and_fetchall("""
    SELECT *
      FROM(
        SELECT transactions."id",
               transactions."amount",
               transactions."fee",
               blocks."timestamp",
               transactions."recipientId",
               transactions."senderId",
               transactions."type",
               transactions."rawasset"
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
        UNION
        SELECT blocks."id",
               blocks."reward",
               blocks."totalFee",
               blocks."timestamp",
               mem_accounts."address",
               NULL,
               100,
               blocks."rawtxs"
        FROM blocks
        INNER JOIN mem_accounts
          ON mem_accounts."publicKey" = blocks."generatorPublicKey"
        WHERE mem_accounts."address" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{0}')) AS events
        ORDER BY events."timestamp";""".format(delegate_pubkey))

    Event = namedtuple(
        'Event',
        'id amount fee timestamp recipientId senderId type raw')
    named_events = []

    for i in res:
        tx_id = Event(
            id=i[0],
            amount=i[1],
            fee=i[2],
            timestamp=i[3],
            recipientId=i[4],
            senderId=i[5],
            type=i[6],
            raw=i[7]
        )
        named_events.append(tx_id)
    return named_events