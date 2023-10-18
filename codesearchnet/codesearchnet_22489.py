def votes(delegate_pubkey):
        """returns every address that has voted for a delegate.
        Current voters can be obtained using voters. ORDER BY timestamp ASC"""
        qry = DbCursor().execute_and_fetchall("""
                 SELECT transactions."recipientId", transactions."timestamp"
                 FROM transactions, votes
                 WHERE transactions."id" = votes."transactionId"
                 AND votes."votes" = '+{}'
                 ORDER BY transactions."timestamp" ASC;
        """.format(delegate_pubkey))

        Voter = namedtuple(
            'voter',
            'address timestamp')
        voters = []
        for i in qry:
            voter = Voter(
                address=i[0],
                timestamp=i[1]
                          )
            voters.append(voter)
        return voters