
"""
在这里定义绘图参数
使用 matplotlib.pyplot 库函数

"""

import matplotlib.pyplot as plt


def set_a(setlim=False, *args, **kwargs):
    plt.rcParams.update({
        'font.size': 12, 
        'lines.linewidth': 2, 
        'font.family': 'Times New Roman'
        })
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("L curve")
    #plt.legend()

    if setlim:
        plt.xlim([0,1])
        plt.ylim([0,1])

def set_b(setlim=False, *args, **kwargs):
    plt.rcParams.update({
        'font.size': 12, 
        'lines.linewidth': 2, 
        'font.family': 'Times New Roman'
        })
    plt.xlabel("Location (m)")
    plt.ylabel(" ")
    plt.title("Minimized Cost")
    #plt.legend()

    if setlim:
        plt.xlim([0,1])
        plt.ylim([0,1])
        