import gdax
import time
import gdax_global_data as ggd
import pprint
import json

class myWebsocketClient(gdax.WebsocketClient,object):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        #self.products = ["LTC-USD"]
        self.message_count = 0
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg and msg["type"]=="match":
            print(msg)
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")


public_client = gdax.PublicClient()

#product_list = public_client.get_products()
#pprint.pprint(product_list)

#print(json.dumps(ggd.product_list, sort_keys=True, indent=4))

myProd = ["LTC-USD"]

wsClient = myWebsocketClient(products=myProd)
wsClient.start()
print(wsClient.url, wsClient.products)
while (wsClient.message_count < 5000):
    print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()
'''
ticker_count=0
while (ticker_count < 5):
    prod_ticker = public_client.get_product_ticker(product_id='ETH-USD')
    time.sleep(3)
    print(prod_ticker)
    ticker_count += 1
'''
