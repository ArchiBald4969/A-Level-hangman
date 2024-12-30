##################################################################
###creates the dictionary with a set size of ten thousand items###
##################################################################

import pickle
dictionary={}
for i in range(0,10000):
    dictionary[i]=""
print(dictionary)

###saves dictionary to a binary file###
fh=open('HashTbl','wb')
pickle.dump(dictionary,fh)
fh.close()
