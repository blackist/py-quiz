import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 中文显示设置 ---
# 方法一：设置全局字体
# 指定一个支持中文的字体，例如 'SimHei' (黑体), 'Microsoft YaHei' (微软雅黑)
# 注意：这些字体需要在您的操作系统中安装
plt.rcParams["font.sans-serif"] = [
    "Heiti SC",
    "PingFang SC",
    "Arial Unicode MS",
]  # 用于显示中文
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# --- 1. 数据准备 ---
# 定义一个波动的函数，并确保其值在 0-9 之间
def fluctuating_function(x):
    # 基础波动 (范围大致在 -5 到 5 之间)
    raw_output = np.sin(x) * 3 + np.cos(x / 2) * 2

    # --- 增加中间波动范围大的部分 ---
    # 定义一个中间区域 (例如 x 从 12 到 18)
    middle_start = 12
    middle_end = 18
    # 使用一个高斯函数或其他平滑过渡函数来增强中间区域的波动
    # 这里使用一个简单的线性增强因子，在中间区域逐渐增大再减小
    if middle_start <= x <= middle_end:
        # 计算 x 在中间区域的相对位置 (0到1)
        relative_x = (x - middle_start) / (middle_end - middle_start)
        # 使用一个二次函数（抛物线）形状的增强因子，峰值在中间区域的中心
        # 峰值在 relative_x = 0.5 时达到最大
        # 例如，当 relative_x = 0.5 时，factor = 1，当 relative_x = 0 或 1 时，factor = 0
        enhancement_factor = 4 * relative_x * (1 - relative_x)  # 0 到 1 的增强因子
        raw_output += (
            np.sin(x * 5) * 5 * enhancement_factor
        )  # 增加更高频率和更大振幅的波动
    # ------------------------------------

    # 将 raw_output 映射到 0 到 9 的范围
    # 假设 raw_output 整体范围现在可能扩大到 -10 到 10 左右 (因为加了额外的波动)
    # 我们可以稍微调整映射的基准，确保大部分数据在范围内
    # (raw_output + 10) 范围大致在 0 到 20 之间
    # (raw_output + 10) * (9/20) 范围大致在 0 到 9 之间
    scaled_output = (raw_output + 10) * (9 / 20.0)  # 调整映射比例
    # 确保不超出 0-9 范围
    return np.clip(scaled_output, 0, 9)


# 定义 x 轴的范围
x_start = 0
x_end = 30  # 将横坐标设置为 0-30
num_points = 500  # 采样点数量
x = np.linspace(x_start, x_end, num_points)
y = np.array([fluctuating_function(val) for val in x])  # 对每个x值计算y

# --- 2. 图形初始化 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("波动函数的动态绘制 (中间波动加大)")
ax.set_xlabel("X轴")
ax.set_ylabel("Y轴")
ax.set_xlim(x_start, x_end)
ax.set_ylim(0, 9)  # 将纵坐标设置为 0-9
ax.grid(True)

# 初始只绘制一个空线
(line,) = ax.plot([], [], lw=2, color="blue")  # lw=2 是线宽


# --- 3. 动画函数 ---
def animate(i):
    """
    动画的每一帧调用的函数。
    i 是当前的帧数。
    """
    # 每次只绘制到第 i 个点
    line.set_data(x[:i], y[:i])
    return (line,)


# --- 4. 创建动画 ---
# FuncAnimation 参数:
# fig: 要动画的图形对象
# animate: 每一帧要调用的函数
# frames: 动画的总帧数 (这里是数据点的数量)
# interval: 每帧之间的延迟时间 (毫秒)
# blit: 是否只重绘发生变化的图形部分 (True 可以提高性能)
ani = animation.FuncAnimation(fig, animate, frames=num_points, interval=20, blit=True)

# --- 5. 显示动画 ---
plt.show()

# --- 6. (可选) 保存动画 ---
# 如果你想保存为 GIF 或 MP4，你需要安装相应的编码器
# 例如，保存为 GIF 需要 ImageMagick 或 Pillow
# ani.save('fluctuating_function_animation.gif', writer='pillow', fps=30)

# 保存为 MP4 需要 FFmpeg
ani.save("fluctuating_function_animation.mp4", writer="ffmpeg", fps=30)
