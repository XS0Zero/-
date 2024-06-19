import numpy as np
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.figure()
# 使用 plot 函数绘制折线图
plt.plot(x, y)

# 显示图形
plt.show()