from chat_replay_downloader import *
from unicodedata import normalize
import re
import json
import time
import datetime
from currency_converter import CurrencyConverter


c = CurrencyConverter()
currency_dic = {}
with open("currency_table") as file:
    for l in file:
        youtube_symbol, iso_symbol = l.strip().split(" ")
        currency_dic[youtube_symbol] = iso_symbol

def Extract_Resume_From_Messages(messages):

	donations_array = [(msg["amount_euros"],msg["author"]) for msg in messages if "amount_value" in msg]

	start_str = messages[0]["timestamp_str"]
	start_unix = int(messages[0]["timestamp"] / 1000000)
	end_str = messages[-1]["timestamp_str"]
	end_unix = int(messages[-1]["timestamp"] / 1000000)
	duration_seconds = int((messages[-1]["timestamp"] - messages[0]["timestamp"])/1000000)
	duration_str = str(datetime.timedelta(seconds=duration_seconds))

	donations_array.sort(key = lambda a : -a[0])
	donations_total = sum([item[0] for item in donations_array])
	biggest_donation = donations_array[0][0]
	biggest_donator = donations_array[0][1]
	donations_n = len(donations_array)
	
	unknown_donations = [msg["amount_currency"] for msg in messages if "amount_value" in msg and msg["currency_code"] == "not found"]
	number_of_unknown_donations = len(unknown_donations)
	unknown_youtube_currencies = list(set(unknown_donations))

	resume = {"start_str" : start_str,
			  "start_unix" : start_unix,
			  "end_str":end_str,
			  "end_unix":end_unix,
			  "duration_seconds" : duration_seconds, 
			  "duration_str" : duration_str,
			  "donations_total" : donations_total,
			  "biggest_donation" : biggest_donation,
			  "biggest_donator" : biggest_donator,
			  "donations_n" : donations_n,
			  "number_of_unknown_donations" : number_of_unknown_donations,
			  "unknown_youtube_currencies":unknown_youtube_currencies}
	
	return resume



def Extract_Amount_And_Currency_wo_compile(mystring):
	
	reversed_mystring = mystring[::-1]
	reversed_amount = re.findall("^[\d\.,]+",reversed_mystring)[0]
	string_amount = reversed_amount[::-1]
	amount = float(string_amount.replace(',',''))
	
	currency = re.findall("^[^\d\.,\s]+",mystring)[0]
	
	return (amount,currency)



def unix_to_string_ts(unixts):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixts))


def Add_Entries_To_Messages(messages,url_video):

	errors = 0
	for msg in messages:

		msg["url"] = url_video
		msg["timestamp_str"] = unix_to_string_ts(msg["timestamp"]/1000000)

		if "amount" in msg:
			try:
				amval,amcur = Extract_Amount_And_Currency_wo_compile(msg["amount"])
			except:
				errors = errors + 1
				amval = 0
				amcur = 0
			msg["amount_value"] = amval
			msg["amount_currency"] = amcur
			msg["currency_code"] = currency_dic.get(amcur,"not found")
			
			try:
				msg["amount_euros"] = c.convert(amval,msg["currency_code"],"EUR")
			except:
				msg["amount_euros"] = 0
				

		
	return messages,errors




def Get_Money(urls_list):
	video = {}
	for url_video in urls_list:
		try:
			messages = get_chat_replay(url = url_video,message_type = "superchat")
		except:
			continue
		messages,errors = Add_Entries_To_Messages(messages,url_video)
		resume = Extract_Resume_From_Messages(messages)
		video[url_video] = {"url":url_video,
						"messages":messages,
						"resume":resume,
						"errors":errors}
	return video