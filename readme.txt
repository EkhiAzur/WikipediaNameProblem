This is a code to make a model and use it to split names into name and surname.

1) Create the model

To create the model, we have to execute createModel.py. It has 2 optional parameters, the size of the train database
and the size of the test database. Default values are, 100000 and 20000.

In order to create the model, there are 2 files (Names.txt and Surnames.txt) that include the names
and surnames that will be used to create databases. It is possible to edit them to include different names and surnames.

First of all, createModel will read both files and it will filter and classify them into 3 list, single word names,
compound names and surnames. Then, using that list, some names will be created randomly to use them as train or test. 
Finally, those databases will be used to make and test the model.

2) Make prediction

To make the prediction, predict.py will be used. The name will give it as parameter, for example: python predict.py Jose Luis Sanchez
using the model, the script will separate the given name into name and surname. ';' is used to separate.

To make predictions reading the names from a file, you only need to pass the file name as a parameter. 
