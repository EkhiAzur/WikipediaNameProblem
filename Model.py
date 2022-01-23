import random, unidecode, time, pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

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

#This is the main function to create a Model. The function creates Train and Test databases and they are used to train and test the model.
#Parameters:  
def createModel(numTrain, numTest, NameSing, NameCom, surnames):
    start_time = time.time()
    Max=5
    X_train=np.array([[0]*(3*Max+6)])#Initialize train database
    y_train=np.array([0])
    for i in range(numTrain):
        r=random.randrange(1,3)
        if r==1:#If it is 1 it means that it is from class 1
            #Randomly choose a name of length 1 and 2 surnames to create a complete name
            rand=random.randrange(0,len(NameSing))
            rand2=random.randrange(0,len(surnames))
            rand3=random.randrange(0,len(surnames))
            #Get random name and surnames
            a=unidecode.unidecode(NameSing[rand])
            b=unidecode.unidecode(surnames[rand2])
            b2=unidecode.unidecode(surnames[rand3])
            #Delete blank spaces and apostrophe
            a.replace(" ", "")
            b.replace(" ","")
            b.replace("'", "")
            b2.replace(" ", "")
            b2.replace("'", "")
            #Create variables to represent the complete name
            array = wordEncode(a, Max)+[len(a)]+[charToFloat(a)]+wordEncode(b, Max)+[len(b)]+[charToFloat(b)]+wordEncode(b2, Max)+[len(b2)]+[charToFloat(b2)]
            #Add data to train database
            X_train=np.row_stack((X_train, np.array([array])))
            y_train=np.row_stack((y_train, np.array([1])))
            
        elif r==2:#If it is from class 2
            #Choose randomly a name with length 2 or more and a single surname to create a cosmplete name
            rand=random.randrange(0,len(NameCom))
            rand2=random.randrange(0,len(surnames))
            #Get random name and a surname
            a=unidecode.unidecode(NameCom[rand])
            b=unidecode.unidecode(surnames[rand2])
            #Delete blank spaces and apostrophe and split the compound name
            a0 = a.split(" ")[0]
            a1 = a.split(" ")[1]
            b.replace(" ","")
            b.replace("'", "")
            #Create variables to represent the complete name
            array = wordEncode(a0, Max)+[len(a0)]+[charToFloat(a0)]+wordEncode(a1, Max)+[len(a1)]+[charToFloat(a1)]+wordEncode(b, Max)+[len(b)]+[charToFloat(b)]
            #Add data to train database
            X_train=np.row_stack((X_train, np.array([array])))
            y_train=np.row_stack((y_train, np.array([2])))
            
    #Delete the first values of each training database
    X_train=np.delete(X_train, 0,0)
    y_train=np.delete(y_train, 0)
    
    #Do the same with the test database
    
    X_test=np.array([[0]*(3*Max+6)])#Initialize test database
    y_test=np.array([0])    
    
    for i in range(numTest):
        r=random.randrange(1,3)
        if r==1:#If it is 1 it means that it is from class 1
            #Randomly choose a name of length 1 and 2 surnames to create a complete name
            rand=random.randrange(0,len(NameSing))
            rand2=random.randrange(0,len(surnames))
            rand3=random.randrange(0,len(surnames))
            #Get random name and surnames
            a=unidecode.unidecode(NameSing[rand])
            b=unidecode.unidecode(surnames[rand2])
            b2=unidecode.unidecode(surnames[rand3])
            #Delete blank spaces and apostrophe
            a.replace(" ", "")
            b.replace(" ","")
            b.replace("'", "")
            b2.replace(" ", "")
            b2.replace("'", "")
	        #Create variables to represent the complete name
            array = wordEncode(a, Max)+[len(a)]+[charToFloat(a)]+wordEncode(b, Max)+[len(b)]+[charToFloat(b)]+wordEncode(b2, Max)+[len(b2)]+[charToFloat(b2)]
            #Add data to test database
            X_test=np.row_stack((X_test, np.array([array])))
            y_test=np.row_stack((y_test, np.array([1])))
            
        elif r==2:#If it is from class 2
            #Randomly choose a name with 2 or more length and a surname to create a complete name
            #Get random name and a surname
            rand=random.randrange(0,len(NameCom))
            rand2=random.randrange(0,len(surnames))
            a=unidecode.unidecode(NameCom[rand])
            b=unidecode.unidecode(surnames[rand2])
            #Delete blank spaces and apostrophe and split the compound name
            a0 = a.split(" ")[0]
            a1 = a.split(" ")[1]
            b.replace(" ","")
            b.replace("'", "")
	       #Create variables to represent the complete name
            array = wordEncode(a0, Max)+[len(a0)]+[charToFloat(a0)]+wordEncode(a1, Max)+[len(a1)]+[charToFloat(a1)]+wordEncode(b, Max)+[len(b)]+[charToFloat(b)]
            #Add data to test database

            X_test=np.row_stack((X_test, np.array([array])))

            y_test=np.row_stack((y_test, np.array([2])))
    #Delete the first values of each training database
    X_test=np.delete(X_test, 0,0)
    y_test=np.delete(y_test, 0)
    
    #Create the classifier object
    gnb = RandomForestClassifier(n_estimators=100)
    #Train it with the training database
    gnb.fit(X_train, y_train)
    #Make predictions of the test database
    y_pred = gnb.predict(X_test)
    #Calculate the accuracy
    Gaizki=(y_test != y_pred).sum()
    #Print the accuracy
    print("%d tested, accuracy : %f"
          % (X_test.shape[0], (1-(float(Gaizki))/X_test.shape[0])))
    #Save the model in a file
    pickle.dump(gnb, open("Model.sav", 'wb'))
    elapsed_time = time.time() - start_time
    #Print the time needed
    print("Elapsed time: %0.10f seconds." % elapsed_time)
