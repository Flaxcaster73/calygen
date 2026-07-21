# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:08:20 2021

Project: Secure password generator

Update 310123: There was a problem with the 'input' command, which
was solved as soon as Spyder was updated to version 5.3.3

@author: Juan Manuel

--------------------------------------------------------------------
NOTA: este archivo es el algoritmo ORIGINAL, sin ningún cambio en la
lógica de generación. Lo único que se modificó fue envolverlo en una
función (en vez de usar input()/print()), porque un servidor web no
tiene una terminal donde escribir respuestas a mano. Las listas de
caracteres y el uso de numpy.random siguen siendo exactamente los
mismos que en el script original.
--------------------------------------------------------------------
"""

import numpy as np

""" Characters being included into the algorithm """
A1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
      'P','Q','R','S','T','U','V','W','X','Y','Z','/','0','1','2',
      '3','4','5','6','7','8','9','+','a','b','c','d','e','f','g',
      'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
      'w','x','y','z','-']
A2 = ['!','$','%','&','(',')','?','_','[',']','{','}',':','@','#',
      '*','<','>']


def generar_password(incluir_especiales=True, nn=18):
    """
    Versión "función" del script original.

    Antes:
        QQ = input('Include special characters...')
        print(s)

    Ahora:
        incluir_especiales (True/False) reemplaza al input()
        return s               reemplaza al print()

    El resto (las listas A1/A2, y la selección con np.random.randint)
    es idéntico al código original.
    """
    if incluir_especiales:
        AA = A1 + A2
    else:
        AA = A1

    List_A = AA
    bb = len(List_A)

    Indices = np.random.randint(0, bb, nn)

    s = ""
    for Index in Indices:
        s = s + List_A[Index]

    return s


# Esto permite que el archivo se siga pudiendo correr solo, tal como
# lo usaba antes (con input() y print()), sin afectar cómo Flask lo usa.
if __name__ == "__main__":
    QQ = input('Include special characters: @,#,$,etc. [y/n]:  ')
    resultado = generar_password(incluir_especiales=(QQ == 'y'))
    print(resultado)
