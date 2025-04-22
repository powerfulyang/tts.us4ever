# 文本转语音 API

这是一个基于 FastAPI 和 Edge TTS 的简单文本转语音 API。

## 安装依赖

```bash
pip install fastapi edge-tts uvicorn
```

## 运行服务

### 本地运行

```bash
uvicorn api:app --reload
```

或者直接运行：

```bash
python api.py
```

服务将在 http://localhost:8000 上启动。

### 使用 Docker 运行

构建 Docker 镜像：

```bash
docker build -t tts-api .
```

运行 Docker 容器：

```bash
docker run -p 8000:8000 tts-api
```

服务将在 http://localhost:8000 上启动。

## API 使用方法

### 文本转语音

**接口**：`POST /tts`

**请求体**：
```json
{
  "text": "你想要转换成语音的文本",
  "voice": "zh-CN-XiaoyiNeural"  // 可选参数，默认为中文女声
}
```

**响应**：
- 成功时返回音频文件 (MP3 格式)
- 失败时返回错误信息

### 示例

使用 curl 发送请求：

```bash
curl -X POST "http://localhost:8000/tts" \
     -H "Content-Type: application/json" \
     -d '{"text":"你好，这是一段测试文本"}' \
     --output speech.mp3
```

使用 Python 发送请求：

```python
import requests

response = requests.post(
    "http://localhost:8000/tts",
    json={"text": "你好，这是一段测试文本"}
)

# 保存返回的音频文件
if response.status_code == 200:
    with open("speech.mp3", "wb") as f:
        f.write(response.content)
```

## 可用的语音列表

以下是部分可用的语音：

- `zh-CN-XiaoxiaoNeural` - 中文女声
- `zh-CN-XiaoyiNeural` - 中文女声 (默认)
- `zh-CN-YunjianNeural` - 中文男声
- `en-US-AriaNeural` - 英文女声
- `en-US-GuyNeural` - 英文男声

更多语音可以参考 Edge TTS 的文档。 