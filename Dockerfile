# Fly.io Dockerfile for ValueCell Backend
FROM python:3.12-slim

WORKDIR /app

# 安装 uv (Python 包管理器)
RUN pip install uv

# 复制后端代码
COPY python/ ./python/
COPY .env.example ./.env

# 安装依赖
WORKDIR /app/python
RUN bash scripts/prepare_envs.sh
RUN uv sync

# 创建数据目录（挂载卷）
RUN mkdir -p /data
ENV DATABASE_PATH=/data/valuecell.db

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uv", "run", "valuecell/server/main.py"]
