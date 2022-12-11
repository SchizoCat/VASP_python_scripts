# %%
###09.12.2022 
###Ertugrul Ceylan 
###This script is intented to fix atoms and add Selective Dynamics to a POSCAR file of VASP

### INPUT: 'POSCAR.vasp' ; OUTPUT: 'POSCAR'  

# %%
##Importing necessary libraries
import pymatgen as mg
import numpy as np
import pandas as pd
import linecache as lc
from os import remove
from tabulate import tabulate


# %%
pd.set_option('display.precision', 9)

# %%
##Reading POSCAR.vasp 
with open('POSCAR.vasp') as file:
    lines = np.array(file.readlines())
file.close()


# %%
##Adding Selective Dynamics before 'Cartesian' (if there aren't any) 
i, = np.where(lines == 'Cartesian\n')
i= i[0]
text='Selective Dynamics\n'
lines = np.insert(lines,i,text)
i+=2
with open("positions.txt", mode="w") as file:
    file.write("\n".join(lines[i:]))


# %%
##Fixing atomic positions selectively using Pandas DataFrames
Pos = pd.read_csv('positions.txt',sep='      ',header=None,names=['x','y','z'],engine='python',index_col=False) # sep= 5 spaces
remove('positions.txt')
Pos.head()




# %%
## Determine which atoms are fixed. Selecting atoms below certain coordinate
check='z'
bulkStart=2.3200000 # Fixing threshold 
Pos['Move?'] = Pos[check].apply(lambda x: 'F F F' if x < bulkStart else 'T T T') #F means the atom cannot move along that vector
Pos.head()

# %%
##Writing the new POSCAR
with open('POSCAR', 'w') as filehandle:
    for line in lines[:i]:
        filehandle.writelines(line)
with open('POSCAR', 'a') as filehandle: 
    PosAsString = Pos.to_string(header=False, index=False)
    filehandle.writelines(PosAsString)
filehandle.close()
 


