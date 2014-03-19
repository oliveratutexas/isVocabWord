#!/py

'''
	Author: Oliver Croomes
	StartDate: March 10th
	Goal: To read in a book, and then determine which words are worth learning as
		"vocabulary words"

	What should I filter out:
		- Proper nouns
			-Names
			-Reocurring places
		- Common Words
			-Pronouns
			-Linking Verbs
		
'''

# regex
import re
import sys

# this is somehow used for sorting
import operator

import GoogleScraper
import urllib.parse


vocab_hint_list = ["http://dictionary.cambridge.org/us/dictionary/american-english/","http://dictionary.reference.com/","http://en.wiktionary.org/wiki/","http://mnemonicdictionary.com/word/","http://thesaurus.com/browse/","http://www.collinsdictionary.com/dictionary/english/","http://www.dict.cc/?s=","http://www.macmillandictionary.com/us/dictionary/american/","http://www.merriam-webster.com/dictionary/","http://www.oxforddictionaries.com/us/definition/american_english/","http://www.thefreedictionary.com/","http://www.vocabulary.scom/dictionary/","http://www.wordreference.com/definition/"]



vocab_list = set()

if __name__=='__main__':
	dictionary = dict()
	trash = set()
	
	if(sys.argv[1] == None):
		print(u"Program arguments are:\nprg_name file.txt")
		exit()

	#copypasted
	text = ''.join(open(sys.argv[1]).readlines())

	# add all the words in the dirty list
	for word in (''.join(open("dirtywords.txt","r").readlines())).split():
		trash.add(word)

	#thought this would be okay, because there's not too much in ram. Talkin kilobytes probably.
	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

	#end copypasta

	for sen in sentences:
		words =  sen.split()

		for x in range(0,len(words)):

			if words[x] in trash:
				pass

			elif x == 0:
				#can't do much with the first word, since it's always capital.
				pass		

			elif words[x].isalpha():
				if words[x][0].isupper():
					trash.add(words[x])
				if words[x] in dictionary:
					if dictionary[words[x]] >= 2:
						trash.add(words[x])
						del dictionary[words[x]]
					else:
						dictionary[words[x]] += 1
				else:
					#add it do dictionary
					dictionary[words[x]] = 1

	#actually sort the items from the dictionary
	smart_words = sorted(dictionary.items(), key=operator.itemgetter(1,0),reverse=True)
	num_words = 100	
	#print out the first 100 words to see if anythings worth it
	for word in smart_words[:num_words]:
		
		results = GoogleScraper.scrape(word[0],num_results_per_page=20, num_pages=1, offset=0, searchtype='normal')
		print("W: %s" % word[0])
		urls = []
		hint_count = 0
		#need at least two dictionary sites to be classified as a dictionary word
		hint_threshold = 2
		page = results[0]
		
		for link_title, link_snippet, link_url in page['results']:
		    # You can access all parts of the search results like that
			try:
				urls.append(urllib.parse.unquote(link_url.geturl()))
			except:
				pass

		for hint in vocab_hint_list:
			for site in urls[:3]:
				if hint in site:
					hint_count += 1
					#vocab_list.add(word[0])
					print("\tHint:%s" % hint[7:])
		
		if(hint_count >= hint_threshold):
			vocab_list.add(word[0])
			print("\t\tAdded %s to vocab list" % word[0])
		
	
	print(vocab_list)	
	print("Found %d words as vocab words out of %d" % (len(vocab_list),num_words))
