FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY api.py .
COPY embedding.py .

# 暴露端口
EXPOSE 8001

# 启动应用
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
