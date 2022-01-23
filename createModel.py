import filterData
import Model
import sys

numData = 100000
numTest = 20000
if len(sys.argv)==1:
	print("Default numData and numTest will be used")
	print("numData = "+str(numData))
	print("numTest = "+str(numTest))
else:
    try:
    	numData = int(sys.argv[1])
    	numTest = int(sys.argv[2])
    except:
        numData = 100000
        numTest = 20000        
print("Filtering data")

NameSing, NameCom, surnames = filterData.DataFilter()#Filters data

print("Creating model")

Model.createModel(numData, numTest, NameSing, NameCom, surnames)#Create model
