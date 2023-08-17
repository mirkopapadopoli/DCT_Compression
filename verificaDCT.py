# Importare le librerie
import cv2 
import numpy as np

# Matrice di verifica
matrixTest= np.array([
    [231, 32, 233, 161, 24, 71, 140, 245],
    [247, 40, 248, 245, 124, 204, 36, 107],
    [234, 202, 245, 167, 9, 217, 239, 173],
    [193, 190, 100, 167, 43, 180, 8, 70],
    [11, 24, 210, 177, 81, 243, 8, 112],
    [97, 195, 203, 47, 125, 114, 165, 181],
    [193, 70, 174, 167, 41, 30, 127, 245],
    [87, 149, 57, 192, 65, 129, 178, 228]
], dtype=np.float32)

# Applica la DCT2 sulla matrice
dct_matrixTest = cv2.dct(matrixTest)

# Stampa la matrice DCT2 risultante
print("Matrice DCT2:")
print(dct_matrixTest)


matrixVerify1R = np.array([
    [231, 32, 233, 161, 24, 71, 140, 245]
], dtype = np.float32)

# Applica la DCT sulla riga
dct_matrix1R = cv2.dct(matrixVerify1R)
# Stampare la riga DCT risultate
print ("Riga DCT2:")
print (dct_matrix1R)
