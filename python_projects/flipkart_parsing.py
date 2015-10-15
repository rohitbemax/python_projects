import urllib
import urllib2
import re
import sys
from bs4 import BeautifulSoup

lowestPrice = 0
lowestPriceProdName = ""
firstTimeFlag = True

#Start compose the URL
base_url = "http://www.flipkart.com/search?"
object_to_search = "Apple iPhone 4S"
object_to_search = sys.argv[1]
suffixURLString = urllib.urlencode({"q" : object_to_search, "as" : "off", "as-show" : "off", "otracker" : "start" })
#fp = urllib.urlopen("http://www.flipkart.com/search?q=iphone+5s&as=on&as-show=on&otracker=start&as-pos=1_q#jumpTo=914|20")
print "URL: " + base_url + suffixURLString
fp = urllib.urlopen(base_url + suffixURLString)
#End of URL Conposition

if fp.code == 200:
	print "Page downloaded : OK"
else:
	#No point to continue
	print 'Unable to download the page, will exit'
	exit()

#Once the page is downloaded proceed with BeautifulSoup
fpbs = BeautifulSoup(fp.read(), "lxml")

#Get all the products columns on the page
products = fpbs.find_all("div", { "class" : "gd-col gu3" })

#Products contains all the products on the page, filter for Name and Price
for product in products:
	prod_title = product.find_all("a", { "data-tracking-id" : "prd_title"})

	#Now check for price only if it is an Apple iPhone 5s
	#if prod_title[0]['title'].startswith("Apple iPhone 5S"):
	if prod_title[0]['title'].startswith(object_to_search):
		#If matching string is there we are interested in the price :)
		prod_price = product.find_all("span", { "class" : "fk-font-17 fk-bold"})
		
		#if lowestPrice > int((prod_price[0].text).replace(",", "")):
		curPrice = int((re.sub('[^0-9]','', prod_price[0].text)))
		if firstTimeFlag:
			lowestPrice = curPrice
			lowestPriceProdName = prod_title[0]['title']
			firstTimeFlag = False
		
		if curPrice < lowestPrice:
			lowestPrice = curPrice
		else:
			pass

		print "Product: {0:45s}  --> Price: {1:2s}".format(prod_title[0]['title'], prod_price[0].text)
	else:
		#Do nothing just continue along
		pass

print "\nLowest Price Details:\n---------------------\nProduct Name: " + lowestPriceProdName +  ", Price: Rs. " + str(lowestPrice)