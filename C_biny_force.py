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
import tools.LoggingPMK as tllg
import tools.FxZeros as tlfz
import tools.ParticalTopo as tlpt

def calculate_kkt(a,**kwargs):
    l1,l2 = [],[]
    if "loss_type" in kwargs:
        loss_type = kwargs["loss_type"]
    else:
        loss_type = "mse"
    # Main KKT calculation
    if "Mat" in kwargs:
        MatrixGen = kwargs["Mat"]
        
    MatrixGen.xbdic(Tikhonov=a)
    MatrixGen.calculate()
    targ = MatrixGen.inv_ac
    MatrixGen.PMKkt.repair(targ.flatten().tolist())
    loss_fx = MatrixGen.PMKkt.real_loss(loss_type,MatrixGen.PMKkt.model.p_x.copy(), MatrixGen.PMKkt.model.p_y.copy())
    loss_vd = MatrixGen.PMKkt.real_loss(loss_type,MatrixGen.PMKkt.model.p_x_test.copy(), MatrixGen.PMKkt.model.p_y_test.copy())
    
    if "Type" not in kwargs:
        # Loss for Tikhnov
        return np.log10(loss_fx) - np.log10(loss_vd)
    else:
        n_xy, n_t = len(MatrixGen.PMKkt.model.p_x), len(MatrixGen.PMKkt.model.p_x_test)
        loss = (np.array(loss_fx)*n_xy + np.array(loss_vd)*n_t) / (n_xy+n_t)
        return np.log10(loss)



@tlcd.Examinor(n=1)
def main():

    config = f"{os.getcwd()}\\settings\\config.txt"
    # load data
    InPuT = kgip.InputPluzer(mode = "load",config = config)
    
    loss_list = []

    InPuT.select_pxy(scen = 8, row = 6)
    
    

    InPuT.auto_modifier("load_stc",2.5)
    InPuT.auto_modifier("load_stc",4)
    # ---------------------------------------------
    # validation
    nums = [0,8]
    InPuT.seperate(kill = nums)
    # ---------------------------------------------
    # establish model
    PMKkt = kgpk.ModelChains(InPuT)
    PMKkt.establish_model()
    PMKkt.purge(adj = "loop",power=4) # opt mode for power: Tikhnov
    MatrixGen = kggt.MtxGenerator(PMKkt)
    
    # =========================================================================
    # =========================== Part 1 ： Optimize ===========================
    # 利用二分法计算零点
    p_st, p_ed = 1e-5, 0.99
    root, iters = tlfz.FxZero.bisection(calculate_kkt, p_st, p_ed, tol=1e-5, Mat=MatrixGen)
    # ==========================================================================
    # =========================== Part 2 : Calculate ===========================
    loss = calculate_kkt(root, Mat=MatrixGen, Type=True, loss_type="all")
    loss_list.append(loss)

    # =========================================================================
    # =========================== Part 3 : Visualize===========================
    # fitting plot
    xx = np.arange(0,PMKkt.model.L+0.01, 0.01).tolist()
    plt_list = ["Disp", "Rot", "Momt", "Shear"]
    y_scale = [1e4,1e4,1e4,1e4]

    plotter = tllp.MultiAxisPlotter(xx)
    for i in range(len(plt_list)):
        yy = PMKkt.field(xx, f"{i-1}")
        plotter.plot(yy, l_y=plt_list[i],scale = y_scale[i])
        if i == 1:
            sc_x = np.array(PMKkt.model.p_x)
            sc_y = np.array(PMKkt.model.p_y)*y_scale[i]
            sc_xt = np.array(PMKkt.model.p_x_test)
            sc_yt = np.array(PMKkt.model.p_y_test)*y_scale[i]   
            plt.scatter(sc_x, sc_y, color='black')
            plt.scatter(sc_xt, sc_yt, color='black')
            plt.ylim(-max(sc_y)*1.1, max(sc_y)*1.1)
    plotter.show(title="Shape Estimation (unit: 1e4)")
    loss_type = "mse"
    loss_fx = PMKkt.real_loss(loss_type,PMKkt.model.p_x.copy(), PMKkt.model.p_y.copy())
    form = f"{2*loss_fx:.2e}".split('e')
    form = f"{form[0]}(e{form[1]})"
    add_mess = "-"*20+ f"\nLoss: Type({loss_type})  ---  Val: {form}\n"

    logger_console = tllg.MultiOutputLogger(log2file=False,print2console=True)
    logger_console.print_chain(PMKkt.Elements)
    logger_console.log5console(add_mess)


    # save local variables
    return locals()


if __name__ == "__main__":
    global_vars = main()
    globals().update(global_vars)  # 将返回的局部变量合并到全局作用域

