# 使用说明

### 如果遇到问题，请在本仓库内提issue。

如果想要检验各个模型在您的电脑上的效果，请将本仓库内的内容下载到您的电脑上。然后执行以下步骤：

1.在本项目目录下，执行pip install -r requirements.txt安装需要的包。

2.进入myProject文件夹，修改aimbot.py文件中第25行代码：

```
model=YOLO("D:/aimbot/myProject/final_8n_best.pt")
```

将后面的pt文件路径改为您想要尝试的pt文件的绝对路径。

然后请修改第31行代码：

```
monitor = sct.monitors[2]
```

如果您想要侦测的画面处在第二显示屏，则无需修改，否则请修改[2]为[x]，x为您想要检测的屏幕序号（电脑屏幕本体一般为1）。

在本仓库中提供这些pt文件：

对应于PPT第6页的yolov8n yolov8s yolov8m的训练结果：

8n_best.pt, 	8s_best.pt,	 8m_best.pt

对应于PPT第14页 leave marked red的训练结果：

red_8n_best.pt

对应于PPT第15页 leave marked red、add headline into box的训练结果：

red_nohead_best.pt,	red_8n_best_include_headline.pt

对应于PPT第18页的左右两个训练结果：

final_8n_best.pt,	huge_data.pt

3.修改好后，运行aimbot.py文件。可将main函数中的参数改为1以启用自动射击功能。

4.请注意！守望先锋在电脑上会屏蔽win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,final_x,final_y)等对于CSGO可用的库函数。

我在本机上曾成功使用该库函数在守望先锋上运行aimbot，但似乎被守望先锋检测到。之后一天无法登入游戏。再之后本机上的库函数在游戏内部就无法起效果了。

作为替代，我选择使用云游戏（网易云游戏，初始注册后赠送若干小时免费PC游戏时长）运行守望先锋，证明使用云游戏时可以让aimbot的鼠标移动功能正常起作用。

如果您想要体验完整瞄准功能，可以采取同样策略。
如果您只需要检验模型性能，则可以本地运行守望先锋并使用aimbot.py生成的实时检测窗口来看是否实时识别了游戏内的敌人。

## 部分文件说明

big_data_train_result文件夹中存储了PPT18页中大数据集模型的训练结果

data/datasets/cross_validation.py是k折交叉验证的生成训练数据的文件。

data/datasets/greater_train.py是k折交叉验证的训练文件。

data/datasets/leave_red.py是将图片转换为仅剩红像素的图片。

data/datasets/split_data.py是正常数据集（如image_v_2）的生成训练数据的文件。

data/datasets/train.py是正常数据集（如image_v_2）的训练文件。

data/datasets/data中包含了数据集（本来还有其他数据集，包括不含头部的txt版本，不同通道过滤的红像素图片，k折交叉验证数据集等，但因为不易于传到github仓库上，因此我精选了几个数据集）。