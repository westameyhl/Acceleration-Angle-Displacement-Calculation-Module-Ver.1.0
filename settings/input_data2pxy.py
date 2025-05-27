
"""
在这里定义数据切片
InpObj.data 是读取的原数据， 输出p_xy
格式： 二维数组[[x,y],....]

"""

#globals().clear()
import numpy as np


def get_p_xy(x, *args, **kwargs):
    #p_xy = np.array([x])
    # ===================== for edit =====================
    i_row = kwargs.get("row")
    i_scen = kwargs.get("scen")
    
    p_x = [0.25,0.75,1.25,2.75,3.25,4,5.25,5.75,6.25]
    p_y_g = x[i_scen][1]
    p_y = p_y_g[i_row][1:] - p_y_g[0][1:] 
    
    return p_x, list(p_y)


if __name__ =="__main__":
    check = get_p_xy(123)