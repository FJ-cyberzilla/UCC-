"""
AI-Powered Captcha Solving with Multi-Engine Support
"""

import asyncio
import io
import base64
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from typing import Dict, List, Optional, Tuple
import logging
import aiohttp
import json

# Try to import ML libraries
try:
    import tensorflow as tf
    from tensorflow import keras
    ML_CAPTCHA_AVAILABLE = True
except ImportError:
    ML_CAPTCHA_AVAILABLE = False

try:
    import torch
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class AICaptchaSolver:
    """Advanced AI-powered captcha solving with multiple engines"""
    
    def __init__(self):
        self.solving_engines = []
        self.success_rates = {}
        self.ml_models = {}
        self.logger = logging.getLogger(__name__)
        
        self._initialize_engines()
        self._setup_image_preprocessors()
    
    def _initialize_engines(self):
        """Initialize multiple captcha solving engines"""
        
        self.solving_engines = [
            {
                'name': 'tesseract_advanced',
                'description': 'Advanced Tesseract OCR with preprocessing',
                'function': self._solve_with_tesseract_advanced,
                'weight': 0.8,
                'supported_types': ['text', 'numbers', 'alphanumeric']
            },
            {
                'name': 'contour_analysis',
                'description': 'Character contour detection and analysis',
                'function': self._solve_with_contour_analysis,
                'weight': 0.7,
                'supported_types': ['text', 'numbers']
            },
            {
                'name': 'neural_network',
                'description': 'Neural network-based recognition',
                'function': self._solve_with_neural_network,
                'weight': 0.9,
                'supported_types': ['text', 'numbers', 'alphanumeric', 'image_recognition']
            },
            {
                'name': 'pattern_matching',
                'description': 'Pattern matching and template comparison',
                'function': self._solve_with_pattern_matching,
                'weight': 0.6,
                'supported_types': ['simple_text', 'numbers']
            }
        ]
        
        # Initialize success rates
        for engine in self.solving_engines:
            self.success_rates[engine['name']] = 0.5  # Initial assumption
    
    def _setup_image_preprocessors(self):
        """Setup image preprocessing pipelines"""
        
        self.preprocessors = {
            'basic': self._basic_preprocessing,
            'advanced': self._advanced_preprocessing,
            'neural_net': self._neural_net_preprocessing,
            'aggressive': self._aggressive_preprocessing
        }
    
    async def solve_captcha(self, image_data: bytes, captcha_type: str = 'auto') -> Dict[str, any]:
        """Solve captcha using multiple AI engines with confidence scoring"""
        
        # Preprocess image based on detected captcha type
        processed_images = await self._preprocess_image(image_data, captcha_type)
        
        results = []
        total_weight = 0
        
        for engine in self.solving_engines:
            if captcha_type in engine['supported_types'] or captcha_type == 'auto':
                try:
                    engine_result = await engine['function'](processed_images, captcha_type)
                    engine_result['engine'] = engine['name']
                    engine_result['weight'] = engine['weight']
                    
                    results.append(engine_result)
                    total_weight += engine['weight']
                    
                except Exception as e:
                    self.logger.warning(f"Engine {engine['name']} failed: {e}")
        
        if not results:
            return {
                'solved': False,
                'text': '',
                'confidence': 0.0,
                'error': 'No engines could process the captcha'
            }
        
        # Weighted consensus from multiple engines
        final_result = await self._calculate_consensus(results, total_weight)
        
        # Update engine success rates
        await self._update_success_rates(results, final_result['confidence'] > 0.7)
        
        return final_result
    
    async def _preprocess_image(self, image_data: bytes, captcha_type: str) -> Dict[str, Image.Image]:
        """Preprocess image with multiple techniques"""
        
        try:
            # Convert to PIL Image
            original_image = Image.open(io.BytesIO(image_data))
            processed_images = {'original': original_image}
            
            # Apply different preprocessing techniques
            for name, preprocessor in self.preprocessors.items():
                processed_images[name] = await preprocessor(original_image)
            
            return processed_images
            
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            # Return original image as fallback
            original_image = Image.open(io.BytesIO(image_data))
            return {'original': original_image}
    
    def _basic_preprocessing(self, image: Image.Image) -> Image.Image:
        """Basic image preprocessing"""
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def _advanced_preprocessing(self, image: Image.Image) -> Image.Image:
        """Advanced preprocessing for difficult captchas"""
        
        # Convert to numpy for OpenCV processing
        img_array = np.array(image)
        
        # Noise reduction
        img_array = cv2.medianBlur(img_array, 3)
        
        # Thresholding
        _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel)
        
        # Convert back to PIL
        return Image.fromarray(img_array)
    
    def _neural_net_preprocessing(self, image: Image.Image) -> Image.Image:
        """Preprocessing optimized for neural networks"""
        
        # Resize to standard size
        image = image.resize((200, 60), Image.Resampling.LANCZOS)
        
        # Normalize
        img_array = np.array(image) / 255.0
        
        # Convert back to PIL
        return Image.fromarray((img_array * 255).astype(np.uint8))
    
    def _aggressive_preprocessing(self, image: Image.Image) -> Image.Image:
        """Aggressive preprocessing for very noisy captchas"""
        
        img_array = np.array(image)
        
        # Multiple denoising steps
        img_array = cv2.fastNlMeansDenoising(img_array)
        img_array = cv2.GaussianBlur(img_array, (3, 3), 0)
        
        # Adaptive threshold
        img_array = cv2.adaptiveThreshold(
            img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Erosion and dilation
        kernel = np.ones((1, 1), np.uint8)
        img_array = cv2.erode(img_array, kernel, iterations=1)
        img_array = cv2.dilate(img_array, kernel, iterations=1)
        
        return Image.fromarray(img_array)
    
    async def _solve_with_tesseract_advanced(self, processed_images: Dict, captcha_type: str) -> Dict:
        """Solve using advanced Tesseract OCR"""
        
        best_result = {'text': '', 'confidence': 0.0}
        
        # Try different preprocessing combinations
        for preprocess_name, image in processed_images.items():
            # Configure Tesseract based on captcha type
            config = self._get_tesseract_config(captcha_type)
            
            try:
                text = pytesseract.image_to_string(image, config=config).strip()
                confidence_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                
                # Calculate average confidence
                if confidence_data['conf']:
                    avg_confidence = np.mean([c for c in confidence_data['conf'] if c > 0]) / 100.0
                else:
                    avg_confidence = 0.5
                
                if avg_confidence > best_result['confidence'] and len(text) >= 3:
                    best_result = {'text': text, 'confidence': avg_confidence}
                    
            except Exception as e:
                continue
        
        return best_result
    
    def _get_tesseract_config(self, captcha_type: str) -> str:
        """Get Tesseract configuration for specific captcha type"""
        
        configs = {
            'numbers': '--psm 8 -c tessedit_char_whitelist=0123456789',
            'text': '--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'alphanumeric': '--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            'auto': '--psm 8'
        }
        
        return configs.get(captcha_type, '--psm 8')
    
    async def _solve_with_contour_analysis(self, processed_images: Dict, captcha_type: str) -> Dict:
        """Solve using character contour analysis"""
        
        try:
            # Use the best preprocessed image
            image = processed_images.get('advanced', processed_images['original'])
            img_array = np.array(image)
            
            # Find contours
            contours, _ = cv2.findContours(img_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Sort contours left to right
            contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
            
            characters = []
            total_confidence = 0
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter out noise
                if w > 5 and h > 10 and w < 100 and h < 100:
                    char_image = img_array[y:y+h, x:x+w]
                    
                    # Recognize character
                    char_result = self._recognize_character(char_image)
                    if char_result:
                        characters.append(char_result['char'])
                        total_confidence += char_result['confidence']
            
            if characters:
                text = ''.join(characters)
                avg_confidence = total_confidence / len(characters)
                return {'text': text, 'confidence': avg_confidence}
            else:
                return {'text': '', 'confidence': 0.0}
                
        except Exception as e:
            self.logger.error(f"Contour analysis failed: {e}")
            return {'text': '', 'confidence': 0.0}
    
    def _recognize_character(self, char_image: np.ndarray) -> Optional[Dict]:
        """Recognize single character using multiple methods"""
        
        # Method 1: Template matching (simplified)
        # In production, this would use actual template databases
        
        # Method 2: Tesseract on single character
        try:
            char_pil = Image.fromarray(char_image)
            text = pytesseract.image_to_string(char_pil, config='--psm 10').strip()
            if text and len(text) == 1:
                return {'char': text, 'confidence': 0.7}
        except:
            pass
        
        return None
    
    async def _solve_with_neural_network(self, processed_images: Dict, captcha_type: str) -> Dict:
        """Solve using neural network (if available)"""
        
        if not ML_CAPTCHA_AVAILABLE:
            return {'text': '', 'confidence': 0.0, 'note': 'ML libraries not available'}
        
        try:
            # This would integrate with a pre-trained neural network
            # For now, return a placeholder implementation
            
            # Use preprocessed image for neural network
            image = processed_images.get('neural_net', processed_images['original'])
            img_array = np.array(image) / 255.0
            
            # Placeholder for actual neural network prediction
            # In production, this would load a trained model
            predicted_text = "NNOTAVAIL"  # Placeholder
            confidence = 0.6  # Placeholder confidence
            
            return {'text': predicted_text, 'confidence': confidence}
            
        except Exception as e:
            self.logger.error(f"Neural network solving failed: {e}")
            return {'text': '', 'confidence': 0.0}
    
    async def _solve_with_pattern_matching(self, processed_images: Dict, captcha_type: str) -> Dict:
        """Solve using pattern matching"""
        
        try:
            image = processed_images.get('basic', processed_images['original'])
            
            # Simple pattern matching implementation
            # This would be expanded with actual pattern databases
            
            return {'text': '', 'confidence': 0.3, 'note': 'Pattern matching not fully implemented'}
            
        except Exception as e:
            return {'text': '', 'confidence': 0.0}
    
    async def _calculate_consensus(self, results: List[Dict], total_weight: float) -> Dict:
        """Calculate weighted consensus from multiple engine results"""
        
        if not results:
            return {'solved': False, 'text': '', 'confidence': 0.0}
        
        # Group by text results
        text_groups = {}
        
        for result in results:
            text = result['text'].strip()
            if text:  # Only consider non-empty results
                if text not in text_groups:
                    text_groups[text] = {
                        'total_confidence': 0.0,
                        'total_weight': 0.0,
                        'engines': []
                    }
                
                text_groups[text]['total_confidence'] += result['confidence'] * result['weight']
                text_groups[text]['total_weight'] += result['weight']
                text_groups[text]['engines'].append(result['engine'])
        
        if not text_groups:
            return {'solved': False, 'text': '', 'confidence': 0.0}
        
        # Find the text with highest weighted confidence
        best_text = max(text_groups.items(), 
                       key=lambda x: x[1]['total_confidence'] / x[1]['total_weight'])
        
        text, data = best_text
        avg_confidence = data['total_confidence'] / data['total_weight']
        
        return {
            'solved': True,
            'text': text,
            'confidence': avg_confidence,
            'engines_used': data['engines'],
            'consensus_method': 'weighted_average'
        }
    
    async def _update_success_rates(self, results: List[Dict], was_successful: bool):
        """Update engine success rates based on performance"""
        
        for result in results:
            engine_name = result['engine']
            current_rate = self.success_rates.get(engine_name, 0.5)
            
            # Simple moving average update
            alpha = 0.1  # Learning rate
            if was_successful:
                new_rate = (1 - alpha) * current_rate + alpha * 1.0
            else:
                new_rate = (1 - alpha) * current_rate + alpha * 0.0
            
            self.success_rates[engine_name] = new_rate
    
    async def solve_interactive_captcha(self, captcha_url: str, session: aiohttp.ClientSession) -> Dict:
        """Solve interactive captchas (like reCAPTCHA) - requires advanced techniques"""
        
        # This would implement advanced techniques for interactive captchas
        # Including audio challenges, image recognition, etc.
        
        return {
            'solved': False,
            'text': '',
            'confidence': 0.0,
            'error': 'Interactive captcha solving requires advanced implementation',
            'note': 'Consider using captcha solving services for production use'
        }
