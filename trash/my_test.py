import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# 创建一些数据
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig = plt.figure(figsize=(8, 6))

gs = gridspec.GridSpec(2, 3, width_ratios=[5, 1, 5], height_ratios=[5, 1])

for i in range(2):
    for j in range(2):
        ax = fig.add_subplot(gs[i * 2 + j])
        im = ax.imshow(y + (i - j), cmap='viridis')

        # 每个子图关联到相同的colorbar对象
        cax = fig.add_subplot(gs[2 + i * 2 + j])
        fig.colorbar(im, cax=cax)

plt.show()