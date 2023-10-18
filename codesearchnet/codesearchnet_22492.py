def dep_trueshare(start_block=0, del_pubkey=None, del_address=None, blacklist=None, share_fees=False, max_weight=float('inf'), raiseError=True):
        '''
        Legacy TBW script (still pretty performant, but has some quirky behavior when forging delegates are amongst
        your voters)

        :param int start_block: block from which we start adding to the share (we calculate balances from block 0 anyways)
        :param str del_pubkey: delegate public key as is presented in the ark wallet
        :param str del_address: delegate address
        :param list blacklist: blacklist for addresses to be removed BEFORE calculation. Their share is removed from the pool balance
        :param bool share_fees: if tx fees should be shared as well.
        :param float max_weight: max_balance of a voter


        '''

        delegate_pubkey = c.DELEGATE['PUBKEY']
        delegate_address = c.DELEGATE['ADDRESS']

        if del_pubkey and del_address:
            delegate_address = del_address
            delegate_pubkey = del_pubkey

        max_timestamp = Node.max_timestamp()

        # utils function
        transactions = get_transactionlist(
            delegate_pubkey=delegate_pubkey
        )

        votes = Delegate.votes(delegate_pubkey)

        # create a map of voters
        voter_dict = {}
        for voter in votes:
            voter_dict.update({voter.address: {
                'balance': 0.0,
                'status': False,
                'last_payout': voter.timestamp,
                'share': 0.0,
                'vote_timestamp': voter.timestamp,
                'blocks_forged': []}
            })

        try:
            for i in blacklist:
                voter_dict.pop(i)
        except Exception:
            pass

        # check if a voter is/used to be a forging delegate
        delegates = Delegate.delegates()
        for i in delegates:
            if i.address in voter_dict:
                try:
                    blocks_by_voter = Delegate.blocks(i.pubkey)
                    voter_dict[i.address]['blocks_forged'].extend(Delegate.blocks(i.pubkey))
                except Exception:
                    pass

        last_payout = Delegate.lastpayout(delegate_address)
        for payout in last_payout:
            try:
                voter_dict[payout.address]['last_payout'] = payout.timestamp
            except Exception:
                pass

        blocks = Delegate.blocks(delegate_pubkey)
        block_nr = start_block
        chunk_dict = {}
        reuse = False
        try:
            for tx in transactions:
                while tx.timestamp > blocks[block_nr].timestamp:
                    if reuse:
                        block_nr += 1
                        for x in chunk_dict:
                            voter_dict[x]['share'] += chunk_dict[x]
                        continue

                    block_nr += 1
                    poolbalance = 0
                    chunk_dict = {}
                    for i in voter_dict:
                        balance = voter_dict[i]['balance']
                        if balance > max_weight:
                            balance = max_weight

                        #checks if a delegate that votes for us is has forged blocks in the mean time
                        try:
                            for x in voter_dict[i]['blocks_forged']:
                                if x.timestamp < blocks[block_nr].timestamp:
                                    voter_dict[i]['balance'] += (x.reward + x.totalFee)
                                    voter_dict[i]['blocks_forged'].remove(x)
                            balance = voter_dict[i]['balance']
                        except Exception:
                            pass

                        if voter_dict[i]['status']:
                            if not voter_dict[i]['balance'] < -20 * c.ARK:
                                poolbalance += balance
                            else:
                                if raiseError:
                                    raise NegativeBalanceError('balance lower than zero for: {0}'.format(i))
                                pass

                    for i in voter_dict:
                        balance = voter_dict[i]['balance']

                        if voter_dict[i]['status'] and voter_dict[i]['last_payout'] < blocks[block_nr].timestamp:
                            if share_fees:
                                share = (balance / poolbalance) * (blocks[block_nr].reward +
                                                                   blocks[block_nr].totalFee)
                            else:
                                share = (balance / poolbalance) * blocks[block_nr].reward
                            voter_dict[i]['share'] += share
                            chunk_dict.update({i: share})
                    reuse = True

                # parsing a transaction
                minvote = '{{"votes":["-{0}"]}}'.format(delegate_pubkey)
                plusvote = '{{"votes":["+{0}"]}}'.format(delegate_pubkey)

                reuse = False

                if tx.recipientId in voter_dict:
                    voter_dict[tx.recipientId]['balance'] += tx.amount
                if tx.senderId in voter_dict:
                    voter_dict[tx.senderId]['balance'] -= (tx.amount + tx.fee)
                if tx.senderId in voter_dict and tx.type == 3 and plusvote in tx.rawasset:
                    voter_dict[tx.senderId]['status'] = True
                if tx.senderId in voter_dict and tx.type == 3 and minvote in tx.rawasset:
                    voter_dict[tx.senderId]['status'] = False

            remaining_blocks = len(blocks) - block_nr - 1
            for i in range(remaining_blocks):
                for x in chunk_dict:
                    voter_dict[x]['share'] += chunk_dict[x]
        except IndexError:
            pass

        for i in voter_dict:
            logger.info("{0}  {1}  {2}  {3}  {4}".format(
                i,
                voter_dict[i]['share'],
                voter_dict[i]['status'],
                voter_dict[i]['last_payout'],
                voter_dict[i]['vote_timestamp']))
        return voter_dict, max_timestamp