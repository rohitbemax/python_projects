import urllib
import urllib2
import re
import time
import sys
from bs4 import BeautifulSoup

def checkForLowestPrice() :
	lowestPrice = 0
	lowestPriceProdName = ""
	firstTimeFlag = True

	#Start compose the URL
	base_url = "http://www.snapdeal.com/search?"
	object_to_search = sys.argv[1]
	suffixURLString = urllib.urlencode({"keyword" : object_to_search, "santizedKeyword" : "", 
		"catId" : "", "suggested" : "false", "vertical" : "p", "noOfResults" : "20","clickSrc" : "go_header", 
		"cityPageUrl" : "", "url" : "", "utmContent" : "", "catalogID" : "", "dealDetail" : ""})

	#Print the composed URL
	print "URL: " + base_url+suffixURLString

	req = urllib2.Request(base_url + suffixURLString)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36') #We add user agent as Snapdeal doesnt allow usu GET request
	res = urllib2.urlopen(req)

	if res.code == 200:
		print "Page downloaded : OK"
	else:
		#No point to continue
		print 'Unable to download the page, will exit'
		exit()

	#Once the page is downloaded proceed with BeautifulSoup
	fpbs = BeautifulSoup(res.read(), "lxml")

	#Get all the products columns on the page
	products = fpbs.find_all("div", { "class" : "productWrapper" })

	#Products contains all the products on the page, filter for Name and Price
	for product in products:
		prod_title = product.find_all("div", { "class" : "product-title"})
		#Trim te extra spaces from the name (before and after)
		prod_sanatized_name = ((prod_title[0].text).lstrip()).rstrip()
		
		#Now check for price only if it is matches the product name specified
		if prod_sanatized_name.startswith(object_to_search):
			#If matching string is there we are interested in the price :)
			prod_price = product.find_all("span", { "id" : "price"})
			curPrice = int((re.sub('[^0-9]','', prod_price[0].text)))
			if firstTimeFlag:
				lowestPrice = curPrice
				lowestPriceProdName = prod_sanatized_name
				firstTimeFlag = False
			
			if curPrice < lowestPrice:
				lowestPrice = curPrice
			else:
				pass

			print "Product: {0:45s}  --> Price: {1:2s}".format(prod_sanatized_name, prod_price[0].text)
		else:
			#Do nothing just continue along
			pass

	print "\nLowest Price Details:\n---------------------\nProduct Name: " + lowestPriceProdName +  ", Price: Rs. " + str(lowestPrice)

def main() :
	while True:
		checkForLowestPrice()
		time.sleep(10)


if __name__ == "__main__": main()
