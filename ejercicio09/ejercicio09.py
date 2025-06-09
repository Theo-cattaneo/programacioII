iva1=1.21
iva2=0
p=0
op=""
s1=0
s2=0
div=0
div2=0

p=int(input("ingrese el precion de la compra:"))

print("ingrese iva1 para sumar el 21% al preco o iva2 para que el usuario ingrese el iva que el quiera")
op=input()

if op=="iva1":
    div=p*iva1
    print("El monton con iva esde: ",div)
    
else:
    iva2=int(input("ingrese cuanto quiere que sea su iva:"))
    iva2=iva2/100+1
    div2=p*iva2
    print("El monton con iva esde: ",div2,"%")
    
