registros = [10, 12, 15, 14, 18, 20, 22] 

ultimos_tres = registros[-3:] 

print(ultimos_tres) 

def es_capicua(lista): 
    for i in range(len(lista) // 2): 
     if lista [i] != lista[-(i+1)]: 

      return False
     return True
lista = [9,12,18,12,9] 

print(es_capicua(lista))