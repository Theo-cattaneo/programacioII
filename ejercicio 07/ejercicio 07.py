año=0
mes=0
dia=0

año=int(input("ingrese su año de nacimiento:"))
mes=int(input("ingrese su mes de nacimiento:"))
dia=int(input("ingrese su dia:"))

import datetime

nacimiento=datetime.datetime(año,mes,dia)
actual=datetime.datetime.now()
diferencia=actual-nacimiento
años=diferencia.days//365
meses=(diferencia.days % 365)//30
dias=(diferencia.days %365)%30

print("uste a vivido ",diferencia," dias")
print("usted vivio ",años," años ",meses," meses y ",dias," dias")

