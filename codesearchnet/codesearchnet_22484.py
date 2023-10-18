def votes(address):
        """Returns a list of namedtuples all votes made by an address, {(+/-)pubkeydelegate:timestamp}, timestamp DESC"""
        qry = DbCursor().execute_and_fetchall("""
           SELECT votes."votes", transactions."timestamp"
           FROM votes, transactions
           WHERE transactions."id" = votes."transactionId"
           AND transactions."senderId" = '{}'
           ORDER BY transactions."timestamp" DESC
        """.format(address))

        Vote = namedtuple(
            'vote',
            'direction delegate timestamp')
        res = []
        for i in qry:
            if i[0][0] == '+':
                direction = True
            elif i[0][0] == '-':
                direction = False
            else:
                logger.fatal('failed to interpret direction for: {}'.format(i))
                raise ParseError('failed to interpret direction of vote for: {}'.format(i))
            vote = Vote(
                direction=direction,
                delegate=i[0][1:],
                timestamp=i[1],
            )
            res.append(vote)
        return res