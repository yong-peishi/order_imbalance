import requests

def depth_info(symbol, minimum):
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/ticker/24hr'
    params = {'symbol': symbol}
    depth_endpoint='/api/v3/depth'
    limit = 10
    depth_params = {'symbol': symbol, 'limit': limit}

    try:
        response = requests.get(base_url + endpoint, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        price = float(data['lastPrice'])

        min_price = price * 

        depth_response = requests.get(base_url + depth_endpoint, depth_params)
        depth_response.raise_for_status()

        depth_data = depth_response.json()
        bids=depth_data['bids']
        asks=depth_data['asks']
        if len(bids) == 0 or len(asks) == 0:
            return
        
        bids_depth = 0
        #print('Bids', bids)
        for bid in bids:
            bids_depth += float(bid[1])
        bids_depth = round(bids_depth, 2)
        first_bid_price = round(float(bids[0][0]), 2)
        last_bid_price = round(float(bids[limit-1][0]), 2)
        bid_price_diff = round(last_bid_price - first_bid_price, 2)
        #print('First Bid Price:', first_bid_price, 'Last Bid Price:', last_bid_price, 'Diff:', bid_price_diff)
        #print('Bids Depth:', bids_depth)

        asks_depth = 0
        #print('Asks', asks)
        for ask in asks:
            asks_depth += float(ask[1])
        asks_depth = round(asks_depth, 2)
        first_ask_price = round(float(asks[0][0]), 2)
        last_ask_price = round(float(asks[limit-1][0]), 2)
        ask_price_diff = round(last_ask_price - first_ask_price,2)
        #print('First Ask Price:', first_ask_price, 'Last Ask Price:', last_ask_price, 'Diff:', ask_price_diff)
        #print('Asks Depth:', asks_depth)

        ask_to_bid = round(asks_depth/bids_depth, 2)
        #print('Ask to Bid', ask_to_bid)
        bid_to_ask = round(bids_depth/asks_depth, 2)
        #print('Bid to Ask', bid_to_ask)

        message = []
        if ask_to_bid >= minimum:
            message.append('Ask to Bid:')
            message.append(ask_to_bid)
        elif bid_to_ask >= minimum:
            message.append('Bid to Ask:')
            message.append(bid_to_ask)
        return message

    except requests.exceptions.RequestException as e:
        return f"Error fetching market data: {e}"