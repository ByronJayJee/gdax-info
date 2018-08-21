import gdax
import time
from datetime import date, timedelta, datetime
import gdax_global_data as ggd
import pandas as pd
import pprint
import json

# 12, 26, 9

def compute_macd(price_history):
	ph = price_history
	#print(ph)

	# Convert time property to an actual timestamp
	ph['time_dt'] = pd.to_datetime(ph['time'])
	
	# use the timestamp as dataframe index
	# this effectievely makes this a time series
	ph.index = wsClient.df['time_dt']
	
	#print(ph.dtypes)
	
	# Convert the 'trade_id' and 'price' columns to type: float
	d=ph.astype({'trade_id':float, 'price':float})
	#print(d.dtypes)
	#print(d)
	
	# resample data into 1 minute intervals
	#r=d.resample('1min')
	r=d.resample('5S') # use 5 sec for testing!!
	
	# forward fill missing data in resampled dataframe
	rl_fill = r.last().ffill()
	
	# compute moving average of price data in resampled dataframe
	rl_fill['ema26'] = rl_fill['price'].ewm(span=26, min_periods=26).mean()
	rl_fill['ma26'] = rl_fill['price'].rolling(26).mean()
	rl_fill['ma12'] = rl_fill['price'].rolling(12).mean()
	rl_fill['ema12'] = rl_fill['price'].ewm(span=12, min_periods=12).mean()
	rl_fill['macd'] = rl_fill['ema12']-rl_fill['ema26']
	rl_fill['signal9'] = rl_fill['macd'].ewm(span=9, min_periods=9).mean()
	#rl_fill['ma26'] = rl_fill['price'].rolling(26).mean()

	# compute difference in price and moving average in resampled dataframe
	#rl_fill['diff'] = rl_fill['price']-rl_fill['ma9']
	#rl_fill['macd'] = rl_fill['ma12']-rl_fill['ma26']
	#print(r)
	print(rl_fill)

def remove_old_data(price_history):
	#sometimeago = datetime.utcnow() - timedelta(seconds=45)
	sometimeago = datetime.utcnow() - timedelta(seconds=200)
	#print('sometimeago ' + str(sometimeago))
	old_points = price_history[(price_history['time_dt'] < sometimeago)]
	price_history.drop(old_points.index,inplace=True)	
	#print('price_history')
	#print(price_history)

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
            #print ("Message type:", msg["type"],
            #       "\t@ {:.3f}".format(float(msg["price"])))
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
#while (minute_count < 30):
while (minute_count < 10):
    #print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    print ("\nminute_count =", "{} \n".format(minute_count))
    time.sleep(60)
    minute_count += 1
    print(wsClient.df.shape)
    compute_macd(wsClient.df)
    remove_old_data(wsClient.df)
wsClient.close()

#compute_macd(wsClient.df)

'''
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
#r=d.resample('1min')
r=d.resample('5S') # use 5 sec for testing!!

# forward fill missing data in resampled dataframe
rl_fill = r.last().ffill()

# compute moving average of price data in resampled dataframe
rl_fill['ma9'] = rl_fill['price'].rolling(9).mean()
rl_fill['ma12'] = rl_fill['price'].rolling(12).mean()
#rl_fill['ma26'] = rl_fill['price'].rolling(26).mean()

# compute difference in price and moving average in resampled dataframe
#rl_fill['diff'] = rl_fill['price']-rl_fill['ma9']
#rl_fill['macd'] = rl_fill['ma12']-rl_fill['ma26']
print(r)
print(rl_fill)
'''

'''
ticker_count=0
while (ticker_count < 5):
    prod_ticker = public_client.get_product_ticker(product_id='ETH-USD')
    time.sleep(3)
    print(prod_ticker)
    ticker_count += 1
'''
