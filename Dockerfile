# Fly.io Dockerfile for ValueCell Backend
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv (Python 包管理器)
RUN pip install --no-cache-dir uv

# 复制后端代码和依赖文件
COPY python/pyproject.toml python/uv.lock ./python/
WORKDIR /app/python

# 创建虚拟环境并安装依赖（不包括 dev 依赖）
RUN uv venv --python 3.12 && \
    uv sync --no-dev

# 复制应用代码
COPY python/ ./

# 创建数据目录（挂载卷）
RUN mkdir -p /data
ENV DATABASE_PATH=/data/valuecell.db

# 暴露端口
EXPOSE 8000

# 启动命令 - 直接使用 uvicorn
CMD ["uv", "run", "uvicorn", "valuecell.server.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
