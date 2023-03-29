from functions import *

#Modes: 1 ... Data plot with slider
#       2 ... Histogram
#       3 ... Clustered data plot with slider
#       4 ... Histogram of clustered data
#       5 ... Event hits

mode = 5

#path="C:\\Users\\domin\\Desktop\\Dataset"
#path="C:\\Users\\domin\\OneDrive\\Desktop\\Dataset 1\\"
#filename="first_try_"
setsize=100
#datatype=".txt"

path="C:\\Users\\domin\\OneDrive\\Desktop\\Dataset 2\\"
filename = "Pixel Output Test 2 ASCII first 10000 hits"
datatype=".t3pa"

analysis(mode, path, filename, setsize, datatype)