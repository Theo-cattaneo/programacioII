import random
num=0
numA=random.randint(1,20)
cont=6

print("adivina el numero secreto")

print("ingresar un numero")

while (cont!=0):
    num=int(input())
    
    if (num==numA):
        print("felicidades adivinaste el numero")
        break    
    if num<numA:
        
         print("el numero a adivinar es mayor")
    else:
        print("el numero a adivinar es menor")
        
    cont=cont-1
   
if cont==0:   
    print("lo siento perdiste el numero era: ",numA)

        
