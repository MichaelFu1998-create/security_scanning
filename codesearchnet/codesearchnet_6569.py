def itemParse(item_data, full=True):
    """Parser for item data. Returns nice dictionary.

    :params item_data: Item data received from ea servers.
    :params full: (optional) False if you're sniping and don't need extended info. Anyone really use this?
    """
    # TODO: object
    # TODO: dynamically parse all data
    # TODO: make it less ugly
    # ItemRareType={NONE:0,RARE:1,LOCK:2,TOTW:3,PURPLE:4,TOTY:5,RB:6,GREEN:7,ORANGE:8,PINK:9,TEAL:10,TOTS:11,LEGEND:12,WC:13,UNICEF:14,OLDIMOTM:15,FUTTY:16,STORYMODE:17,CHAMPION:18,CMOTM:19,IMOTM:20,OTW:21,HALLOWEEN:22,MOVEMBER:23,SBC:24,SBCP:25,PROMOA:26,PROMOB:27,AWARD:28,BDAY:30,UNITED:31,FUTMAS:32,RTRC:33,PTGS:34,FOF:35,MARQUEE:36,CHAMPIONSHIP:37,EUMOTM:38,TOTT:39,RRC:40,RRR:41}
    return_data = {
        'tradeId': item_data.get('tradeId'),
        'buyNowPrice': item_data.get('buyNowPrice'),
        'tradeState': item_data.get('tradeState'),
        'bidState': item_data.get('bidState'),
        'startingBid': item_data.get('startingBid'),
        'id': item_data.get('itemData', {'id': None})['id'] or item_data.get('item', {'id': None})['id'],
        'offers': item_data.get('offers'),
        'currentBid': item_data.get('currentBid'),
        'expires': item_data.get('expires'),  # seconds left
        'sellerEstablished': item_data.get('sellerEstablished'),
        'sellerId': item_data.get('sellerId'),
        'sellerName': item_data.get('sellerName'),
        'watched': item_data.get('watched'),
        'resourceId': item_data.get('resourceId'),  # consumables only?
        'discardValue': item_data.get('discardValue'),  # consumables only?
    }
    if full:
        if 'itemData' in item_data:
            return_data.update({
                'timestamp': item_data['itemData'].get('timestamp'),  # auction start
                'rating': item_data['itemData'].get('rating'),
                'assetId': item_data['itemData'].get('assetId'),
                'resourceId': item_data['itemData'].get('resourceId'),
                'itemState': item_data['itemData'].get('itemState'),
                'rareflag': item_data['itemData'].get('rareflag'),
                'formation': item_data['itemData'].get('formation'),
                'leagueId': item_data['itemData'].get('leagueId'),
                'injuryType': item_data['itemData'].get('injuryType'),
                'injuryGames': item_data['itemData'].get('injuryGames'),
                'lastSalePrice': item_data['itemData'].get('lastSalePrice'),
                'fitness': item_data['itemData'].get('fitness'),
                'training': item_data['itemData'].get('training'),
                'suspension': item_data['itemData'].get('suspension'),
                'contract': item_data['itemData'].get('contract'),
                'position': item_data['itemData'].get('preferredPosition'),
                'playStyle': item_data['itemData'].get('playStyle'),  # used only for players
                'discardValue': item_data['itemData'].get('discardValue'),
                'itemType': item_data['itemData'].get('itemType'),
                'cardType': item_data['itemData'].get('cardsubtypeid'),  # alias
                'cardsubtypeid': item_data['itemData'].get('cardsubtypeid'),  # used only for cards
                'owners': item_data['itemData'].get('owners'),
                'untradeable': item_data['itemData'].get('untradeable'),
                'morale': item_data['itemData'].get('morale'),
                'statsList': item_data['itemData'].get('statsList'),  # what is this?
                'lifetimeStats': item_data['itemData'].get('lifetimeStats'),
                'attributeList': item_data['itemData'].get('attributeList'),
                'teamid': item_data['itemData'].get('teamid'),
                'assists': item_data['itemData'].get('assists'),
                'lifetimeAssists': item_data['itemData'].get('lifetimeAssists'),
                'loyaltyBonus': item_data['itemData'].get('loyaltyBonus'),
                'pile': item_data['itemData'].get('pile'),
                'nation': item_data['itemData'].get('nation'),  # nation_id?
                'year': item_data['itemData'].get('resourceGameYear'),  # alias
                'resourceGameYear': item_data['itemData'].get('resourceGameYear'),
                'marketDataMinPrice': item_data['itemData'].get('marketDataMinPrice'),
                'marketDataMaxPrice': item_data['itemData'].get('marketDataMaxPrice'),
                'loans': item_data.get('loans'),
            })
        elif 'item' in item_data:  # consumables only (?)
            return_data.update({
                'cardassetid': item_data['item'].get('cardassetid'),
                'weightrare': item_data['item'].get('weightrare'),
                'gold': item_data['item'].get('gold'),
                'silver': item_data['item'].get('silver'),
                'bronze': item_data['item'].get('bronze'),
                'consumablesContractPlayer': item_data['item'].get('consumablesContractPlayer'),
                'consumablesContractManager': item_data['item'].get('consumablesContractManager'),
                'consumablesFormationPlayer': item_data['item'].get('consumablesFormationPlayer'),
                'consumablesFormationManager': item_data['item'].get('consumablesFormationManager'),
                'consumablesPosition': item_data['item'].get('consumablesPosition'),
                'consumablesTraining': item_data['item'].get('consumablesTraining'),
                'consumablesTrainingPlayer': item_data['item'].get('consumablesTrainingPlayer'),
                'consumablesTrainingManager': item_data['item'].get('consumablesTrainingManager'),
                'consumablesTrainingGk': item_data['item'].get('consumablesTrainingGk'),
                'consumablesTrainingPlayerPlayStyle': item_data['item'].get('consumablesTrainingPlayerPlayStyle'),
                'consumablesTrainingGkPlayStyle': item_data['item'].get('consumablesTrainingGkPlayStyle'),
                'consumablesTrainingManagerLeagueModifier': item_data['item'].get(
                    'consumablesTrainingManagerLeagueModifier'),
                'consumablesHealing': item_data['item'].get('consumablesHealing'),
                'consumablesTeamTalksPlayer': item_data['item'].get('consumablesTeamTalksPlayer'),
                'consumablesTeamTalksTeam': item_data['item'].get('consumablesTeamTalksTeam'),
                'consumablesFitnessPlayer': item_data['item'].get('consumablesFitnessPlayer'),
                'consumablesFitnessTeam': item_data['item'].get('consumablesFitnessTeam'),
                'consumables': item_data['item'].get('consumables'),
                'count': item_data.get('count'),  # consumables only (?)
                'untradeableCount': item_data.get('untradeableCount'),  # consumables only (?)
            })

    return return_data