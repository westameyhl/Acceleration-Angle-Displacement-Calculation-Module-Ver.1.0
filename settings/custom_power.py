# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 14:28:41 2025

@author: Westame
"""

"""
custom setting of power

"""



def power_limitation(power):

    # ===================== for edit =====================
    up_lim = 5
    dw_lim = 3
    
    power = min(max(power-2,3),5)
    
    return power


if __name__ =="__main__":
    check = power_limitation(6)