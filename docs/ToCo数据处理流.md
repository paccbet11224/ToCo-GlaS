根据对 rulixiang/ToCo 仓库（CVPR 2023 Token Contrast for Weakly-Supervised Semantic Segmentation）的源码分析，ToCo 的数据集处理方式如下：

---

## 1. 数据集目录结构与索引

- **images 目录**：保存输入图片（如 JPEG/PNG），分子文件夹（如 train2014、val2014）或自定义 train/val/test。
- **masks/labels 目录**：保存分割掩码（PNG，单通道，像素值为类别编号），同样分子文件夹。
- **索引文件**：如 `train.txt`、`val.txt`，每行一个样本名（不带扩展名），决定数据集划分。
- **cls_labels_onehot.npy**（可选）：用于分类标签的 one-hot 编码，但分割训练不必需。

---

## 2. 数据加载方式

以 `datasets/coco.py` 为例：

- 构造数据集时，传入图片目录、掩码目录和索引txt路径。
- `load_img_name_list()` 读取 txt，每行一个文件名，作为数据集索引。
- `__getitem__` 按索引加载图片和掩码（如 images/train2014/xxx.jpg 与 labels/train2014/xxx.png）。
- **掩码读取时像素值为类别编号**（如二分类为 0/1，多类为 0,1,2,...）。
- test 阶段可不加载掩码，仅图片。

---

## 3. 掩码格式

- 掩码为单通道灰度图，**像素值为类别编号**，不需要提前 one-hot。
- ignore 区域用 255（ignore_index）标记，不参与损失计算。

---

## 4. 数据增强与预处理

- 数据增强（训练阶段可选）包括：
  - 随机缩放、随机裁剪、随机水平翻转、色彩扰动等
  - 图像归一化（均值/方差标准化），ToTensor
- 增强操作在 __transforms 中实现，对图片和掩码同步处理。

---

## 5. one-hot 处理

- **训练时不要求掩码为 one-hot 格式，直接用类别编号标签。**
- 如果有 one-hot 需求（如分类标签），内部有 `_to_onehot` 静态方法，但分割掩码默认不用 one-hot。

---

## 6. 配置与运行

- 在训练脚本或 config 中指定 images_dir、label_dir、name_list_dir（即图片、掩码、索引文件路径）。
- 各 split（train/val/test）用独立 txt 文件区分。
- 只要保证图片与掩码一一对应、索引文件正确，ToCo会自动完成数据加载和增强。

---

## 7. 典型流程示意

```python
img_list = load_img_name_list('train.txt')
for img_name in img_list:
    img = Image.open(os.path.join(images_dir, 'train2014', img_name+'.jpg'))
    mask = Image.open(os.path.join(label_dir, 'train2014', img_name+'.png'))
    # mask为单通道，像素值为类别编号
    # 数据增强与归一化等在transforms中自动完成
```

---

## 总结

- ToCo的数据集处理完全遵循分割领域主流标准：**单通道类别编号掩码，txt分割，自动增强，无需提前one-hot**。
- 你的当前数据集结构与处理方式（图片、mask、索引txt文件）完全适用ToCo，无需再特殊处理。
- 运行ToCo只需在config/脚本中指向你的数据路径即可。
