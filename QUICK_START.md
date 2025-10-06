# Lark 快速开始指南

## 🚀 快速安装和使用

### 方法1：从当前目录安装
```bash
# 进入项目目录
cd detect_language_format/git_/Lark

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

### 方法2：直接使用（无需安装）
```bash
# 直接运行Python脚本
cd detect_language_format/git_/Lark
python -c "from lark import LarkDetector; detector = LarkDetector(); print(detector.detect('Hello world'))"
```

## 📝 基本使用方法

### 1. 简单检测
```python
from lark import LarkDetector

# 初始化检测器
detector = LarkDetector()

# 检测单个文本
text = "Hello, how are you today?"
language, confidence = detector.detect(text)
print(f"语言: {language}, 置信度: {confidence:.4f}")
```

### 2. 批量检测
```python
texts = [
    "Hello world!",
    "今天天气真好",
    "こんにちは、元気ですか？"
]
results = detector.detect_batch(texts)

for text, (lang, conf) in zip(texts, results):
    print(f"'{text}' -> {lang} ({conf:.4f})")
```

### 3. 高级功能
```python
# 获取前5个预测
language, confidence, top_k = detector.detect_with_topk(text, k=5)
print(f"预测: {language} (置信度: {confidence:.4f})")
for i, item in enumerate(top_k):
    print(f"  {i+1}. {item['language']:8} - {item['probability']:.4f}")

# 使用置信度阈值
language, confidence, top_k = detector.detect_with_confidence(
    text, confidence_threshold=0.7
)
if language == "unknown":
    print(f"低置信度: {confidence:.4f}")
else:
    print(f"检测到: {language} (置信度: {confidence:.4f})")
```

## 🎮 交互式演示

```bash
# 运行交互式演示
cd detect_language_format/git_/Lark
python demo.py
```

## 🔧 关于 HF_ENDPOINT

**HF_ENDPOINT=https://hf-mirror.com 对Lark项目无效**，因为：

1. **Lark是独立项目**：不依赖Hugging Face Hub
2. **模型权重本地加载**：直接从本地文件加载模型权重
3. **无需网络连接**：推理过程完全离线

### 如果您需要下载预训练模型：
```bash
# 如果模型权重需要从网络下载，可以使用镜像
export HF_ENDPOINT=https://hf-mirror.com

# 但Lark目前设计为从本地文件加载
# 您需要将训练好的模型文件放在项目根目录
```

## 📁 文件结构说明

```
Lark/
├── lark/                    # 主包目录
│   ├── __init__.py         # 包初始化
│   ├── model.py            # 模型架构
│   ├── tokenizer.py        # 分词器
│   └── detector.py         # 主要API
├── lark_epoch1.pth         # 模型权重文件（需要添加）
├── all_dataset_labels.json # 语言标签映射
├── requirements.txt        # 依赖列表
├── setup.py               # 包配置
├── demo.py                # 交互式演示
├── examples/              # 使用示例
└── tests/                 # 单元测试
```

## ⚠️ 常见问题

### Q: 运行时提示找不到模型文件？
A: 需要将训练好的模型权重文件（如 `lark_epoch1.pth`）复制到项目根目录。

### Q: 如何自定义模型路径？
```python
detector = LarkDetector(
    model_path="/path/to/your/model.pth",
    labels_path="/path/to/your/labels.json"
)
```

### Q: 支持哪些语言？
```python
detector = LarkDetector()
languages = detector.get_supported_languages()
print(f"支持 {len(languages)} 种语言: {languages[:10]}...")
```

### Q: 如何提高检测精度？
- 使用更长的文本（建议至少20个字符）
- 检查文本编码（确保是UTF-8）
- 使用置信度阈值过滤低质量结果

## 🛠️ 开发模式

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/

# 构建包
python setup.py sdist bdist_wheel
```

## 📞 获取帮助

如果遇到问题：
1. 检查模型文件是否存在
2. 确认PyTorch安装正确
3. 查看错误日志中的具体信息
4. 运行测试用例验证功能
