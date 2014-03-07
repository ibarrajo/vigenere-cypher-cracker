from  __builtin__ import any as b_any
import time
import sys
import thread
import sqlite3
from subprocess import call

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def createTable():
	conn = sqlite3.connect('crypto.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS wordlist
	             (key text, cleartext text, words real, score real)''')
	conn.commit()
	conn.close()


def addEntry(key, cleartext, words, score):
	conn = sqlite3.connect('crypto.db')
	c = conn.cursor()
	c.execute("INSERT INTO wordlist VALUES ('%s', '%s', %s, %s)" % (key, cleartext, words, score))
	conn.commit()

cyphertext = "ZEJFOKHTMSRMELCPODWHCGAW"

# key: DAY
# ctxt: WELCOMETOPROBLEMOFTHEDAY

def crack(keys, dictionary):
	with open(keys) as keylist:
		for key in keylist:
			key = key.strip()
			wordCount = 0
			score = 0
			cleartxt = decryptMessage(key, cyphertext)
			for word in dictionary:
				word = word.strip()
				if (word in cleartxt and (len(word) > 3)):
					wordCount = wordCount + 1
					score = score + len(word)
			if (score > 12):
				print("%s %s   %s    %s \n" % (cleartxt, key, wordCount, score))
				addEntry(key, cleartxt, wordCount, score)
		print(keys + " IS ALL DONE!")
		return 0

def main():
	generate_words()
	createTable()

	englishDictionary = open("english.dic")
	dictionary = englishDictionary.readlines()
	try:
		thread.start_new_thread( crack, ("listaa",dictionary,) )
		thread.start_new_thread( crack, ("listab",dictionary,) )
		thread.start_new_thread( crack, ("listac",dictionary,) )
		thread.start_new_thread( crack, ("listad",dictionary,) )
		thread.start_new_thread( crack, ("listae",dictionary,) )
	except:
		print "Error: unable to start thread"

	while 1:
		pass


def generate_words():
	with open("list.dic","a") as listFile:
		print("Generating single char list:")
		for char1 in LETTERS:
			listFile.write(char1 + "\n")

		print("Generating two word:")
		for char1 in LETTERS:
			for char2 in LETTERS:
				listFile.write(char1 + char2 + "\n")

		print("Generating three word:")
		for char1 in LETTERS:
			for char2 in LETTERS:
				for char3 in LETTERS:
					listFile.write(char1 + char2 + char3 + "\n")


		print("Generating four word:")
		for char1 in LETTERS:
			for char2 in LETTERS:
				for char3 in LETTERS:
					for char4 in LETTERS:
						listFile.write(char1 + char2 + char3 + char4 + "\n")


		print("Generating five word:")
		for char1 in LETTERS:
			for char2 in LETTERS:
				for char3 in LETTERS:
					for char4 in LETTERS:
						for char5 in LETTERS:
							listFile.write(char1 + char2 + char3 + char4 + char5 + "\n")
		# divide the resulting file into 5 files
		call(["wc","-l", "2471326", "list.dic", "list"])



def encryptMessage(key, message):
	return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
	return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
	translated = [] # stores the encrypted/decrypted message string

	keyIndex = 0
	key = key.upper()

	for symbol in message: # loop through each character in message
		num = LETTERS.find(symbol.upper())
		if num != -1: # -1 means symbol.upper() was not found in LETTERS
			if mode == 'encrypt':
				num += LETTERS.find(key[keyIndex]) # add if encrypting
			elif mode == 'decrypt':
				num -= LETTERS.find(key[keyIndex]) # subtract if decrypting

			num %= len(LETTERS) # handle the potential wrap-around

			# add the encrypted/decrypted symbol to the end of translated.
			if symbol.isupper():
				translated.append(LETTERS[num])
			elif symbol.islower():
				translated.append(LETTERS[num].lower())

			keyIndex += 1 # move to the next letter in the key
			if keyIndex == len(key):
				keyIndex = 0
		else:
			# The symbol was not in LETTERS, so add it to translated as is.
			translated.append(symbol)

	return ''.join(translated)


# If vigenereCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
	main()