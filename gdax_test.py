import gdax
import gdax_global_data as ggd
import pprint
import json

#public_client = gdax.PublicClient()

#product_list = public_client.get_products()
#pprint.pprint(product_list)

print(json.dumps(ggd.product_list, sort_keys=True, indent=4))
