e=0
c=0
r=0
cpe=0
 
print("ingrese cuantos caramelos tiene la bolsa")
c=int(input())
 
print("ingrese cuantos alumnos hay")
e=int(input())
 
cpe=c//e

r=c%e
print("cada estudiante recibira: ",cpe," caramelos")

print("y en la bolsa restan: ",r," caramelos")

 
 
 