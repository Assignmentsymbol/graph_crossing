import numpy as np
import matplotlib.pyplot as plt

# 生成数据
x = np.linspace(0, 10, 50)
y = np.sin(x) + 0.2 * np.random.randn(50)  # 加上少量噪声

# 绘制原始数据
plt.scatter(x, y, color='blue', label="Data Points")

# 使用二次多项式进行拟合
coefficients = np.polyfit(x, y, 2)  # 选择二次拟合
polynomial = np.poly1d(coefficients)

# 绘制拟合曲线
x_fit = np.linspace(0, 10, 100)
y_fit = polynomial(x_fit)
plt.plot(x_fit, y_fit, color='red', label="Fitted Curve")

# 添加标题和标签
plt.title("Sine Wave with Noise and Curve Fitting")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()

# 显示图形
plt.show()
# 生成数据
x = np.linspace(0, 5, 50)
y = np.exp(-x) + 0.1 * np.random.randn(50)  # 加上少量噪声

# 绘制原始数据
plt.scatter(x, y, color='blue', label="Data Points")

# 使用指数函数拟合数据
def exp_fit(x, a, b, c):
    return a * np.exp(b * x) + c

from scipy.optimize import curve_fit
params, _ = curve_fit(exp_fit, x, y, p0=(1, -1, 0))  # 初始猜测 (1, -1, 0)

# 绘制拟合曲线
y_fit = exp_fit(x, *params)
plt.plot(x, y_fit, color='red', label="Fitted Curve")

# 添加标题和标签
plt.title("Exponential Decay with Curve Fitting")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()

# 显示图形
plt.show()
# 生成数据
x = np.linspace(-5, 5, 50)
y = x**2 + 2 * x + 1 + 0.5 * np.random.randn(50)  # 加上少量噪声

# 绘制原始数据
plt.scatter(x, y, color='blue', label="Data Points")

# 使用二次多项式进行拟合
coefficients = np.polyfit(x, y, 2)  # 选择二次拟合
polynomial = np.poly1d(coefficients)

# 绘制拟合曲线
x_fit = np.linspace(-5, 5, 100)
y_fit = polynomial(x_fit)
plt.plot(x_fit, y_fit, color='red', label="Fitted Curve")

# 添加标题和标签
plt.title("Parabolic Data with Curve Fitting")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()

# 显示图形
plt.show()
