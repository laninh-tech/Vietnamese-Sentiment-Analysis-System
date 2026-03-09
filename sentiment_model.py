import torch
from transformers import pipeline
from pyvi import ViTokenizer
import re


class SentimentModel:
    """
    Vietnamese Sentiment Classification using PhoBERT.
    
    This class wraps the pre-trained PhoBERT model for sentiment analysis
    of Vietnamese text, achieving >85% F1-score on benchmark datasets.
    
    Attributes:
        model_name (str): Hugging Face model ID for PhoBERT sentiment
        device (int): CUDA device ID (0) or CPU (-1)
        classifier (pipeline): Hugging Face sentiment-analysis pipeline
        loaded (bool): Whether model loaded successfully
    """
    
    def __init__(self):
        """Initialize SentimentModel with PhoBERT from Hugging Face."""
        # Using a fast, pre-trained Vietnamese sentiment model for demonstration
        # wonrax/phobert-base-vietnamese-sentiment is a good choice for PhoBERT sentiment tasks
        self.model_name = "wonrax/phobert-base-vietnamese-sentiment"
        self.device = 0 if torch.cuda.is_available() else -1
        try:
            # We use pipeline for direct abstraction over tokenization and inference
            self.classifier = pipeline("sentiment-analysis", model=self.model_name, device=self.device)
            self.loaded = True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.loaded = False

    def preprocess_text(self, text):
        """
        Clean and tokenize Vietnamese text for PhoBERT.
        
        Preprocessing steps:
        1. Convert to lowercase
        2. Remove URLs
        3. Remove special punctuation
        4. Tokenize using Vietnamese word segmentation (pyvi)
        
        Args:
            text (str): Raw Vietnamese text
            
        Returns:
            str: Preprocessed and tokenized text
        """
        if not text:
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # 3. Remove punctuation (optional, but sometimes helps with noisy social media text)
        text = re.sub(r'[^\w\s\.]', ' ', text)
        
        # 4. Tokenize (word segmentation) using pyvi
        # Example: "Hôm nay tôi buồn" -> "Hôm_nay tôi buồn"
        tokenized_text = ViTokenizer.tokenize(text)
        
        return tokenized_text

    def predict(self, text):
        """
        Predict sentiment label and confidence for given text.
        
        Args:
            text (str): Vietnamese text to analyze
            
        Returns:
            dict: Contains:
                - 'label' (str): 'Positive', 'Negative', or 'Neutral'
                - 'score' (float): Confidence score (0.0 - 1.0)
        """
        if not self.loaded or not text:
            return {'label': 'Neutral', 'score': 0.0}

        try:
            # First, preprocess the text
            clean_text = self.preprocess_text(text)
            
            # truncate to 256 tokens to avoid max length errors
            result = self.classifier(clean_text, truncation=True, max_length=256)[0]
            
            # map labels if needed (model specific: POS, NEG, NEU)
            label_map = {
                'POS': 'Positive',
                'NEG': 'Negative',
                'NEU': 'Neutral'
            }
            
            mapped_label = label_map.get(result['label'], result['label'])
            
            return {
                'label': mapped_label,
                'score': result['score']
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {'label': 'Neutral', 'score': 0.0}


# Singleton instance for the app
sentiment_engine = SentimentModel()


def analyze_text(text):
    """
    Convenience function to analyze text using the singleton sentiment engine.
    
    Args:
        text (str): Vietnamese text to analyze
        
    Returns:
        dict: Sentiment prediction result
    """
    return sentiment_engine.predict(text)
