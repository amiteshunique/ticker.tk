import urllib.request
import time
import struct
import sys
from bs4 import BeautifulSoup 
from urllib.request import Request, urlopen
from datetime import datetime, date


def send_message_to_slack(text):
    from urllib import request, parse
    import json

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

dict = {'RELIANCE':'https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI',
	'BHARTIARTL':'https://www.moneycontrol.com/india/stockpricequote/telecommunications-service/bhartiairtel/BA08',
	'TATAMOTORS':'https://www.moneycontrol.com/india/stockpricequote/auto-lcvshcvs/tatamotors/TM03',
	'CHEMCON':'https://www.moneycontrol.com/india/stockpricequote/speciality-chemicals/chemconspecialitychemicals/CSC',
	'IRCTC':'https://www.moneycontrol.com/india/stockpricequote/misc-commercial-services/irctc-indianrailwaycateringtourismcorp/IRC',
	'CAMS':'https://www.moneycontrol.com/india/stockpricequote/online-services/computeragemanagementservices/CAM',
	'SBIN':'https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/statebankindia/SBI',
	'SBICARD':'https://www.moneycontrol.com/india/stockpricequote/finance-term-lending/sbicardspaymentservices/SCP02',
	'HDFCBANK':'https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/hdfcbank/HDF01',
	'HDFC':'https://www.moneycontrol.com/india/stockpricequote/finance-housing/housingdevelopmentfinancecorporation/HDF',
	'ICICIBANK':'https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/icicibank/ICI02',
	'BALRAMCHIN':'https://www.moneycontrol.com/india/stockpricequote/sugar/balrampurchinimills/BCM',
	}
seen_prcnt = {}

def ticker( stock ): 
	# the target we want to open	 
	stock = stock.upper()

	#if Stock is not found then exit
	url = dict.get(stock)
	if url is None: 
		exit()

	#print("Open the web page from url")
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	resp = urlopen(req).read()
	
	#print("Successfully opened the web page from url")
	soup=BeautifulSoup(resp,'html.parser')
	

	#print("....Processing........");
	name_data 		= soup.find("h1", {"class": "pcstname"})
	prev_price_data = soup.find("p", {"class": "prev_open priceprevclose"})
	open_price_data = soup.find("p", {"class": "prev_open priceopen"})

	#Red highlight
	curr_price_data = soup.find("span", {"class": "span_price_wrap stprh red_hilight rdclr"})
	chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt rdpc1"})

	#Red only
	if curr_price_data is None :
		curr_price_data = soup.find("span", {"class": "span_price_wrap stprh rdclr"})
		chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt rdpc1"})
	
	#Green highlight
	if curr_price_data is None :
		curr_price_data	= soup.find("span", {"class": "span_price_wrap stprh grn_hilight grnclr"})
		chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt grnpc1"})
	
	#Green only
	if curr_price_data is None :
		curr_price_data	= soup.find("span", {"class": "span_price_wrap stprh grnclr"})
		chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt grnpc1"})

	#Neutral highlight
	if curr_price_data is None :
		curr_price_data	= soup.find("span", {"class": "span_price_wrap stprh neautral_bg neautral_color"})
		chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt neautral_color"})

	#Neutral only
	if curr_price_data is None :
		curr_price_data	= soup.find("span", {"class": "span_price_wrap stprh neautral_color"})
		chg_price_data 	= soup.find("span", {"class": "span_price_change_prcnt neautral_color"})
	
	#Cleaning the parse in presentable form
	name 			= "".join(name_data.text)
	if curr_price_data is None :
		print(name+" Unable to fetch curr_price")
		return (name+" Unable to fetch curr_price")
	
	curr_price 		= "".join(curr_price_data.text.split())
	prev_price 		= "".join(prev_price_data.text.split())
	open_price 		= "".join(open_price_data.text.split())
	
	chg_price 		= "".join(chg_price_data.text.split())
	temp 			= chg_price.split("(")
	c_price			= float(temp[0])
	c_price_percent	= float(temp[1].split("%")[0])
	
	#All set to return the output
	output = "Name:"+name+"("+stock+")"+"\nCurrent Stock Price:"+curr_price+"\nPrice Change:"+str(c_price)+"("+str(c_price_percent)+"%)"+"\nYesterday's Closing Price:"+prev_price+"\nToday's Opening Price:"+open_price+"\nLast Seen Percent:"+str(seen_prcnt[stock])+"%\n\n"
	
	#If percent difference is greater than last seen value then only return output
	if abs(seen_prcnt[stock] - c_price_percent) > 0.5 :
		seen_prcnt[stock] = c_price_percent
		return output


send_message_to_slack("Starting the Ticker server..!!!")
# Stock related
#print(ticker('RELIANCE')
#print(ticker('TATAMOTORS')

#Initialize the ticker change in percent for each stock
for stock in dict:
	seen_prcnt[stock] = 0

msg = ""
wakeup_msg = "Server woken-up at: "+str(datetime.now())
#Loop 
while True :
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	current_hr = now.strftime("%H")
	date_time = str(date.today())+ " , " + current_time
	#print(date_time)
	
	#Wakeup msg
	#send_message_to_slack(wakeup_msg)
	print(wakeup_msg)
	
	msg = date_time
	result = ""
	for stock in dict:
		out = ticker(stock)
		if out is None:
			continue
		#print(out)
		result = result + out
		#print("Slack:"+result)

	
	if result == "":
		continue
	
	send_message_to_slack("Alert at: "+msg)
	send_message_to_slack(result)
	send_message_to_slack("#####################")
	print("Alert at: "+msg)
	print(result)
	print("#####################")
	
	

	
	time.sleep(5)
