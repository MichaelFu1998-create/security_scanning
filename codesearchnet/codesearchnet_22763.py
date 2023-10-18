def tbw(self, delegate_address, blacklist=None, share_fees=False, compound_interest=False):
        """This function doesn't work yet. Instead use legacy.trueshare() for a functional tbw script"""
        if not blacklist:
            blacklist = []

        delegate_public_key = self.account_details(address=delegate_address)['public_key']
        height_at_calculation = self.node_height_details()['height']

        # string format of the rawasset
        minvote = '{{"votes":["-{0}"]}}'.format(delegate_public_key)
        plusvote = '{{"votes":["+{0}"]}}'.format(delegate_public_key)

        events = self.get_events_vote_cluster(delegate_address)
        votes = self.get_historic_voters(delegate_address)
        blocks = self.get_blocks(delegate_address)
    
        # create a map of voters
        voter_dict = {}
        for voter in votes:
            voter_dict.update({voter: {
                'balance': 0.0,
                'status': False,
                'last_payout': votes[voter]['height'],
                'share': 0.0,
                'vote_height': votes[voter]['height'],
                'blocks_forged': []}
            })

        for blacklisted_address in blacklist:
            voter_dict.pop(blacklisted_address, None)

        last_payout = self.get_last_out_transactions(delegate_address)

        # not all voters have had a payout, thus a KeyError is thrown
        for payout in last_payout:
            try:
                voter_dict[payout]['last_payout'] = last_payout[payout]['height']
            except KeyError:
                pass

        # the change in the previous state of the voter_dict. This is added to the voterdict if
        # no state change occurs in the blockchain.
        delta_state = {}
        no_state_change = False

        block_keys = sorted(list(blocks.keys()))
        block_nr = 0

        try:
            for id in events:
                # calculating poolbalances and updating shares
                if events[id]['height'] > blocks[block_keys[block_nr]]['height']:

                    # if the state is the same for the votepool, the previous calculation can be reused.
                    block_nr += 1
                    if no_state_change:
                        for x in delta_state:
                            voter_dict[x]['share'] += delta_state[x]
                        continue


                    # update pool balances
                    poolbalance = 0
                    delta_state = {}

                    for i in voter_dict:

                        # here we update the poolbalance
                        if compound_interest:
                            balance = voter_dict[i]['balance'] + voter_dict[i]['share']
                        else:
                            balance = voter_dict[i]['balance']

                        if voter_dict[i]['status']:
                            # if not voter_dict[i]['balance'] < 0:
                            poolbalance += balance
                            # else:
                            #     raise exceptions.NegativeBalanceError('balance lower than zero for: {0}. balance: {1}'.format(i, voter_dict[i]['balance']))

                    # here we calculate the share per voter
                    for i in voter_dict:
                        if compound_interest:
                            balance = voter_dict[i]['balance'] + voter_dict[i]['share']
                        else:
                            balance = voter_dict[i]['balance']

                        if voter_dict[i]['status'] and voter_dict[i]['last_payout'] < blocks[block_keys[block_nr]]['height']:
                            if share_fees:
                                share = (balance / poolbalance) * (blocks[block_keys[block_nr]]['reward'] +
                                                                   blocks[block_keys[block_nr]]['totalFee'])
                            else:
                                share = (balance / poolbalance) * blocks[block_keys[block_nr]]['reward']
                            voter_dict[i]['share'] += share
                            delta_state.update({i: share})

                    no_state_change = True
                    continue

                # parsing an event
                no_state_change = False

                if events[id]['event_type'] == 'transaction':
                    if events[id]['recipient_id'] == 'Acw2vAVA48TcV8EnoBmZKJdV8bxnW6Y4E9':
                        print(events[id]['amount'])

                # parsing a transaction
                if events[id]['event_type'] == 'transaction':
                    if events[id]['recipient_id'] in voter_dict:
                        voter_dict[events[id]['recipient_id']]['balance'] += events[id]['amount']

                    if events[id]['sender_id'] in voter_dict:
                        voter_dict[events[id]['sender_id']]['balance'] -= (events[id]['amount'] + events[id]['fee'])

                    if events[id]['sender_id'] in voter_dict and events[id]['type'] == 3 and plusvote in events[id]['rawasset']:
                        voter_dict[events[id]['sender_id']]['status'] = True

                    if events[id]['sender_id'] in voter_dict and events[id]['type'] == 3 and minvote in events[id]['rawasset']:
                        voter_dict[events[id]['sender_id']]['status'] = False

                # parsing a forged block (if forged by a voter)
                if events[id]['event_type'] == 'block':
                    voter_dict[events[id]['address']]['balance'] += (events[id]['reward'] + events[id]['total_fee'])

            # the transaction for loop ends with the final transaction. However more blocks may be forged. This copies
            # the final delta share and adds it to the share x the amount of blocks left.
            remaining_blocks = len(block_keys) - block_nr - 1
            for i in range(remaining_blocks):
                for x in delta_state:
                    voter_dict[x]['share'] += delta_state[x]

            # and indexerror indicates that we have ran out of forged blocks, thus the calculation is done (blocks[block_nr]
            # throw the error)
        except IndexError:
            raise

        return voter_dict, height_at_calculation