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
	
	#print out the first 100 words to see if anythings worth it
	for word in smart_words[:199]:
		print( word ) 	
		
