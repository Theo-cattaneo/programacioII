m=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
s=0
mul=1
sc=0
mc=1

for i in range(4):
    for x in range(4):
        if(i==x):
            s=s+m[i][x]
            mul=mul*m[i][x]
        elif(x==len(m)-1-i):
            sc=sc+m[i][x]
            mc=mc*m[i][x]
            
print("la suma principal de la matris es: ",s)
print("la multiplicacion principal de la matris es: ",mul)
print("la suma contraria de la matris es: ",sc)
print("la multiplicacion contraria de la matris es: ",mc)