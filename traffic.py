
import numpy as np
import random
rows=8
columns=8
n_bits=rows*columns
total=n_bits*n_bits-n_bits
payloads=3
test=np.ones([n_bits,n_bits-1])

"""
test= [[1 ,1, 1, 1 ,1 ,0 ,1, 1, 1, 1,1, 1, 1, 1 ,0, 1],
 [1 ,1 ,1, 1, 1, 1, 1, 0, 1, 1 ,1 ,1, 1, 1, 1, 1],
 [1 ,1, 1, 0 ,1 ,0 ,0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
 [0 ,1 ,1 ,1 ,1, 1 ,0 ,0 ,0 ,0 ,1 ,1, 0, 1, 1, 1],
 [1 ,1, 0 ,1, 1 ,0 ,0 ,0 ,1 ,1 ,1, 1, 1, 0, 1, 1],
 [1, 1, 1, 0, 1, 1, 1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,0],
 [0 ,1 ,1, 1 ,1 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,0, 1 ,1],
 [0 ,1 ,1 ,1 ,1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
 [0 ,1, 1 ,0, 1 ,1 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,1 ,1],
 [0 ,0, 0, 1, 1 ,1, 1, 1, 1 ,1 ,0 ,1 ,0 ,1 ,1 ,1],
 [0 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,0 ,1],
 [0 ,1 ,1 ,1 ,1 ,1 ,1, 0, 1, 0 ,1 ,0 ,0, 1, 0 ,1],
 [1 ,0, 0, 1, 0 ,0 ,0, 0,1, 1, 0 ,0 ,0 ,1 ,1 ,0],
 [1 ,0, 0 ,1 ,1 ,1 ,0, 1 ,1, 1, 1, 1, 0, 1, 1, 0],
 [0, 1, 1, 1 ,1 ,0, 1 ,0 ,1,0, 0, 1 ,0 ,0 ,0 ,1]]
 """
print(test)
lst_s = list(range(0, n_bits))
lst_d = list(range(0, n_bits-1))
#random.shuffle(lst_s)
#random.shuffle(lst_d)
print(lst_s)
print(lst_d)
combos=[]
f=open("traffic"+str(rows)+"x"+str(columns)+".txt","w")
for i in lst_s:
    for j in lst_d:
        combos.append([i,j])
random.shuffle(combos)
print(combos)
print(len(combos))

for k in combos:
    j=k[1]
    i=k[0]
    if (j >= i):
        d = j + 1
    else:
        d = j
    if (test[i][j] >= 1):
        lbs = i // columns
        source_l = bin(lbs).replace('0b', '')
        x = source_l[::-1]  # this reverses an array
        while len(x) < 4:
            x += '0'
        source_l = x[::-1]
        ubs = i % columns
        source_u = bin(ubs).replace('0b', '')
        x = source_u[::-1]  # this reverses an array
        while len(x) < 4:
            x += '0'
        source_u = x[::-1]
        source = str(source_l) + str(source_u)
        ######################
        lbd = d // columns
        dest_l = bin(lbd).replace('0b', '')
        x = dest_l[::-1]  # this reverses an array
        while len(x) < 4:
            x += '0'
        dest_l = x[::-1]
        ubd = d % columns
        dest_u = bin(ubd).replace('0b', '')
        x = dest_u[::-1]  # this reverses an array
        while len(x) < 4:
            x += '0'
        dest_u = x[::-1]
        dest = str(dest_l) + str(dest_u)

        rand_ls = np.random.random_integers(0, 1, size=(13))
        rand_ls = str(rand_ls).replace(" ", "")
        rand_ls = str(rand_ls).replace("[", "")
        rand_ls = str(rand_ls).replace("]", "")
        h_f = str(source) + str(dest)
        f.write(h_f)
        f.write("\n")


f.close()

