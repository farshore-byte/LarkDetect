# Lark - Byte-Level Language Detection

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![中文文档](https://img.shields.io/badge/文档-中文-blue.svg)](README_zh.md)


<div align="center">
  <h3>🌍 Byte-Level Language Detection Supporting 102 Languages</h3>
  <p>High-accuracy, efficient language identification solution</p>
  
  <p>
    <a href="README_zh.md">中文文档</a> | 
    <a href="README.md">English Documentation</a>
  </p>
</div>

---

## 🚀 Features

- **102 Languages**: Supports a wide range of languages including English, Chinese, Japanese, Spanish, French, etc.
- **Byte-Level Processing**: No vocabulary limitations, handles any Unicode text
- **High Accuracy**: State-of-the-art performance on language detection tasks
- **Fast Inference**: Optimized for both CPU and GPU
- **Easy Integration**: Simple API for both batch and single text processing

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install lark-ld==1.0.1
```

### From Source
```bash
git clone https://github.com/farshore-byte/LarkDetect.git
cd LarkDetect
pip install -e .
```

## 🎯 Quick Start

### Basic Usage
```python
from lark import LarkDetector

# Initialize detector
detector = LarkDetector()

# Detect language for single text
text = "Hello, how are you today?"
language, confidence = detector.detect(text)
print(f"Language: {language}, Confidence: {confidence:.4f}")

# Batch detection
texts = [
    "Hello world!",
    "今天天气真好",
    "こんにちは、元気ですか？"
]
results = detector.detect_batch(texts)
for text, (lang, conf) in zip(texts, results):
    print(f"'{text}' -> {lang} ({conf:.4f})")
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| Overall Accuracy | **89.61%** on validation set (97 languages with samples) |
| Inference Speed | ~1ms per text (CPU) |
| Model Size | 9.28MB (float16) |
| Precision | float16 (CPU/GPU compatible) |
| Total Parameters | 4,866,919 |
| Supported Languages | 102 |

**Detailed Evaluation**: See [classification report](classification_report.txt) for per-language metrics (precision, recall, F1-score).

---

## 📝 More Information

For detailed documentation, please see:
- **[中文详细文档](README_zh.md)** - Complete Chinese documentation
- **[English Full Documentation](README.md)** - Complete English documentation

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
