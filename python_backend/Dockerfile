FROM python:3.10-slim

# 安装系统依赖 (OpenCV/rembg 需要)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
# --no-cache-dir 减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 预下载 rembg 模型 (u2net) 到默认目录
# 这样容器启动时不需要联网下载模型，加快启动速度
RUN python -c "from rembg.session_factory import new_session; new_session('u2net')"

# 复制其余代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
