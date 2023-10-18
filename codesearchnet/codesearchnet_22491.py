def share(passphrase=None, last_payout=None, start_block=0, del_pubkey=None, del_address=None):
        """Calculate the true blockweight payout share for a given delegate,
        assuming no exceptions were made for a voter. last_payout is a map of addresses and timestamps:
        {address: timestamp}. If no argument are given, it will start the calculation at the first forged block
        by the delegate, generate a last_payout from transaction history, and use the set_delegate info.

        If a passphrase is provided, it is only used to generate the adddress and keys, no transactions are sent.
        (Still not recommended unless you know what you are doing, version control could store your passphrase for example;
        very risky)
        """
        logger.info('starting share calculation using settings: {0} {1}'.format(c.DELEGATE, c.CALCULATION_SETTINGS))


        delegate_pubkey = c.DELEGATE['PUBKEY']
        delegate_address = c.DELEGATE['ADDRESS']

        if del_pubkey and del_address:
            delegate_address = del_address
            delegate_pubkey = del_pubkey

        logger.info('Starting share calculation, using address:{0}, pubkey:{1}'.format(delegate_address, delegate_pubkey))

        max_timestamp = Node.max_timestamp()
        logger.info('Share calculation max_timestamp = {}'.format(max_timestamp))

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

        # check if a voter is/used to be a forging delegate
        delegates = Delegate.delegates()
        for i in delegates:
            if i.address in voter_dict:
                logger.info('A registered delegate is a voter: {0}, {1}, {2}'.format(i.username, i.address, i.pubkey))
                try:
                    blocks_by_voter = Delegate.blocks(i.pubkey)
                    voter_dict[i.address]['blocks_forged'].extend(Delegate.blocks(i.pubkey))
                    logger.info('delegate {0} has forged {1} blocks'.format(i.username, len(blocks_by_voter)))
                except Exception:
                    logger.info('delegate {} has not forged any blocks'.format(i))
                    pass
        try:
            for i in c.CALCULATION_SETTINGS['BLACKLIST']:
                voter_dict.pop(i)
                logger.debug('popped {} from calculations'.format(i))
        except Exception:
            pass

        if not last_payout:
            last_payout = Delegate.lastpayout(delegate_address)
            for payout in last_payout:
                try:
                    voter_dict[payout.address]['last_payout'] = payout.timestamp
                except Exception:
                    pass
        elif type(last_payout) is int:
            for address in voter_dict:
                if address['vote_timestamp'] < last_payout:
                    address['last_payout'] = last_payout
        elif type(last_payout) is dict:
            for payout in last_payout:
                try:
                    voter_dict[payout.address]['last_payout'] = payout.timestamp
                except Exception:
                    pass
        else:
            logger.fatal('last_payout object not recognised: {}'.format(type(last_payout)))
            raise InputError('last_payout object not recognised: {}'.format(type(last_payout)))

        # get all forged blocks of delegate:
        blocks = Delegate.blocks(max_timestamp=max_timestamp,
                                 delegate_pubkey=delegate_pubkey)

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

                        try:
                            if voter_dict[i]['balance'] > c.CALCULATION_SETTINGS['MAX']:
                                balance = c.CALCULATION_SETTINGS['MAX']
                        except Exception:
                            pass

                        try:
                            if balance > c.CALCULATION_SETTINGS['EXCEPTIONS'][i]['REPLACE']:
                                balance = c.CALCULATION_SETTINGS['EXCEPTIONS'][i]['REPLACE']
                        except Exception:
                            pass

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
                                logger.fatal('balance lower than zero for: {0}'.format(i))
                                raise NegativeBalanceError('balance lower than zero for: {0}'.format(i))

                    for i in voter_dict:
                        balance = voter_dict[i]['balance']

                        if voter_dict[i]['balance'] > c.CALCULATION_SETTINGS['MAX']:
                            balance = c.CALCULATION_SETTINGS['MAX']

                        try:
                            if balance > c.CALCULATION_SETTINGS['EXCEPTIONS'][i]['REPLACE']:
                                balance = c.CALCULATION_SETTINGS['EXCEPTIONS'][i]['REPLACE']
                        except Exception:
                            pass

                        if voter_dict[i]['status'] and voter_dict[i]['last_payout'] < blocks[block_nr].timestamp:
                            if c.CALCULATION_SETTINGS['SHARE_FEES']:
                                share = (balance/poolbalance) * (blocks[block_nr].reward +
                                                                 blocks[block_nr].totalFee)
                            else:
                                share = (balance/poolbalance) * blocks[block_nr].reward
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

        # an IndexError occurs if max(transactions.timestamp) > max(blocks.timestamp) This means we parsed every block
        except IndexError:
            pass

        for i in voter_dict:
            logger.info("{0}  {1}  {2}  {3}  {4}".format(i,
                                                         voter_dict[i]['share'],
                                                         voter_dict[i]['status'],
                                                         voter_dict[i]['last_payout'],
                                                         voter_dict[i]['vote_timestamp']))
        return voter_dict, max_timestamp