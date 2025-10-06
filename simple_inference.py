# -*- coding: utf-8 -*-
"""
简单推理方案 - 直接使用PyTorch模型

由于ONNX和TorchScript都遇到问题，这里提供直接使用PyTorch模型的推理方案。
这是最稳定、最可靠的方案。
"""

import torch
import json
import time
from model import LarkModel
from tokenizer import batch_tokenize


class SimpleInference:
    """简单推理类 - 直接使用PyTorch模型"""
    
    def __init__(self, model_path: str = "./lark_epoch1.pth", labels_path: str = "./all_dataset_labels.json"):
        """
        初始化推理器
        
        Args:
            model_path: 模型权重路径
            labels_path: 标签文件路径
        """
        # 加载模型
        self.model = LarkModel(
            d_model=256, n_layers=4, n_heads=8, ff=512,
            label_size=102, dropout=0.0, max_len=1024
        )
        
        # 加载权重
        try:
            state_dict = torch.load(model_path, map_location='cpu')
            self.model.load_state_dict(state_dict, strict=True)
            print(f"✅ 模型权重加载成功: {model_path}")
        except Exception as e:
            print(f"⚠️ 权重加载失败: {e}")
            print("使用随机初始化模型")
        
        self.model.eval()
        
        # 加载标签映射
        with open(labels_path, "r", encoding="utf-8") as f:
            all_labels = json.load(f)["all_labels"]
        self.id2label = {i: lang for i, lang in enumerate(all_labels)}
        
        print(f"✅ 标签数量: {len(self.id2label)}")
        print(f"✅ 模型参数数量: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def predict(self, texts: list, max_len: int = 1024):
        """
        批量预测文本的语言
        
        Args:
            texts: 文本列表
            max_len: 最大序列长度
            
        Returns:
            predictions: 预测结果列表
            probabilities: 概率分布
        """
        # 分词
        token_ids, pad_mask = batch_tokenize(texts, max_len=max_len)
        
        # 推理
        with torch.no_grad():
            logits = self.model(token_ids, pad_mask)
        
        # 处理输出
        if logits.dim() == 3:  
            cls_logits = logits[:, 0, :]     # [B, label_size]
        else:
            cls_logits = logits              # [B, label_size]
        
        # 计算概率
        probabilities = torch.softmax(cls_logits, dim=-1)
        
        # 预测结果
        preds = torch.argmax(cls_logits, dim=-1)
        predictions = [self.id2label[p.item()] for p in preds]
        
        return predictions, probabilities
    
    def predict_single(self, text: str, max_len: int = 1024):
        """
        单文本预测
        
        Args:
            text: 输入文本
            max_len: 最大序列长度
            
        Returns:
            prediction: 预测语言
            probability: 预测概率
            top_k: 前k个预测结果
        """
        predictions, probabilities = self.predict([text], max_len=max_len)
        
        # 获取top-k预测
        probs = probabilities[0]
        top_probs, top_indices = torch.topk(probs, k=5)
        
        top_k = []
        for prob, idx in zip(top_probs, top_indices):
            top_k.append({
                "language": self.id2label[idx.item()],
                "probability": prob.item()
            })
        
        return predictions[0], probabilities[0].max().item(), top_k
    
    def predict_with_confidence(self, text: str, max_len: int = 1024, confidence_threshold: float = 0.5):
        """
        带置信度阈值的预测
        
        Args:
            text: 输入文本
            max_len: 最大序列长度
            confidence_threshold: 置信度阈值
            
        Returns:
            prediction: 预测语言 (如果置信度低于阈值返回"unknown")
            confidence: 置信度
            top_k: 前k个预测结果
        """
        prediction, confidence, top_k = self.predict_single(text, max_len)
        
        if confidence < confidence_threshold:
            return "unknown", confidence, top_k
        else:
            return prediction, confidence, top_k


def test_simple_inference():
    """测试简单推理"""
    print("=== 简单推理测试 ===")
    
    # 创建推理器
    inference = SimpleInference()
    
    # 测试文本
    test_texts = [
    "Hello, how are you doing today? It's nice to meet you here.",
    "今天的天气真不错，我们一起去公园散步吧！",
    "こんにちは！今日はどんな一日でしたか？楽しかったですか？",
    "Bonjour, je suis très heureux de te voir. Comment vas-tu aujourd'hui ?",
    "¡Hola! Espero que tengas un buen día lleno de energía y alegría.",
    "Привет! Как твои дела? Надеюсь, у тебя всё отлично сегодня.",
    "Ciao! Oggi è una bellissima giornata per fare una passeggiata al sole.",
    "안녕하세요! 오늘 기분이 어때요? 좋은 하루 보내세요!",
    "مرحبًا! كيف حالك اليوم؟ أتمنى لك يومًا سعيدًا ومليئًا بالنجاح.",
    "Hallo! Schön dich zu sehen. Wie läuft dein Tag bisher?"
    ]
    
    # 批量预测
    predictions, probabilities = inference.predict(test_texts)
    
    print("\n=== 批量预测结果 ===")
    for i, (text, pred, prob) in enumerate(zip(test_texts, predictions, probabilities)):
        confidence = prob.max().item()
        print(f"{i+1:2d}. {text[:30]:30} -> {pred:8} (置信度: {confidence:.4f})")
    
    # 单文本详细预测
    print("\n=== 单文本详细预测 ===")
    test_text = "This is a sample English text for language detection."
    prediction, confidence, top_k = inference.predict_single(test_text)
    
    print(f"文本: {test_text}")
    print(f"预测语言: {prediction} (置信度: {confidence:.4f})")
    print("Top 5 预测:")
    for i, item in enumerate(top_k):
        print(f"  {i+1}. {item['language']:8} - {item['probability']:.4f}")



def benchmark_inference():
    """性能基准测试"""
    print("\n=== 性能基准测试 ===")
    inference = SimpleInference()
    
    # 创建测试数据
    test_texts = ["Hello world, this is a test text for language detection."] * 50
    
    # 预热
    _ = inference.predict(test_texts[:5])
    
    # 基准测试
    start_time = time.time()
    predictions, _ = inference.predict(test_texts)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / len(test_texts)
    
    print(f"总文本数: {len(test_texts)}")
    print(f"总耗时: {total_time:.4f} 秒")
    print(f"平均每文本: {avg_time*1000:.2f} 毫秒")
    print(f"QPS: {len(test_texts)/total_time:.2f}")


def export_for_production():
    """生产环境部署建议"""
    print("\n=== 生产环境部署建议 ===")
    print("1. 直接使用PyTorch模型 (当前方案)")
    print("   - 优点: 稳定可靠，无需额外转换")
    print("   - 缺点: 需要PyTorch运行时")
    
    print("\n2. 使用Flask/FastAPI封装为Web服务")
    print("   - 创建REST API接口")
    print("   - 支持并发请求")
    print("   - 易于集成到现有系统")
    
    print("\n3. 使用Docker容器化部署")
    print("   - 创建包含PyTorch环境的Docker镜像")
    print("   - 确保环境一致性")
    print("   - 便于扩展和运维")
    
    print("\n4. 性能优化建议")
    print("   - 使用GPU加速 (如果可用)")
    print("   - 批处理优化")
    print("   - 模型量化 (torch.quantization)")


if __name__ == "__main__":
    test_simple_inference()
    benchmark_inference()
    export_for_production()
