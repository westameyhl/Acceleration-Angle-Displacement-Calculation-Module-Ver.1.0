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
    
    dp_list = np.arange(0.5,6.5-0.4, 0.1).tolist()
    
    loss_list = []
    for dp in dp_list:
        InPuT.select_pxy(scen = 8, row = 6)

        InPuT.auto_modifier("plastic_hinge",dp)
        # ---------------------------------------------
        # validation
        nums = [0,8]
        InPuT.seperate(kill = nums)
        # ---------------------------------------------
        # establish model
        PMKkt = kgpk.ModelChains(InPuT)
        PMKkt.establish_model()
        PMKkt.purge(adj = "max") # opt mode for power: Tikhnov
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
    import matplotlib.pyplot as plt
    xx,yy = dp_list,loss_list
    xx_topo = [0.25,0.75,1.25,2.5,2.75,3.25,4,4,5.25,5.75,6.25]
    plt_list = ["MAE", "MSE", "EMD"]
    # 建立x轴
    plotter = tllp.MultiAxisPlotter(xx)
    for i, mark in enumerate(plt_list):
        yy = []    # 计算yy
        for j in range(len(xx)):
            yy.append(loss_list[j][i])
        yy = tlpt.partiTopo(xx_topo,xx, yy)
        plotter.plot(yy, l_y=mark,centre=False,ylabel_shift = 0.5)  # 画xx-yy
    plotter.show()
# =============================================================================
#     import settings.plot_setting as stps
#     stps.set_b()
# =============================================================================


    # save local variables
    return locals()


if __name__ == "__main__":
    global_vars = main()
    globals().update(global_vars)  # 将返回的局部变量合并到全局作用域

