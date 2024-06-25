import datetime
import shutil
from pathlib import Path
from collections import Counter
import os

import yaml
import numpy as np
import pandas as pd
from ultralytics import YOLO
from sklearn.model_selection import KFold

# 定义数据集路径
dataset_path = Path('D:\\aimbot\data\datasets\data\greater_image')  # 替换成你的数据集路径

# 获取所有标签文件的列表
labels = sorted(dataset_path.rglob("*.txt"))  # 所有标签文件在'labels'目录中

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的文件夹路径（即当前文件的根目录）
root_directory = os.path.dirname(current_file_path)

print("当前文件运行根目录:", root_directory)

# 从YAML文件加载类名
yaml_file = 'D:\\aimbot\data\datasets\data\classes.yaml'
with open(yaml_file, 'r', encoding="utf8") as y:
    classes = yaml.safe_load(y)['names']
cls_idx = sorted(classes.keys())

# 创建DataFrame来存储每张图像的标签计数
indx = [l.stem for l in labels]  # 使用基本文件名作为ID（无扩展名）
labels_df = pd.DataFrame([], columns=cls_idx, index=indx)

# 计算每张图像的标签计数
for label in labels:
    lbl_counter = Counter()

    with open(label, 'r') as lf:
        lines = lf.readlines()

    for l in lines:
        # YOLO标签使用每行的第一个位置的整数作为类别
        lbl_counter[int(l.split(' ')[0])] += 1

    labels_df.loc[label.stem] = lbl_counter

# 用0.0替换NaN值
labels_df = labels_df.fillna(0.0)

# 使用K-Fold交叉验证拆分数据集
ksplit = 5
kf = KFold(n_splits=ksplit, shuffle=True, random_state=20)  # 设置random_state以获得可重复的结果
kfolds = list(kf.split(labels_df))
folds = [f'split_{n}' for n in range(1, ksplit + 1)]
folds_df = pd.DataFrame(index=indx, columns=folds)

# 为每个折叠分配图像到训练集或验证集
for idx, (train, val) in enumerate(kfolds, start=1):
    folds_df[f'split_{idx}'].loc[labels_df.iloc[train].index] = 'train'
    folds_df[f'split_{idx}'].loc[labels_df.iloc[val].index] = 'val'

# 计算每个折叠的标签分布比例
fold_lbl_distrb = pd.DataFrame(index=folds, columns=cls_idx)
for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
    train_totals = labels_df.iloc[train_indices].sum()
    val_totals = labels_df.iloc[val_indices].sum()

    # 为避免分母为零，向分母添加一个小值（1E-7）
    ratio = val_totals / (train_totals + 1E-7)
    fold_lbl_distrb.loc[f'split_{n}'] = ratio

# 创建目录以保存分割后的数据集
save_path = Path(dataset_path / f'{datetime.date.today().isoformat()}_{ksplit}-Fold_Cross-val')
save_path.mkdir(parents=True, exist_ok=True)

# 获取图像文件列表
images = sorted(dataset_path.rglob("*.png"))  # 更改文件扩展名以匹配你的数据
ds_yamls = []

# 循环遍历每个折叠并复制图像和标签
for split in folds_df.columns:
    # 为每个折叠创建目录
    split_dir = save_path / split
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'labels').mkdir(parents=True, exist_ok=True)



    # 创建数据集的YAML文件
    dataset_yaml = split_dir / f'{split}_dataset.yaml'
    ds_yamls.append(dataset_yaml.as_posix())
    split_dir = os.path.join(root_directory, split_dir.as_posix())

    with open(dataset_yaml, 'w') as ds_y:
        yaml.safe_dump({
            'path': split_dir,
            'train': 'train',
            'val': 'val',
            'names': classes
        }, ds_y)
print(ds_yamls)

# 将文件路径保存到一个txt文件中
with open('D:\\aimbot\data\\file_paths.txt', 'w') as f:
    for path in ds_yamls:
        f.write(path + '\n')

# 为每个折叠复制图像和标签到相应的目录
for image, label in zip(images, labels):
    for split, k_split in folds_df.loc[image.stem].items():
        # 目标目录
        img_to_path = save_path / split / k_split / 'images'
        lbl_to_path = save_path / split / k_split / 'labels'

        # 将图像和标签文件复制到新目录中
        # 如果文件已存在，可能会抛出SamefileError
        shutil.copy(image, img_to_path / image.name)
        shutil.copy(label, lbl_to_path / label.name)
