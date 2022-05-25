# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:27:17 2022

@author: Ivan
"""

# 通过 Materials Project网站提供的API接口进行材料弹性常数、化学式和结构特征数据提取，依赖pymatgen包。

from pymatgen.ext.matproj import MPRester
import numpy as np

# 主函数，按用户定义id列表进行数据提取，API Key可从Materials Project网站获得。

def main():

    # Personal Materials Project API key, unencrypted.

    USER_API_KEY = '**************'
    
    # Sample selection criteria should be confirmed.
    
    id_list = []
    
    for i in range(0,10000000):
        
        materials_id = 'mp-' + str(i)
        id_list.append(materials_id)
        
    batch_fetch_by_ids(id_list, 'dataset', USER_API_KEY)
        
    return None        
    
# 批量提取函数，遍历输入id列表，提取凸包能量（E above hull）小于等于0结构的刚度矩阵（VASP理论计算结果，如存在）、对应化学式和结构信息。输出另存为三个独立文件。    

def batch_fetch_by_ids(id_list,dataset_name,user_api_key):
    
    formula_list = []
    els_list = []
    spacegroup_list = []
    
    save_count = 0
    
    for materials_id in id_list:
        
        ehull = e_above_hull(materials_id,user_api_key)
        
        if ehull == None:
            
            print('No ehull from '+materials_id+'!')
            
            pass
        
        elif ehull <=0:
            
            formula,els = fetch_els_tensor(materials_id,user_api_key)
            spacegroup = get_space_group(materials_id, user_api_key)
            
            if els == None:
                
                print('No els tensor from '+materials_id+'!')
                
                pass
            
            else:
            
                formula_list.append(formula)
                els_list.append(els)
                spacegroup_list.append(spacegroup)
            
                save_count+=1
                print(materials_id)
            
            # Save data per save_count to avoid data loss, can be modified depend on network.
            
            if save_count == 10:
            
                np.save(dataset_name+'_els',els_list)
                np.save(dataset_name+'_formula',formula_list)
                np.save(dataset_name+'_spacegroup',spacegroup_list)
                save_count=0
            
            else:
                
                pass
            
        else:
            
            print('ehull > 0 for '+materials_id+'!')
            
            pass
    
    return None

# 刚度矩阵及化学式提取函数

def fetch_els_tensor(sample_id,user_api_key):
    
    try:

        with MPRester(user_api_key) as m:
            formula = m.get_data(sample_id,prop='pretty_formula')
            raw_els = m.get_data(sample_id,data_type="vasp",prop='elasticity')
    except:
        
        formula = []
        raw_els = []

    if raw_els == []:
        
        els_tensor = None
        
        print('No elastic tensor data from '+sample_id+'!')
        
    else:

        els_dict = eval(str(raw_els[0]))
    
        if els_dict['elasticity'] == None:
        
            els_tensor = None
            
            print('No elastic tensor data from '+sample_id+'!')
        
        else:
        
            els_tensor = els_dict['elasticity']['elastic_tensor']
    
    return formula,els_tensor

# 凸包能量提取函数

def e_above_hull(sample_id,user_api_key):
    
    try:
    
        with MPRester(user_api_key) as m:
            
            ehull = m.get_data(sample_id,prop='e_above_hull')
        
    except:
            
        print('Cannot fetch ehull data from '+sample_id+'!')
        ehull = []
        
    
    if ehull == []:
        
        ehull_value = None
    
    else:
        
        ehull = eval(str(ehull[0]))
        ehull_value = ehull['e_above_hull']
    
    return ehull_value

# 结构信息提取函数

def get_space_group(sample_id,user_api_key):
    
    try:
    
        with MPRester(user_api_key) as m:
        
            spacegroup = m.get_data(sample_id,prop='spacegroup')
    
    except:
        
        spacegroup=None
        
    return spacegroup


if __name__ == "__main__":
    
    main()


