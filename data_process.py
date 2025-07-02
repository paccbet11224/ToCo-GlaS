import os
import shutil
from glob import glob
from PIL import Image
import numpy as np

# 设置原始路径
SRC_IMG = r'hsn_data/img/02_glas_full'
SRC_MASK = r'hsn_data/gt/02_glas_full/glas'

# 新数据集输出路径
DST_ROOT = r'hsn_data/ToCo_GlaS'
DST_IMG = os.path.join(DST_ROOT, 'images')
DST_MASK = os.path.join(DST_ROOT, 'masks')

splits = {
    'train': 'train_',
    'val': 'testA_',
    'test': 'testB_'
}

os.makedirs(DST_ROOT, exist_ok=True)
for subset in splits:
    os.makedirs(os.path.join(DST_IMG, subset), exist_ok=True)
    os.makedirs(os.path.join(DST_MASK, subset), exist_ok=True)

lists = {subset: [] for subset in splits}

# 遍历图片，按前缀分配
for img_path in glob(os.path.join(SRC_IMG, '*.png')):
    fname = os.path.basename(img_path)
    for subset, prefix in splits.items():
        if fname.startswith(prefix):
            mask_path = os.path.join(SRC_MASK, fname)
            if not os.path.exists(mask_path):
                print(f"Warning: Mask not found for {fname}")
                continue
            # 复制图片
            shutil.copy(img_path, os.path.join(DST_IMG, subset, fname))
            # 读取并二值化掩码（只保留像素值229为腺体）
            mask = np.array(Image.open(mask_path))
            mask_bin = (mask == 229).astype(np.uint8)
            Image.fromarray(mask_bin * 1).save(os.path.join(DST_MASK, subset, fname))
            # 记录文件名（不含扩展名）
            lists[subset].append(fname[:-4])
            break

# 写入txt索引文件
for subset in splits:
    with open(os.path.join(DST_ROOT, f"{subset}.txt"), 'w') as f:
        f.write('\n'.join(sorted(lists[subset])))

print("GlaS数据已转换为ToCo格式，输出目录：", DST_ROOT)