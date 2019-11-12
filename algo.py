from itertools import combinations 
#itertools.combinations(input,size) returns size length subsequences of elements from the input iterable
def maxsize_pal_subStrings(s):
    l=[]
    for i in range(len(s)):
        for j in combinations(s,len(s)-i):
            if ''.join(j)==(''.join(j))[::-1]:    #add to the sorted list only the palindrome words
                l+=[''.join(j)]
    
    return len(l[0])    #return the lenght of the sorted list's first value
      
s=input()
print((maxsize_pal_subStrings(s)))

