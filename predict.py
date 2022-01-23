import sys, pickle, unidecode
import numpy as np

#This function makes a float array representation of the given word. Each element of the array is the
#normalized ascii number of the character. For example, cat = [0.0, 9.9, 9.7, 1.16, 0.0].
#Max is the length of the array, if the word is longer than max, the first max character will be used to encode the word.
def wordEncode(word, Max):
    if len(word)>Max:
        word=word[:Max]
    mid=int(len(word)/2)
    array=[0.]*(int(Max/2)-mid)+[charToFloat(i) for i in word]
    array+=[0.]*(Max-len(array))
    return array


#This function encodes into a normalized float the given word or character. 
def charToFloat(word):
    normFloat=""
    for elem in word:
        normFloat+=str(ord(elem))
    if len(normFloat)<2:
        return 1
    return float(normFloat[0]+"."+normFloat[1:])

#This function encodes each element of the list using 3 values. The return of wordEncode concatenates with
# the length of string and the return of charToFloat
def encodeString(arg):
    Max = 5
    array=[]
    for elem in arg:
        array+=wordEncode(elem, Max)+[len(elem)]+[charToFloat(elem)]
    return array

#This function simplifies the list. If a word is in the black list, it will be concatenated with the following word.
#Return: simplified data and a list of numbers to save the concatenations
#For example: Alvarez de Eulate -> Alvarez deEulate, [1, 2;3]
def simplifyData(arg):
    blackList = ["del","de","la","el","los","i","y"]
    numList = [str(i) for i in range(len(arg))]
    result = arg.copy()
    for i in reversed(range(len(arg)-1)):
        if arg[i].lower() in blackList:
            result[i:i+2] = [''.join(result[i:i+2])]
            numList[i:i+2] = [';'.join(numList[i:i+2])]

    return result, numList

#This function is the opposite of simplifyData, using the list of numbers and the args of the beginning
#creates the result without simplifications.
#For example: numList=[1,2,/,3;4] args=["Jose","Angeles","de","Alvarez"] ->  "Jose Angeles ; de Alvarez"
def numToAnswer(numList, args):
    result = ""
    for elem in numList:
        if "/" in elem:
            result+="; "
        elif ";" not in elem:
            result+=args[int(elem)]+" "
        else:
            indexList = elem.split(";")
            for elem2 in indexList:
                result+=args[int(elem2)]+" "
    return result

def filepredict(filename):
    try:
        f = open(filename,"r")#Open the file
    except:
        print("Introduce a file name")#If the file does not exist
        return 1
    f2 = open("Results.txt",'w')#Open the results file
    nameList = list(f)#Read names
    model= pickle.load(open("Model.sav", 'rb'))#Load the model
    for name in nameList:
        nameSplit = name.split(" ")#Split the name into a list
        if "i" in nameSplit:#This is a specific answer for some names
            index = nameSplit.index("i")
            nameSplit.insert(index-1, ";")
            f2.write(' '.join(nameSplit))
            continue
        if "y" in nameSplit:#This is a specific answer for some names
            index = nameSplit.index("y")
            nameSplit.insert(index-1, ";")
            f2.write(' '.join(nameSplit))
            continue
        arg, numList = simplifyData(nameSplit)#Simplify data and get the numList
        standarChars= [unidecode.unidecode(elem) for elem in arg]#Convert characters to unicode
        if len(standarChars)>=4:
            standarChars = standarChars[:3]#If the length is more than 3, take into account just the first 3
        elif len(standarChars)==2:#If the length is 2, insert ';' between the 2 words
        	nameSplit.insert(1,";")
        	f2.write(' '.join(nameSplit))
        	continue
        encoded = encodeString(standarChars)#Encode words
        result = model.predict(np.array([encoded]))[0]#Make prediction
        numList.insert(result, "/")#Insert '/'
        f2.write(numToAnswer(numList, nameSplit))#Convert the numerical representation into a string and print the result
    print("All names have been processed")


def main():
    if len(sys.argv)==1:
        print("No name was given")
        return 0
    if len(sys.argv)==2:
        filepredict(sys.argv[1])
        return 0
    args = []
    for i in range(1,len(sys.argv)):#Read the arguments and save them to args list
        args+=[sys.argv[i]]
    if "i" in args:
        index = args.index("i")
        args.insert(index-1, ";")
        print(' '.join(args))
        return 0
    if "y" in args:
        index = args.index("y")
        args.insert(index-1, ";")
        print(' '.join(args))
        return 0
    arg, numList = simplifyData(args)#Simplify data and get the numList
    standarChars= [unidecode.unidecode(elem) for elem in arg]#Convert characters to unicode
    if len(standarChars)==3:
        print("Length=3")
    elif len(standarChars)>=4:
        print("Length>=4")
        standarChars = standarChars[:3]#If the length is more than 3, take into account just the first 3
    elif len(standarChars)==2:#If the length is 2, insert ';' between the 2 words
    	args.insert(1,";")
    	print(' '.join(args))
    	return 0
    	
    model= pickle.load(open("Model.sav", 'rb'))#Load the model
    encoded = encodeString(standarChars)#Encode words
    result = model.predict(np.array([encoded]))[0]#Make prediction
    numList.insert(result, "/")#Insert '/'
    print(numToAnswer(numList, args))#Convert the numerical representation into a string and print the result

if __name__ == "__main__":
    main()
