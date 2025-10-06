#!/usr/bin/env python3
"""
Interactive demo for Lark language detector
"""

import sys
from lark import LarkDetector


def interactive_demo():
    """Interactive demo for language detection"""
    print("🚀 Lark Language Detection Demo")
    print("=" * 50)
    
    # Initialize detector
    print("Loading Lark model...")
    detector = LarkDetector()
    print(f"✅ Model loaded successfully!")
    print(f"✅ Supports {len(detector.get_supported_languages())} languages")
    print()
    
    while True:
        print("\nOptions:")
        print("1. Detect language from text")
        print("2. Batch detection from file")
        print("3. Show supported languages")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            single_text_detection(detector)
        elif choice == "2":
            batch_detection_from_file(detector)
        elif choice == "3":
            show_supported_languages(detector)
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def single_text_detection(detector):
    """Single text detection mode"""
    print("\n--- Single Text Detection ---")
    print("Enter text to detect language (or 'back' to return):")
    
    while True:
        text = input("\nText: ").strip()
        
        if text.lower() == 'back':
            break
        elif not text:
            print("❌ Please enter some text.")
            continue
        
        try:
            # Get detailed prediction
            language, confidence, top_k = detector.detect_with_topk(text, k=5)
            
            print(f"\n📊 Results:")
            print(f"  Predicted language: {language}")
            print(f"  Confidence: {confidence:.4f}")
            print(f"  Top 5 predictions:")
            for i, item in enumerate(top_k):
                print(f"    {i+1}. {item['language']:8} - {item['probability']:.4f}")
            
            # Test with confidence threshold
            threshold_lang, threshold_conf, _ = detector.detect_with_confidence(
                text, confidence_threshold=0.7
            )
            if threshold_lang == "unknown":
                print(f"  ⚠️  Low confidence (<0.7): {threshold_conf:.4f}")
            else:
                print(f"  ✅ High confidence (≥0.7): {threshold_conf:.4f}")
                
        except Exception as e:
            print(f"❌ Error during detection: {e}")


def batch_detection_from_file(detector):
    """Batch detection from file"""
    print("\n--- Batch Detection from File ---")
    print("Enter path to text file (one text per line):")
    
    file_path = input("File path: ").strip()
    
    if not file_path:
        print("❌ No file path provided.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        if not texts:
            print("❌ No valid texts found in file.")
            return
        
        print(f"📁 Processing {len(texts)} texts...")
        
        # Process in batches to avoid memory issues
        batch_size = 50
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_results = detector.detect_batch(batch_texts)
            results.extend(batch_results)
            
            progress = min(i + batch_size, len(texts))
            print(f"  Processed {progress}/{len(texts)} texts...")
        
        print("\n📊 Batch Results:")
        print("-" * 80)
        print(f"{'No.':<4} {'Text Preview':<30} {'Language':<10} {'Confidence':<10}")
        print("-" * 80)
        
        for i, (text, (language, confidence)) in enumerate(zip(texts, results)):
            preview = text[:28] + "..." if len(text) > 30 else text
            print(f"{i+1:<4} {preview:<30} {language:<10} {confidence:.4f}")
            
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")


def show_supported_languages(detector):
    """Show all supported languages"""
    print("\n--- Supported Languages ---")
    languages = detector.get_supported_languages()
    
    print(f"Total: {len(languages)} languages")
    print()
    
    # Group by first letter for better display
    grouped = {}
    for lang in languages:
        first_char = lang[0].upper() if lang else 'Other'
        if first_char not in grouped:
            grouped[first_char] = []
        grouped[first_char].append(lang)
    
    # Display in columns
    for letter in sorted(grouped.keys()):
        langs = sorted(grouped[letter])
        print(f"{letter}: {', '.join(langs)}")
    
    print(f"\nTotal: {len(languages)} languages")


if __name__ == "__main__":
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
