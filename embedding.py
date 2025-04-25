from sentence_transformers import SentenceTransformer

# 加载BGE-M3模型
model = SentenceTransformer('BAAI/bge-m3')


def embedding_text(text: str):
    """
    获取文本的嵌入表示
    :param text: 输入文本
    :return: 嵌入表示
    """
    # 获取文本的嵌入表示
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    return embedding
