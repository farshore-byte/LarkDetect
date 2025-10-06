#!/usr/bin/env python3
"""
准确率分析脚本
用于分析分类报告并计算过滤后的准确率
"""

import re
from typing import Dict, List, Tuple

def parse_classification_report(file_path: str) -> Dict:
    """解析分类报告文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'languages': {},
        'accuracy': 0.0,
        'macro_avg': {},
        'weighted_avg': {}
    }
    
    lines = content.split('\n')
    
    # 解析每个语言的指标
    for line in lines:
        line = line.strip()
        if not line or line.startswith('=') or line.startswith('Detailed'):
            continue
            
        # 解析准确率
        if 'accuracy' in line and not line.startswith('macro') and not line.startswith('weighted'):
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'accuracy':
                    if i + 1 < len(parts):
                        try:
                            results['accuracy'] = float(parts[i + 1])
                        except ValueError:
                            pass
                    break
            continue
            
        # 解析宏平均和加权平均
        if line.startswith('macro avg'):
            parts = line.split()
            if len(parts) >= 5:
                try:
                    results['macro_avg'] = {
                        'precision': float(parts[1]),
                        'recall': float(parts[2]),
                        'f1': float(parts[3]),
                        'support': int(parts[4])
                    }
                except ValueError:
                    pass
            continue
            
        if line.startswith('weighted avg'):
            parts = line.split()
            if len(parts) >= 5:
                try:
                    results['weighted_avg'] = {
                        'precision': float(parts[1]),
                        'recall': float(parts[2]),
                        'f1': float(parts[3]),
                        'support': int(parts[4])
                    }
                except ValueError:
                    pass
            continue
            
        # 解析语言指标
        parts = line.split()
        if len(parts) >= 5:
            try:
                language = parts[0]
                precision = float(parts[1])
                recall = float(parts[2])
                f1 = float(parts[3])
                support = int(parts[4])
                
                results['languages'][language] = {
                    'precision': precision,
                    'recall': recall,
                    'f1': f1,
                    'support': support
                }
            except ValueError:
                continue
    
    return results

def calculate_filtered_accuracy(results: Dict) -> Tuple[float, List[str]]:
    """计算过滤掉无样本语言后的准确率"""
    languages_with_samples = {}
    languages_without_samples = []
    
    total_samples = 0
    total_correct = 0
    
    for lang, metrics in results['languages'].items():
        if metrics['support'] > 0:
            languages_with_samples[lang] = metrics
            total_samples += metrics['support']
            total_correct += metrics['recall'] * metrics['support']
        else:
            languages_without_samples.append(lang)
    
    filtered_accuracy = total_correct / total_samples if total_samples > 0 else 0
    
    return filtered_accuracy, languages_without_samples

def main():
    """主函数"""
    print("=== Lark 语言检测模型准确率分析 ===\n")
    
    # 解析分类报告
    results = parse_classification_report('classification_report.txt')
    
    print(f"原始准确率: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"宏平均F1: {results['macro_avg'].get('f1', 0):.4f}")
    print(f"加权平均F1: {results['weighted_avg'].get('f1', 0):.4f}")
    
    # 计算过滤后的准确率
    filtered_accuracy, languages_without_samples = calculate_filtered_accuracy(results)
    
    print(f"\n=== 过滤分析结果 ===")
    print(f"总语言数: {len(results['languages'])}")
    print(f"有验证样本的语言数: {len(results['languages']) - len(languages_without_samples)}")
    print(f"无验证样本的语言数: {len(languages_without_samples)}")
    print(f"无样本语言: {languages_without_samples}")
    
    print(f"\n=== 准确率对比 ===")
    print(f"原始准确率: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"过滤后准确率: {filtered_accuracy:.4f} ({filtered_accuracy*100:.2f}%)")
    
    # 差异分析
    difference = abs(results['accuracy'] - filtered_accuracy)
    if difference < 0.0001:
        print("✅ 准确率一致（差异可忽略）")
    else:
        print(f"⚠️ 存在差异: {difference:.6f}")
    
    # 详细统计
    print(f"\n=== 详细统计 ===")
    total_samples = sum(metrics['support'] for metrics in results['languages'].values())
    total_correct = sum(metrics['recall'] * metrics['support'] for metrics in results['languages'].values() if metrics['support'] > 0)
    
    print(f"总验证样本数: {total_samples:,}")
    print(f"正确预测样本数: {total_correct:,.0f}")
    
    # 按支持数排序显示语言性能
    print(f"\n=== 语言性能排名（按支持数）===")
    languages_with_samples = {lang: metrics for lang, metrics in results['languages'].items() if metrics['support'] > 0}
    sorted_languages = sorted(languages_with_samples.items(), key=lambda x: x[1]['support'], reverse=True)
    
    print(f"{'语言':<8} {'支持数':<8} {'准确率':<8} {'F1分数':<8}")
    print("-" * 40)
    for lang, metrics in sorted_languages[:10]:  # 显示前10个
        print(f"{lang:<8} {metrics['support']:<8} {metrics['recall']:<8.3f} {metrics['f1']:<8.3f}")
    
    if len(sorted_languages) > 10:
        print(f"... 还有 {len(sorted_languages) - 10} 种语言")

if __name__ == "__main__":
    main()
