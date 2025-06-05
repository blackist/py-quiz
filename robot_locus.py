import matplotlib.pyplot as plt
import numpy as np

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


# --------------------

# --- 1. 数据生成：模拟机器人目标轨迹和实际轨迹 ---


def generate_robot_trajectory(
    num_points=1000, helix_radius=5, helix_height=10, noise_level=0.1
):
    """
    生成机器人目标轨迹（螺旋线）和带有噪声的实际轨迹。

    Args:
        num_points (int): 轨迹点数量。
        helix_radius (float): 螺旋线的半径。
        helix_height (float): 螺旋线的高度。
        noise_level (float): 实际轨迹相对于目标轨迹的噪声水平。

    Returns:
        tuple: (target_trajectory, actual_trajectory)
               target_trajectory: (num_points, 3) 形状的 NumPy 数组，表示目标点的 (x, y, z) 坐标。
               actual_trajectory: (num_points, 3) 形状的 NumPy 数组，表示实际点的 (x, y, z) 坐标。
    """
    print(f"生成包含 {num_points} 个点的机器人轨迹...")

    # 生成时间/角度参数
    t = np.linspace(0, 5 * np.pi, num_points)  # 5个螺旋圈

    # 目标轨迹 (螺旋线)
    x_target = helix_radius * np.cos(t)
    y_target = helix_radius * np.sin(t)
    z_target = helix_height * (t / (5 * np.pi))  # Z轴随t线性增加

    target_trajectory = np.vstack((x_target, y_target, z_target)).T

    # 实际轨迹 (在目标轨迹基础上添加随机噪声)
    noise = np.random.randn(num_points, 3) * noise_level  # 3D 噪声
    actual_trajectory = target_trajectory + noise

    print("轨迹生成完成。")
    return target_trajectory, actual_trajectory


# --- 2. 误差计算：欧几里得距离误差 ---


def calculate_position_error(target_pos, actual_pos):
    """
    计算机器人末端位姿的欧几里得距离误差（位置误差）。

    Args:
        target_pos (numpy.ndarray): (N, 3) 形状的 NumPy 数组，目标位置点。
        actual_pos (numpy.ndarray): (N, 3) 形状的 NumPy 数组，实际位置点。

    Returns:
        numpy.ndarray: (N,) 形状的 NumPy 数组，每个点的误差值。
    """
    print("计算位置误差...")
    # 计算每个维度上的差值平方
    diff_squared = (actual_pos - target_pos) ** 2
    # 求和并开方，得到欧几里得距离
    error = np.sqrt(np.sum(diff_squared, axis=1))
    print("误差计算完成。")
    return error


# --- 3. 数据可视化 ---


def visualize_error_2d(errors):
    """
    二维可视化误差随时间/步数的变化。

    Args:
        errors (numpy.ndarray): 误差值数组。
    """
    plt.figure(figsize=(10, 6))
    plt.plot(errors, color="blue", alpha=0.7)
    plt.title("机器人末端位姿误差随步数变化")
    plt.xlabel("步数 (模拟时间)")
    plt.ylabel("欧几里得距离误差 (单位)")
    plt.grid(True)
    plt.axhline(
        y=np.mean(errors),
        color="r",
        linestyle="--",
        label=f"平均误差: {np.mean(errors):.3f}",
    )
    plt.legend()
    plt.tight_layout()
    print("二维误差图生成。")


def visualize_trajectory_3d(target_trajectory, actual_trajectory, errors):
    """
    三维可视化机器人轨迹，并用颜色编码误差。

    Args:
        target_trajectory (numpy.ndarray): 目标轨迹点。
        actual_trajectory (numpy.ndarray): 实际轨迹点。
        errors (numpy.ndarray): 误差值数组，用于颜色编码。
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    print("生成三维轨迹图...")

    # 绘制目标轨迹
    ax.plot(
        target_trajectory[:, 0],
        target_trajectory[:, 1],
        target_trajectory[:, 2],
        color="gray",
        linestyle="--",
        label="目标轨迹",
        alpha=0.6,
    )

    # 绘制实际轨迹点，并用颜色编码误差
    # 颜色映射：误差越大，颜色越偏向暖色（如红色）
    cmap = plt.cm.viridis_r  # 可以选择其他颜色映射，如 'jet', 'hot', 'magma_r'
    sc = ax.scatter(
        actual_trajectory[:, 0],
        actual_trajectory[:, 1],
        actual_trajectory[:, 2],
        c=errors,
        cmap=cmap,
        s=20,
        alpha=0.8,
        label="实际轨迹 (颜色表示误差)",
    )

    # 添加误差连线（可选，如果点太多可能会很密集）
    # for i in range(len(target_trajectory)):
    #     ax.plot([target_trajectory[i, 0], actual_trajectory[i, 0]],
    #             [target_trajectory[i, 1], actual_trajectory[i, 1]],
    #             [target_trajectory[i, 2], actual_trajectory[i, 2]],
    #             color='red', linestyle=':', alpha=0.2, linewidth=0.5)

    ax.set_title("机器人目标与实际轨迹及误差可视化 (三维)")
    ax.set_xlabel("X 坐标")
    ax.set_ylabel("Y 坐标")
    ax.set_zlabel("Z 坐标")
    ax.legend()
    fig.colorbar(sc, label="位置误差")  # 添加颜色条
    plt.tight_layout()
    print("三维轨迹图生成。")


# --- 主程序 ---
if __name__ == "__main__":
    # 设定参数
    num_points = 1000  # 轨迹点数量
    helix_radius = 5  # 螺旋半径
    helix_height = 10  # 螺旋高度
    noise_level = 0.5  # 噪声水平，可以调整查看不同误差效果

    # 1. 生成数据
    target_traj, actual_traj = generate_robot_trajectory(
        num_points, helix_radius, helix_height, noise_level
    )

    # 2. 计算误差
    errors = calculate_position_error(target_traj, actual_traj)

    # 3. 数据可视化
    visualize_error_2d(errors)
    visualize_trajectory_3d(target_traj, actual_traj, errors)

    # 显示所有图表
    plt.show()

    print("\n--- 结果分析建议 ---")
    print("1. 观察二维误差折线图：")
    print("   - 误差是否在一个可接受的范围内波动？")
    print("   - 是否有异常的误差尖峰，这可能代表机器人控制系统瞬时失稳或外部干扰？")
    print("   - 误差趋势是收敛还是发散？")
    print("2. 观察三维轨迹图：")
    print("   - 目标轨迹和实际轨迹的偏离程度。")
    print(
        "   - 颜色越深（或根据你选择的颜色映射，表示误差较大的颜色），表示该点的实际位置与目标位置的偏差越大。"
    )
    print(
        "   - 哪些区域的误差更集中或更大？这可能与机器人运动的特定阶段（如加速、减速、转弯）或关节的性能限制有关。"
    )
    print("3. 应用讨论：")
    print("   - 这种可视化可以用于：机器人精度测试、控制算法性能评估、早期故障诊断等。")
    print(
        "   - 例如，如果误差在特定时间或特定空间区域持续增大，则需要检查相关机械部件或控制参数。"
    )
