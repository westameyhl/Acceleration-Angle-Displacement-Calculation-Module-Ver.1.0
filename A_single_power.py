# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 14:53:55 2025

@author: westa
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import random


import Kings.INP as kgip
import Kings.PMK as kgpk
import Kings.Generator as kggt

import tools.CustomDecorator as tlcd
import tools.LocalPlot as tllp
from tools.Static import Static as tlst





@tlcd.Examinor()
def main():

    current_dir = os.getcwd()
    config = f"{current_dir}\\settings\\config.txt"
    
    
    
    power_mode = ["Tikh","Monte"][0]
    
    if power_mode == "Monte":
        p_st, p_ed = 3, 11
        p_list = np.arange(p_st,p_ed, 1).tolist()
        dl = [0]*(p_ed-p_st)
        InPuT = kgip.InputPluzer(mode = "load",config = config)
        
        for i in range(30):
            num = random.randrange(1, 4)
            nums = random.sample(range(9), num)
            print(nums)
            InPuT.select_pxy(row = 6,scen = 8)
            InPuT.seperate(kill = nums, noise = 0.1)
            
            lost = []
            for p in p_list:
                # 这一坨不用动
                PMKkt = kgpk.ModelChains(InPuT)
                PMKkt.establish_model()
                
                PMKkt.purge(adj = "loop", power=p)
                
                MatrixGen = kggt.MtxGenerator(PMKkt)
                MatrixGen.xbdic()
                MatrixGen.calculate()
                targ = MatrixGen.inv_ac
                PMKkt.repair(targ.flatten().tolist())
                
                loss_type = "mse"
                loss_gen = PMKkt.real_loss(loss_type,PMKkt.model.p_x_test.copy(), PMKkt.model.p_y_test.copy())
                loss_3 = PMKkt.real_loss(loss_type,PMKkt.model.p_x.copy(), PMKkt.model.p_y.copy())
                dloss = loss_gen-loss_3
                aloss = loss_gen+loss_3
                #lost.append([loss_3,loss_gen,dloss,aloss])
                lost.append(aloss)
    
            min_index = tlst.catch_minmax(lost, 4, weight=True)
            for i in min_index:
                dl[i[0]-p_st] += i[2]
            
        PD = tllp.PlotGaussian()
        PD.plot_norm(p_list, dl)
        PD.show()
        
        
    elif power_mode == "Tikh":
        p_st, p_ed = 0.001,0.9
        alph = np.arange(p_st,p_ed, 0.001).tolist()
        #alph = [alph[66]]
        InPuT = kgip.InputPluzer(mode = "load",config = config)
        InPuT.select_pxy(row = 6,scen = 8)
        #InPuT = kgip.InputPluzer(mode = "test")
        nums = [0,8]
        InPuT.seperate(kill = nums)
        
        l1,l2 = [],[]
        for a in alph:

            PMKkt = kgpk.ModelChains(InPuT)
            PMKkt.establish_model()
            PMKkt.purge(adj = "max")
            MatrixGen = kggt.MtxGenerator(PMKkt)
            MatrixGen.xbdic(Tikhnov=a)
            MatrixGen.calculate()
            targ = MatrixGen.inv_ac
            PMKkt.repair(targ.flatten().tolist())
            
            loss_type = "mse"
            loss_fx = PMKkt.real_loss(loss_type,PMKkt.model.p_x.copy(), PMKkt.model.p_y.copy())
            loss_vd = PMKkt.real_loss(loss_type,PMKkt.model.p_x_test.copy(), PMKkt.model.p_y_test.copy())

            l1.append(np.log10(loss_fx))
            l2.append(np.log10(loss_vd))
        
        #plt.plot(l1,l2)
        plt.plot(alph,l1)
        plt.plot(alph,l2)
        min_loss = tlst.catch_equal(l1,l2)

        xx = np.arange(0,PMKkt.model.L+0.01, 0.01).tolist()
        plt_list = ["Disp", "Rot", "Momt", "Shear"]
        plotter = tllp.MultiAxisPlotter(xx)
        for i in range(4):
            yy = PMKkt.field(xx, f"{i-1}")
            plotter.plot(yy, l_y=plt_list[i])
            if i == 1:
                plt.scatter(PMKkt.model.p_x, PMKkt.model.p_y, color='black')
                plt.ylim(-max(PMKkt.model.p_y)*1.1, max(PMKkt.model.p_y)*1.1)
        plotter.show()

        

    # 保存局部变量
    return locals()


if __name__ == "__main__":
    global_vars = main()
    globals().update(global_vars)  # 将返回的局部变量合并到全局作用域

