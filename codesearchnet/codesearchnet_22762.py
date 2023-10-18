def get_events_vote_cluster(self, delegate_address):
        ''' Returns all transactions and forged blocks by voters clustered around a single delegate_address'''

        delegate_pubkey = self.account_details(address=delegate_address)['public_key']

        plusvote = '+{delegate_pubkey}'.format(delegate_pubkey=delegate_pubkey)

        resultset = self._cursor.execute_and_fetchall("""
            SELECT *
             FROM (
            SELECT 
            trs."{transactions[id]}" AS a,
            'transaction' AS b, 
            trs."{transactions[amount]}" AS c,
            trs."{transactions[timestamp]}" AS d, 
            trs."{transactions[recipient_id]}" AS e,
            trs."{transactions[sender_id]}" AS f, 
            trs."{transactions[rawasset]}" AS g,
            trs."{transactions[type]}" AS h, 
            trs."{transactions[fee]}" AS i, 
            trs."{transactions[block_id]}" AS j,
            blocks."{blocks[height]}" AS k
            FROM {transactions[table]} AS trs
            INNER JOIN {blocks[table]} AS blocks
                 ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")
            WHERE trs."{transactions[sender_id]}" IN
              (SELECT trs."{transactions[sender_id]}"
               FROM {transactions[table]} AS trs, {votes[table]} AS votes
               WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"
               AND votes."{votes[votes]}" = '{plusvote}') 
            OR trs."{transactions[recipient_id]}" IN
              (SELECT trs."{transactions[sender_id]}"
               FROM {transactions[table]} AS trs, {votes[table]} AS votes
               WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"
               AND votes."{votes[votes]}" = '{plusvote}') 
            UNION
            SELECT 
            blocks."{blocks[id]}" AS a, 
            'block' AS b, 
            blocks."{blocks[reward]}"as c, 
            blocks."{blocks[total_fee]}" AS d,
            ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, 'hex') AS e,
            mem."{mem_accounts[address]}" AS f,
            mem."{mem_accounts[username]}" AS g,
            NULL AS h,
            blocks."{blocks[timestamp]}" AS i,
            NULL AS j,
            blocks."{blocks[height]}" AS k
            FROM blocks
              INNER JOIN {mem_accounts[table]} AS mem
              ON (mem."{mem_accounts[public_key]}" = blocks."{blocks[generator_public_key]}")  
            WHERE
            blocks."{blocks[generator_public_key]}" IN (
                    SELECT mem2."{mem_accounts[public_key]}"
                    FROM {mem_accounts[table]} mem2
                    WHERE mem2."{mem_accounts[address]}" IN 
                    (SELECT trs."{transactions[sender_id]}"
                     FROM {transactions[table]} AS trs, {votes[table]} AS votes
                     WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"
                     AND votes."{votes[votes]}" = '{plusvote}') 
               )) total
               
            ORDER BY total.k ASC;""".format(
                address=delegate_address,
                transactions=self.scheme['transactions'],
                blocks=self.scheme['blocks'],
                mem_accounts=self.scheme['mem_accounts'],
                mem_accounts2delegates=self.scheme['mem_accounts2delegates'],
                votes=self.scheme['votes'],
                plusvote=plusvote))
        res = {}
        for i in resultset:

            if i[1] == 'transaction':
                res.update({i[0]: {
                   'tx_id': i[0],
                   'event_type': i[1],
                   'amount': i[2],
                   'timestamp': i[3],
                   'recipient_id': i[4],
                   'sender_id': i[5],
                   'rawasset': i[6],
                   'type': i[7],
                   'fee': i[8],
                   'block_id': i[9],
                   'height': i[10]
                }})

            elif i[1] == 'block':
                res.update({i[0]: {
                    'block_id': i[0],
                    'event_type': i[1],
                    'reward': i[2],
                    'total_fee': i[3],
                    'timestamp': i[8],
                    'address': i[5],
                    'username': i[6],
                    'public_key': i[4],
                    'height': i[10]
                }})

        return res