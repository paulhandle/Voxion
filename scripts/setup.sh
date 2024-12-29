#!/bin/bash

# 确保脚本在错误时停止
set -e

echo "开始设置语音标注系统..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p uploads
mkdir -p annotations

# 下载模型
echo "下载 Whisper 模型..."
python scripts/download_models.py

echo "设置完成！"
