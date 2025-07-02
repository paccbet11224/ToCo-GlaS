下面是一段关于处理后 GlaS 数据集（ToCo_GlaS 目录）的简要介绍，适合写在readme或文档中：

---

## ToCo_GlaS 数据集结构说明与使用指南

本数据集已按 ToCo 语义分割训练框架的标准格式整理，适用于腺体分割（GlaS）任务。其目录与文件结构如下：

### 目录结构说明

```
ToCo_GlaS/
├── images/
│   ├── train/   # 训练集原始图片
│   ├── val/     # 验证集原始图片
│   └── test/    # 测试集原始图片
├── masks/
│   ├── train/   # 训练集掩码（0/1，0为背景，1为腺体）
│   ├── val/     # 验证集掩码
│   └── test/    # 测试集掩码
├── train.txt    # 训练集图片文件名索引（无扩展名）
├── val.txt      # 验证集图片文件名索引（无扩展名）
└── test.txt     # 测试集图片文件名索引（无扩展名）
```

- **images/**：存放原始的组织切片图片，分为train/val/test三类。
- **masks/**：存放与原图一一对应的掩码（mask），已二值化（0=背景，1=腺体），同样分为train/val/test。
- **train.txt / val.txt / test.txt**：每个txt文件按行列举了该子集所有样本的文件名（不带扩展名），用于训练脚本读取。

### 如何在ToCo中使用本数据集

1. **数据配置**：在ToCo的配置文件（如`config/dataset/your_dataset.yaml`）中，指定images、masks和索引txt文件的路径。例如：

   ```yaml
   train:
     images_dir: /path/to/ToCo_GlaS/images/train
     masks_dir: /path/to/ToCo_GlaS/masks/train
     file_list: /path/to/ToCo_GlaS/train.txt
   val:
     images_dir: /path/to/ToCo_GlaS/images/val
     masks_dir: /path/to/ToCo_GlaS/masks/val
     file_list: /path/to/ToCo_GlaS/val.txt
   test:
     images_dir: /path/to/ToCo_GlaS/images/test
     masks_dir: /path/to/ToCo_GlaS/masks/test
     file_list: /path/to/ToCo_GlaS/test.txt
   ```

2. **通用分割训练流程**：加载上述配置后，ToCo会自动按txt列表读取图片和掩码进行训练、验证和评估，无需手动对齐或额外处理。

3. **注意事项**：
   - 掩码已标准化为0/1，适合二分类分割任务。
   - 文件名和索引对应，无需额外脚本处理。

4. **开始训练**：根据ToCo文档，运行训练脚本即可。例如：

   ```bash
   python train.py --config config/dataset/your_dataset.yaml
   ```

---

**总结**：  
本 GlaS 数据集已完全适配 ToCo 的训练、验证、测试流程，用户只需在配置中正确填写路径，即可直接用于模型训练与评估。