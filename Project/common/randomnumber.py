import module
from common import generaterandom
def randomnumber(n,key):
    #Function to generate a list of random numbers
    l=[]
    i=0
    while i<=n:
         curr_key=generaterandom.generaterandom(key)
         if curr_key not in l:
            l.append(curr_key)
            key=curr_key
         i+=1
            


    return l

