# Lark - 字节级语言检测模型

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lark 是一个字节级语言检测模型，支持 **102 种语言**，具有高准确性和高效率。

## 🚀 特性

- **102 种语言**: 支持包括英语、中文、日语、西班牙语、法语等在内的多种语言
- **字节级处理**: 无词汇表限制，可处理任何 Unicode 文本
- **高准确性**: 在语言检测任务上达到最先进的性能
- **快速推理**: 针对 CPU 和 GPU 进行优化
- **易于集成**: 提供简单 API，支持批量和单文本处理

## 📦 安装

### 从 PyPI 安装（推荐）
```bash
pip install lark-ld==1.0.1
```

### 从源码安装
```bash
git clone https://github.com/farshore-byte/LarkDetect.git
cd LarkDetect
pip install -e .
```

## 🎯 快速开始

### 基础用法
```python
from lark import LarkDetector

# 初始化检测器
detector = LarkDetector()

# 检测单个文本的语言
text = "你好，今天过得怎么样？"
language, confidence = detector.detect(text)
print(f"语言: {language}, 置信度: {confidence:.4f}")

# 批量检测
texts = [
    "Hello world!",
    "今天天气真好",
    "こんにちは、元気ですか？"
]
results = detector.detect_batch(texts)
for text, (lang, conf) in zip(texts, results):
    print(f"'{text}' -> {lang} ({conf:.4f})")
```

### 高级用法
```python
from lark import LarkDetector

detector = LarkDetector()

# 获取前 k 个预测结果
text = "这是一个示例文本"
prediction, confidence, top_k = detector.detect_with_topk(text, k=5)
print(f"预测: {prediction} (置信度: {confidence:.4f})")
print("前 5 个预测:")
for i, item in enumerate(top_k):
    print(f"  {i+1}. {item['language']:8} - {item['probability']:.4f}")

# 置信度阈值
language, confidence, top_k = detector.detect_with_confidence(
    text, 
    confidence_threshold=0.7
)
if language == "unknown":
    print(f"置信度低: {confidence:.4f}")
else:
    print(f"检测到: {language} (置信度: {confidence:.4f})")
```

## 📊 支持的语言

Lark 支持 102 种语言，包括：

- **欧洲语言**: 英语、西班牙语、法语、德语、意大利语、俄语等
- **亚洲语言**: 中文、日语、韩语、印地语、阿拉伯语、泰语等
- **非洲语言**: 斯瓦希里语、约鲁巴语、祖鲁语等
- **其他语言**: 以及更多...

完整列表请参见 [all_dataset_labels.json](all_dataset_labels.json)。

## 🏗️ 模型架构

Lark 使用新颖的字节级架构：

1. **字节编码器**: 将原始字节转换为上下文表示
2. **边界预测器**: 使用 Gumbel-Sigmoid 识别片段边界
3. **片段解码器**: 处理片段进行语言分类

这种架构实现了：
- 无词汇表限制
- 对混合语言文本的鲁棒处理
- 长文档的高效处理

## 📈 性能

| 指标 | 数值 |
|------|------|
| 总体准确率 | 验证集上 90.14% |
| 推理速度 | 每文本约 1ms (CPU) |
| 模型大小 | 9.28MB (float16) |
| 精度 | float16 (CPU/GPU兼容) |
| 总参数数量 | 4,866,919 |
| 支持语言 | 102 |

### 训练数据集
模型在综合数据集上训练，包括：
- **opus-100** - 多语言平行语料库
- **Mike0307/language-detection** - 语言检测数据集
- **sirgecko___language_detection** - 语言检测数据集
- **papluca/language-identification** - 语言识别数据集
- **sirgecko/language_detection_train** - 语言检测训练数据

**数据集统计：**
- 训练样本：109,636,748
- 验证样本：385,306
- 总语言数：102

### 评估结果
详细的每种语言评估结果（准确率、精确率、召回率、F1分数）将在评估结果文件中提供。模型在验证数据集上达到 90.14% 的总体准确率。

**关于评估数据的说明**：虽然模型整体性能强劲，但当前评估数据集对某些语言的覆盖有限（例如 an、dz、hy、mn、yo）。这是由于验证集拆分中不包含这些语言的样本。然而，训练数据集提供了全面的覆盖。

### 训练数据集详情
模型在综合数据集上训练，包括：
- **OPUS-100** - 包含 100 种语言对的多语言平行语料库
- **Mike0307/language-detection** - 语言检测数据集
- **sirgecko___language_detection** - 语言检测数据集
- **papluca/language-identification** - 语言识别数据集
- **sirgecko/language_detection_train** - 语言检测训练数据

**OPUS-100 数据集统计：**
- 包含约 5500 万个句子对
- 覆盖 99 种语言对
- 44 种语言对拥有 100 万+句子对
- 73 种语言对拥有 10 万+句子对  
- 95 种语言对拥有 1 万+句子对
- 每种语言至少有 10,000 个训练样本

**数据集统计：**
- 训练样本：109,636,748
- 验证样本：385,306
- 总语言数：102

## 🔧 API 参考

### LarkDetector 类

```python
class LarkDetector:
    def __init__(self, model_path: str = None, labels_path: str = None):
        """初始化语言检测器"""
    
    def detect(self, text: str) -> Tuple[str, float]:
        """检测单个文本的语言"""
    
    def detect_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        """批量语言检测"""
    
    def detect_with_topk(self, text: str, k: int = 5) -> Tuple[str, float, List[Dict]]:
        """获取前 k 个预测结果及概率"""
    
    def detect_with_confidence(self, text: str, confidence_threshold: float = 0.5) -> Tuple[str, float, List[Dict]]:
        """带置信度阈值的检测"""
```

## 🛠️ 开发

### 设置开发环境
```bash
git clone https://github.com/farshore-byte/LarkDetect.git
cd LarkDetect
pip install -e ".[dev]"
```

### 运行测试
```bash
python -m pytest tests/
```

### 从源码构建
```bash
python setup.py sdist bdist_wheel
```

## 📝 引用

如果您在研究中使用了 Lark，请引用：

```bibtex
@software{lark2024,
  title={Lark: Byte-Level Language Detection},
  author={Farshore AI},
  year={2024},
  url={https://github.com/farshore-byte/LarkDetect}
}
```

## 🤝 贡献

我们欢迎贡献！详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢开源社区提供的数据集和工具
- 受现代语言检测方法的启发
- 基于 PyTorch 和 Hugging Face 生态系统构建
