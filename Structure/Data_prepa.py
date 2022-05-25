import numpy as np
import pickle
import formula

#读取并存储数据
D_formula = np.load("dataset_v1.2_1_formula.npy",allow_pickle=True)
D_elas_matrix = np.load("dataset_v1.2_1_els.npy",allow_pickle=True)
D_space = np.load("dataset_v1.2_1_spacegroup.npy",allow_pickle=True)

#定义元素序列及对应原子质量
Periodic_table = {'H':1.008, 'He':4.003, 'Li':6.941, 'Be':9.012, 'B':10.81, 'C':12.01, 'N':14.01, 'O':16, 'F':19, 'Ne':20.18, 'Na':22.99, 'Mg':24.41, 'Al':26.98, 'Si':28.09, 'P':30.97, 'S':32.06, 'Cl':35.45, 'Ar':39.95,
      
                  'K':39.10, 'Ca':40.08, 'Sc':44.96, 'Ti':47.87, 'V':50.94, 'Cr':52.00, 'Mn':54.94, 'Fe':55.85, 'Co':58.93, 'Ni':58.69, 'Cu':63.55, 'Zn':65.39, 'Ga':69.72, 'Ge':72.64, 'As':74.92, 'Se':78.96, 'Br':79.90,

                  'Kr':83.80, 'Rb':85.47, 'Sr':87.62, 'Y':88.91, 'Zr':91.22, 'Nb':92.91, 'Mo':95.96, 'Tc':98, 'Ru':101.1, 'Rh':102.9, 'Pd':106.4, 'Ag':107.9, 'Cd':112.4, 'In':114.8, 'Sn':118.7, 'Sb':121.8, 'Te':127.6,

                  'I':126.9, 'Xe':131.3, 'Cs':133, 'Ba':137.3, 'La':139, 'Ce':140, 'Pr':141, 'Nd':144, 'Pm':145, 'Sm':150.5, 'Eu':152, 'Gd':157, 'Tb':159, 'Dy':162.5, 'Ho':165, 'Er':167, 'Tm':169,
                  
                  'Yb':173, 'Lu':175, 'Hf':178.5, 'Ta':181, 'W':184, 'Re':186, 'Os':190, 'Ir':192, 'Pt':195, 'Au':197, 'Hg':200.6, 'Tl':204.5, 'Pb':207, 'Bi':209, 'Po':209, 'At':210, 'Rn':222,
                  
                  'Fr':223, 'Ra':226, 'Ac':227, 'Th':232, 'Pa':231, 'U':238, 'Np':237, 'Pu':244, 'Am':243, 'Cm':247, 'Bk':247, 'Cf':251, 'Es':252, 'Fm':257,'Md':258, 'No':259, 'Lr':260,
                  
                  'Rf':261, 'Db':262, 'Sg':263, 'Bh':264, 'Hs':265, 'Mt':266, 'Ds':269, 'Rg':272, 'Cn':277, 'Nh':286, 'Fl':289, 'Mc':289, 'Lv':293, 'Ts':294, 'Og':294, 'Uue':295}

periodic_table = ('H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
                  'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 
                  'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 
                  'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 
                  'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 
                  'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm','Md', 'No', 'Lr',
                  'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og', 'Uue')

#定义点群及晶系分类
Pointgroup = {'1':1, "-1":2, "2":3, "m":4, "2/m":5, "222":6, "mm2":7, "mmm":8, "4":9, "-4":10, "4/m":11, "422":12, "4mm":13, "-42m":14, "4/mmm":15, "3":16,"-3":17, "32":18, "3m":19, "-3m":20,
              '6':21, '-6':22, "6/m":23, "622":24, "6mm":25, "-6m2":26, "6/mmm":27, "23":28, "m-3":29, "432":30, "-43m":31, "m-3m":32}

Crystal_system = {"triclinic":1, "monoclinic":2, "orthorhombic":3,"tetragonal":4,"trigonal":5,"hexagonal":6,"cubic":7}
#%%输入及输出数据准备



Matrix_input = []
Matrix_output = []
initialize_list = []

for num in range(len(D_formula)):
    
    a = formula.Solution()
    array_individual_input = np.zeros(len(periodic_table)+3)
    component = a.countOfAtoms(D_formula[num][0]["pretty_formula"])

    for i in range(len(component)):
    
        array_individual_input[periodic_table.index(component[i][0])] += eval(component[i][1])
         
         
        array_individual_input[-3] += Periodic_table[component[i][0]]*eval(component[i][1])
    array_individual_input[:len(Periodic_table)] /= array_individual_input[:len(Periodic_table)].sum(axis = 0)     
    
    if D_space[num]:
    
        initialize_list.append(array_individual_input[0])
        array_individual_input[-2] = Crystal_system[D_space[num][0]["spacegroup"]["crystal_system"]]
        array_individual_input[-1] = Pointgroup[D_space[num][0]["spacegroup"]["point_group"]]
        
        Matrix_input.append(np.around(array_individual_input, decimals=4))
        array_individual_output = np.concatenate([D_elas_matrix[num][i][i:6] for i in range(6)],axis=0)
       # array_individual_output = D_elas_matrix[num][0][:3]
        Matrix_output.append(array_individual_output) 
        

    
         #array_individual_input /= array_individual_input.sum(axis = 0) 
    
#%%
#输入数据归一化[0,1]区间
for i in range(len(Matrix_input)):
    
    Matrix_input[i][-3] = np.around((Matrix_input[i][-3]-4.003)/(2993.2-4.003),decimals=4)
    Matrix_input[i][-2] = np.around((Matrix_input[i][-2]-1)/(7-1),decimals=4)
    Matrix_input[i][-1] = np.around((Matrix_input[i][-1]-1)/(32-1),decimals=4)
    


#%%
#保存为模型读取文件
            
with open("Matrix_input.pkl", mode="wb") as opened_file:
    pickle.dump(Matrix_input, opened_file)
with open("Matrix_output.pkl", mode="wb") as opened_file:
    pickle.dump(Matrix_output, opened_file)
    