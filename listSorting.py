#!/usr/bin/env python
'''
Written by Carlos A. Cedeno for consideration of Nopsec
listSorting.py takes two arguments, an input file and an output file.
It sanitizes the strings for only alpha numeric characters, sorts the strings and prints them to the outputfile
while maintaining original placements of different types of elements (in this case 
only strings and integers are expected and handeled)
'''
import sys

def split_and_sanitize(data):			#function for separating raw input data into strings, and then sanitizing those strings. Returns a python list of sanatized strings.
  list_of_words = data.split(" ")		#create a list of strings, each selected and seperated by their delimiter, the space character.
  sanitized_words = [] 				#create a new list for holding sanitized words
  for word in list_of_words: 			#for every string in the unsanitized list...
    clean_word = ''.join( char for char in word if char.isalnum()) #create a new santized string by joining only alpha-numeric characters of the current string
    sanitized_words.append(clean_word)		#append santized string to santized list
  return sanitized_words 			#return list
      
def separate_and_sort(clean_list_of_words):	#function for seperating strings from integers and sorting them after seperation, when given a sanitized list of strings.
  alphaWords = []				#creates a list for holding strings
  numWords = []					#creates a list for holding integers
  placeholder = []				#creates a list that is used for  mapping original placement of strings and integers. 
  for word in clean_list_of_words:		#for every string in sanitized list...
    if word.isalpha():				#if the string has alphabetic characters...
      alphaWords.append(word)			#add it to the list holding strings
      placeholder.append('a')			#create a placeholder indicating that that element was an 'a'lphabetic string in the placeholder list
    elif word.isdigit():			#if the string has numeric characters...
      numWords.append(int(word))		#add it to the list holding integers, first change it to an int, which allows for proper sorting
      placeholder.append('n')			#create a placeholder indicating that the element was a 'n'umeric string 
    else:					#if string has both alphabetic and numeric characters...
      pass      				#do nothing.
  alphaWords = sorted(alphaWords, reverse=True) #sort alphabetic list in reverse order, because we will use a LIFO (last in first out) function for extraction of elements.
  numWords = sorted(numWords, reverse=True)		#sort numeric list in reverse order, for the same reasons as above.
  outputLists = [alphaWords, numWords, placeholder]	#create a list of all three lists, for returning
  return (outputLists)					#return all three lists, which are ready for output.
     
def outputer(outputLists, outputfile):			#function for outputting sorted lists, into the output file
  try:
    with open(outputfile, 'w') as f:			#open outputfile
      for items in outputLists[2]:			#for items in the mapping list called 'placeholder'
	if items == 'a':				#if the item was originally an alphabetic string...
	  f.write(outputLists[0].pop())		#place sorted alphabetic string in that place
	  f.write(' ')					#place a space character after that string
	elif items == 'n':				#if the item was originally a numeric string...
	  f.write(str(outputLists[1].pop()))		#convert the integer into a string and place the sorted numeric string in that place
	  f.write(' ')					#place a space character after that string
	else:						#if our mapping list contaings something other than 'a' or 'n' 
	  print("Error! in outputer")			#Alert user of error
      f.write('\n')
  except IOError as ioerr:				#catch if an error occours when trying to open the output file...
    print("File error: " + str(ioerr))			#Alert the user of error
    return(None)					
    raise SystemExit(1)					#exit if cannot create output file
  finally:
    f.close()						#close the output file

def main():						#main function
  if len(sys.argv) != 3:				#check if program is being called properly
    sys.stderr.write("Usage : ./listSorting.py <path-and-name-of-input-file> <path-to-output-file>\n Output file will be called 'result.txt'\n") #if not tell user how to properly call program and...
    raise SystemExit(1)					#exit
  inputfile = sys.argv[1]				#otherwise get the name of the input file
  outputfile = sys.argv[2]+ "/result.txt"				#get the name of the ouput file
  try:							
    for rawInput in open(inputfile):			#for every line in the inputfile...
      cleanDataList = split_and_sanitize(rawInput)	# split it into strings and sanitize the strings of special characters, returning a list of clean strings
      listsforOutput = separate_and_sort(cleanDataList)	#Once santized, seperate into two lists, strings and ingtegers, sort each accordingly. use a 3rd list to keep track of original placement.
      outputer(listsforOutput, outputfile)			#Place sorted, sanitized, strings and integers, in proper place, in the output file
  except IOError as ioerr:					#catch if an error occurs when attempting to open inputfile
    print("File error: " + str(ioerr))				#Alert user of the error
    raise SystemExit(1)						#Exit program

  
if __name__ == '__main__':
  main()
    
