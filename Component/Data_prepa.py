import numpy as np
import pickle
import formula

#读取并存储数据
D_formula = np.load("dataset_v1.2_1_formula.npy",allow_pickle=True)
D_elas_matrix = np.load("dataset_v1.2_1_els.npy",allow_pickle=True)

#定义元素序列及对应原子质量

periodic_table = ('H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
                  'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 
                  'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 
                  'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 
                  'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 
                  'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm','Md', 'No', 'Lr',
                  'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og', 'Uue')


#%%输入及输出数据准备、输入数据归一化
Matrix_input = []
Matrix_output = []


for num in range(len(D_formula)):
    mark = 0
    mark_o = 0
    a = formula.Solution()
    array_individual_input = np.zeros((len(periodic_table)))
    component = a.countOfAtoms(D_formula[num][0]["pretty_formula"])


    for i in range(len(component)):
         array_individual_input[periodic_table.index(component[i][0])] += eval(component[i][1])
         array_individual_input /= array_individual_input.sum(axis = 0) 
         
    Matrix_input.append(np.around(array_individual_input, decimals=4))
    array_individual_output = np.concatenate([D_elas_matrix[num][i][i:6] for i in range(6)],axis=0)
    
    Matrix_output.append(array_individual_output) 




#保存为模型读取文件           
with open("Matrix_input.pkl", mode="wb") as opened_file:
    pickle.dump(Matrix_input, opened_file)
with open("Matrix_output.pkl", mode="wb") as opened_file:
    pickle.dump(Matrix_output, opened_file)
    