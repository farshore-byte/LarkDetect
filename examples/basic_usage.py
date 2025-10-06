"""
Basic usage examples for Lark language detector
"""

from lark import LarkDetector, detect_language


def basic_example():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Initialize detector
    detector = LarkDetector()
    
    # Single text detection
    text = "Hello, how are you doing today?"
    language, confidence = detector.detect(text)
    print(f"Text: {text}")
    print(f"Detected: {language} (confidence: {confidence:.4f})")
    print()


def batch_example():
    """Batch detection example"""
    print("=== Batch Detection Example ===")
    
    detector = LarkDetector()
    
    texts = [
        "Hello world! This is an English text.",
        "今天的天气真不错，我们一起去公园散步吧！",
        "こんにちは！今日はどんな一日でしたか？",
        "Bonjour, comment allez-vous aujourd'hui ?",
        "¡Hola! ¿Cómo estás hoy?",
        "Привет! Как дела?",
        "Ciao! Come stai oggi?"
    ]
    
    results = detector.detect_batch(texts)
    
    for i, (text, (language, confidence)) in enumerate(zip(texts, results)):
        print(f"{i+1}. '{text[:30]:30}...' -> {language:6} (confidence: {confidence:.4f})")
    print()


def topk_example():
    """Top-k predictions example"""
    print("=== Top-K Predictions Example ===")
    
    detector = LarkDetector()
    
    text = "This is a sample text that might be ambiguous"
    language, confidence, top_k = detector.detect_with_topk(text, k=5)
    
    print(f"Text: {text}")
    print(f"Prediction: {language} (confidence: {confidence:.4f})")
    print("Top 5 predictions:")
    for i, item in enumerate(top_k):
        print(f"  {i+1}. {item['language']:8} - {item['probability']:.4f}")
    print()


def confidence_threshold_example():
    """Confidence threshold example"""
    print("=== Confidence Threshold Example ===")
    
    detector = LarkDetector()
    
    # Test with low confidence threshold
    text = "Short ambiguous text"
    language, confidence, top_k = detector.detect_with_confidence(
        text, confidence_threshold=0.3
    )
    print(f"Low threshold (0.3): '{text}' -> {language} (confidence: {confidence:.4f})")
    
    # Test with high confidence threshold
    language, confidence, top_k = detector.detect_with_confidence(
        text, confidence_threshold=0.9
    )
    print(f"High threshold (0.9): '{text}' -> {language} (confidence: {confidence:.4f})")
    print()


def supported_languages_example():
    """Supported languages example"""
    print("=== Supported Languages Example ===")
    
    detector = LarkDetector()
    languages = detector.get_supported_languages()
    
    print(f"Total supported languages: {len(languages)}")
    print("First 20 languages:")
    for i, lang in enumerate(languages[:20]):
        print(f"  {i+1:2d}. {lang}")
    print("... and many more!")
    print()


def convenience_function_example():
    """Convenience function example"""
    print("=== Convenience Function Example ===")
    
    text = "Hello world, this is a quick test!"
    language, confidence = detect_language(text)
    
    print(f"Text: {text}")
    print(f"Detected: {language} (confidence: {confidence:.4f})")
    print()


if __name__ == "__main__":
    basic_example()
    batch_example()
    topk_example()
    confidence_threshold_example()
    supported_languages_example()
    convenience_function_example()
