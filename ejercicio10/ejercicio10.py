num=0

print("ingresa el numero que quieres factorizar")
num=int(input())

def factorial(num):
    contador=0
    for x in range(1,num,1):
        contador=contador+1
        num=num*contador
    return num

print("este es el factorial de tu numero: ",factorial(num))


    
    