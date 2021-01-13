from chat_replay_downloader import *
from unicodedata import normalize
import re
import json
import sys
import argparse
from fun import *

currency_dic = {}
with open("currency_table") as file:
    for l in file:
        youtube_symbol, iso_symbol = l.strip().split(" ")
        currency_dic[youtube_symbol] = iso_symbol


def Get_Donations_For_URLs_List(args):

	urls_filename = args.urls_filename
	saved_filename = args.saved_filename

	# RÉCUPERATION DE LA URL LIST CONTENU DANS LE URLS FILENAME
	urls_list = []
	with open(urls_filename) as file:
		for l in file:
			urls_list.append(l.strip())

	# CREATION DU DICO DONATIONS
	donations = Get_Money(urls_list)

	# SAUVEGARDE DU DICO DONATION AU FORMAT JSON
	with open(saved_filename, 'w') as outfile:
		json.dump(donations, outfile)


	return None




if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='test arguments')
	parser.add_argument('-u', '--urls_filename')
	parser.add_argument('-s','--saved_filename')
	args = parser.parse_args()
	Get_Donations_For_URLs_List(args)