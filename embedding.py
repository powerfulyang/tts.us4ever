import torch
from sentence_transformers import SentenceTransformer

model = None
default_embedding = None


def load_model():
    global model, default_embedding
    # 加载BGE-M3模型
    model = SentenceTransformer('BAAI/bge-m3')

    # 获取模型的第一个参数的设备
    device = next(model.parameters()).device
    if device.type == 'cuda':
        print(f"模型在 GPU 上运行，设备：{device}")
        # 进一步显示 GPU 信息
        print(f"GPU 名称：{torch.cuda.get_device_name(device.index if device.index is not None else 0)}")
    else:
        print("模型在 CPU 上运行")

    default_embedding = model.encode("unknown", normalize_embeddings=True).tolist()


def embedding_text(text: str):
    """
    获取文本的嵌入表示
    :param text: 输入文本
    :return: 嵌入表示
    """
    if model is None:
        load_model()

    # 检查输入是否为空
    if not text.strip():
        # 或者返回预计算的默认向量
        return default_embedding
    # 获取文本的嵌入表示
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    return embedding
