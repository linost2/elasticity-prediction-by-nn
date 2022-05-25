# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:43:24 2022
该代码拆解化学式便于填充输入序列以及相对原子质量
@author: Youlin Zhu
"""

#%%
#Step No.1 归一化化学式名称 Na2CO3--> NaNaCOOO 


# -*- coding: UTF-8 -*-
class Solution(object):
    def countOfAtoms(self, formula):
 
        stack = list()
        # 第一步将每个元素、数字、括号独立出来，也就是说有的元素有两个字母组成，有的数字是10以上的
        # 因此要把他们组合
        i = 0
        n = len(formula)
        while i < n:
            if formula[i].isalpha():
                if formula[i].islower():
                    c = stack.pop()
                    c = c + formula[i]
                    stack.append(c)
                else:
                    stack.append(formula[i])
                i += 1
            elif formula[i] == '(':
                stack.append(formula[i])
                i += 1
 
            elif formula[i] == ')':
                stack.append(formula[i])
                i += 1
            else:
                num_str = formula[i]
                i += 1
                while i < n and formula[i].isdigit():
                    num_str += formula[i]
                    i += 1
                stack.append(num_str)
        # 组合结果如下
        # print stack
        # ['K', '4', '(', 'O', 'N', '(', 'S', 'O', '3', ')', '2', ')', '2']
 
        # 第二步 有的元素只有一个，因此要把1补齐
        i = 0
        m = len(stack)-1
        tmp_stack = list()
        for i in range(m):
            tmp_stack.append(stack[i])
            if stack[i].isalpha():
                if not stack[i+1].isdigit():
                    tmp_stack.append("1")
 
        tmp_stack.append(stack[m])
        if stack[m].isalpha():
            tmp_stack.append("1")
 
        stack = tmp_stack
        # 补齐结果如下
        # print stack
        # ['K', '4', '(', 'O', '1', 'N', '1', '(', 'S', '1', 'O', '3', ')', '2', ')', '2']
 
        # 第三步，开始遍历，进行计算，每次遇到一个“）”都往回找“（”，把括号外的数字乘进去，并组合元素和数字
        stack2 = list()
        i = 0
        l = len(stack)
        while i < l:
            if stack[i].isalpha():
                stack2.append([stack[i],stack[i+1]])
                i += 2
            elif stack[i] == '(':
                stack2.append(stack[i])
                i += 1
            elif stack[i] == ')':
                num = int(stack[i+1])
                tmp = list()
                c = stack2.pop()
                while i > 0 and c != '(':
                    c1 = [c[0], str(int(c[1]) * num)]
                    tmp.append(c1)
                    c = stack2.pop()
                stack2.extend(tmp)
                i += 2
 
        # print stack2
        # [['K', '4'], ['S', '4'], ['O', '12'], ['N', '2'], ['O', '2']]
 
        # 第四步，计算基本完成，将结果中重复元素合并，
        result_dict = {}
        for i in stack2:
            if i[0] in result_dict:
                count = result_dict[i[0]] + int(i[1])
                result_dict[i[0]] = count
            else:
                result_dict[i[0]] = int(i[1])
        result = ""
        sor = sorted(result_dict)
        for key in sor:
            if result_dict[key] == 1:
                result += key
            else:
                result += str(key)+str(result_dict[key])
 
        #print(result)
        # K4N2O14S4
        return stack2
