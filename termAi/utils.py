"""Utility functions for TermAI"""
import re

def tokenize(text):
    """Simple tokenization"""
    return re.findall(r'\w+', text.lower())

def preprocess_message(message):
    """Clean and prepare message for AI processing"""
    # Remove special characters, normalize
    cleaned = re.sub(r'[^\w\s]', '', message.lower())
    return cleaned.strip()

def is_question(message):
    """Check if message is a question"""
    return '?' in message

def extract_keywords(message):
    """Extract important keywords from message"""
    keywords = tokenize(message)
    # Filter common words
    stop_words = {'ir', 'kad', 'su', 'be', 'per', 'and', 'the', 'is', 'in', 'to'}
    return [word for word in keywords if word not in stop_words and len(word) > 2]

def similarity(text1, text2):
    """Simple text similarity"""
    words1 = set(tokenize(text1))
    words2 = set(tokenize(text2))
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0