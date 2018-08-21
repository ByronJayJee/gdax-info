import gdax
import time
import gdax_global_data as ggd
import pandas as pd
import pprint
import json

class myWebsocketClient(gdax.WebsocketClient,object):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        #self.products = ["LTC-USD"]
        self.message_count = 0
        # Create class object that is Pandas DataFrame
        self.df = pd.DataFrame(columns=['time', 'trade_id', 'price'])
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg and msg["type"]=="match":
            #print(msg)
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
            # Append message to dataframe
            # This use of pandas dataframe is VERY inefficient!!! Come up with something better for long-term
            self.df = self.df.append({'time': msg['time'], 'trade_id': msg['trade_id'], 'price': msg['price']}, ignore_index=True)
    def on_close(self):
        print("-- Goodbye! --")


public_client = gdax.PublicClient()

#product_list = public_client.get_products()
#pprint.pprint(product_list)

#print(json.dumps(ggd.product_list, sort_keys=True, indent=4))

#myProd = ["LTC-USD"]
myProd = ["BTC-USD"]

wsClient = myWebsocketClient(products=myProd)
wsClient.start()
print(wsClient.url, wsClient.products)
minute_count=0
#while (wsClient.message_count < 5000):
while (minute_count < 30):
    #print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    print ("\nminute_count =", "{} \n".format(minute_count))
    time.sleep(60)
    minute_count += 1
wsClient.close()

print(wsClient.df)

# Convert time property to an actual timestamp
wsClient.df['time'] = pd.to_datetime(wsClient.df['time'])

# use the timestamp as dataframe index
# this effectievely makes this a time series
wsClient.df.index = wsClient.df['time']

print(wsClient.df.dtypes)

# Convert the 'trade_id' and 'price' columns to type: float
d=wsClient.df.astype({'trade_id':float, 'price':float})
print(d.dtypes)
print(d)

# resample data into 1 minute intervals
r=d.resample('1min')
#r=d.resample('5S')

# forward fill missing data in resampled dataframe
rl_fill = r.last().ffill()

# compute moving average of price data in resampled dataframe
rl_fill['ma'] = rl_fill['price'].rolling(9).mean()

# compute difference in price and moving average in resampled dataframe
rl_fill['diff'] = rl_fill['price']-rl_fill['ma']
print(r)
print(rl_fill)

'''
ticker_count=0
while (ticker_count < 5):
    prod_ticker = public_client.get_product_ticker(product_id='ETH-USD')
    time.sleep(3)
    print(prod_ticker)
    ticker_count += 1
'''
