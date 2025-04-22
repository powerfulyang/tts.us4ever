import os
import uuid
import asyncio
import time
from typing import Optional

import edge_tts
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# 创建临时文件存储目录
os.makedirs("temp", exist_ok=True)


class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = "zh-CN-XiaoyiNeural"


def remove_file(path: str):
    """删除临时文件"""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error removing file {path}: {e}")


@app.post("/tts")
async def text_to_speech(request: TextToSpeechRequest, background_tasks: BackgroundTasks):
    """
    将文本转换为语音并返回音频文件
    """
    try:
        # 生成唯一的文件名
        output_file = f"temp/temp_{uuid.uuid4()}.mp3"

        # 调用edge_tts生成语音
        communicate = edge_tts.Communicate(request.text, request.voice)
        await communicate.save(output_file)

        # 确保文件创建成功
        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="音频文件生成失败")

        # 添加后台任务清理文件
        background_tasks.add_task(remove_file, output_file)

        # 返回文件响应
        return FileResponse(
            path=output_file,
            media_type="audio/mpeg",
            filename="speech.mp3",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成语音时出错: {str(e)}")


# 定期清理临时文件的后台任务
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_temp_files())


async def cleanup_temp_files():
    """定期清理临时文件夹中的旧文件"""
    while True:
        try:
            # 等待一段时间后清理
            await asyncio.sleep(3600)  # 每小时清理一次

            current_time = time.time()
            for filename in os.listdir("temp"):
                file_path = os.path.join("temp", filename)
                # 如果文件存在且超过30分钟，则删除
                if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 1800:
                    os.remove(file_path)
        except Exception as e:
            print(f"Error in cleanup task: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
