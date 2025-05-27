Editor: WestameYHL
Update time: 2025/05/27

程序结构
=====================================
主执行文件：mainfunc_xxxx.py
A. 基本程序架构，单次计算
B. for p in i_power 改变 power，计算不同power下的loss
C. for dp in i_dp_list1 改变断点的位置，计算power，看是否能检测出断点
D. 改变外力的大小，看拟合结果会不会变

包含程序效率检测的装饰器，用于规划运算顺序和输出端

四大主程序（Kings）
1. PMK ：实例化模型，整个计算的核心对象，存储每一个分段的各种物理、数学参数，决定每个单元计算的法则和精度
2. Generator ： 利用PMK对象生成计算KKT矩阵，并进行数学求解
3. Objects ： 定义基本计算单元（节点、切片、点对、连接）
3. INP ：输入端，添加约束、连接等条件，模块化装配模型


工具包（tools）
1. loss_func  ： 损伤计算端接口，可以定义多种损伤计算法则
     1.1 EarthMovingCalculator.py  ： 计算EMD的代码
2. LocalPlot  ： 作图输出端接口，适应多种自定义绘图函数
3. LoggingPMK. ： 日志输出端接口，可以将命令行的东西输出到txt
4. DataLoader ：从文件读入数据并存到变量里面（mat，csv，txt）
5. ParticalTopo ：拓扑损伤
6. FxZeros ：二分法函数零点计算框架，用于方便的计算Tikhonov正则项


配置文件（settings）
config.txt ：存放模型基本参数，设定数据读入位置
input_data2pxy.py ：手动计算 p_xy 的subroutine插件
plot_setting.py ：设置绘图参数的插件
custom_power.py ：手动设定每个计算单元的模型参数的插件


源数据集（data）
存放各种数据文件
