b1000=0
b200=0
ms=0
sobra=0
sobra2=0

print("ingrese cuanto dinero quiere sacar del cajero")
ms=int(input())

b1000=ms//1000
sobra=ms%1000

b200=sobra//200

sobra2=sobra%200

print("la cantidad de billetes de mil que se entregan son: ",b1000)
print("la cantidad de billetes de doscientos que se entresa son: ",b200)
print("lo que no se puede entregar es: ",sobra2)

