FROM pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime

WORKDIR /app

# 安装依赖
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
# COPY api.py .
# COPY embedding.py .

# 暴露端口
# EXPOSE 8001

# 启动应用
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]

# 判断是否有 torch cuda 环境
CMD [ "python", "-c", "import torch; print(torch.cuda.is_available())" ]

