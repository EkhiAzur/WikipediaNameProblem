import re

#This function firstly filters duplicated data and makes 2 lists with single word names and compound names in it.
def DataFilter():
    f=open("Names.txt",'r')#Open the names file and make it a list
    NameList=list(f)
    #Initalize 2 lists
    NameCom=[]
    NameSing=[]
    prog = re.compile("[a-zA-ZáéíóúÁÉÍÓÚ ]+ [a-zA-ZáéíóúÁÉÍÓÚ ]+")#Create the regular expression object
    #For each name, we evaluate it with regular expressions and add it to one of the lists while filtering duplicated names
    for elem in NameList:
        elem.replace("-"," ")
        result = prog.match(elem)
        if result and (not (elem in NameCom)):#If the name is a compound name
            NameCom.append(elem)#Add to NameCom list
        elif (not elem in NameSing):#If the name has only 1 word
            NameSing.append(elem)#Add to NameSing list
    f.close()
    f = open("Surnames.txt",'r')#Open the surnames file
    SurnameList = list(f.readlines())
    surnames = []
    for abizen in SurnameList:#Filters duplicated surnames
        if not (abizen in surnames):
            surnames.append(abizen)
    return NameSing, NameCom, surnames #Return names and surnames

