"""
Advanced Leet Speak (1337) Detection and Normalization
Handles hacker/gamer username variations with character substitutions
"""

import re
import string
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import logging
from unidecode import unidecode

@dataclass
class LeetVariant:
    """Represents a leet speak variant"""
    original_char: str
    leet_substitutions: List[str]
    frequency: float  # How common this substitution is

class LeetProcessor:
    """
    Advanced leet speak processor for username normalization and detection
    Handles character substitutions, reversals, and advanced leet patterns
    """
    
    def __init__(self):
        self.leet_mapping = self._build_comprehensive_leet_map()
        self.patterns = self._build_leet_patterns()
        self.logger = logging.getLogger(__name__)
    
    def _build_comprehensive_leet_map(self) -> Dict[str, LeetVariant]:
        """Build comprehensive leet speak character mapping"""
        
        return {
            'a': LeetVariant('a', ['4', '@', '/\\', '^', '∂', 'λ', 'α'], 0.95),
            'b': LeetVariant('b', ['8', '6', '|3', 'ß', ']3', '13'], 0.85),
            'c': LeetVariant('c', ['(', '<', '{', '[', '©', '¢'], 0.80),
            'd': LeetVariant('d', ['|)', '|]', 'Ð', '∂', ']', 'Þ'], 0.75),
            'e': LeetVariant('e', ['3', '€', 'є', 'ë', '[-', 'ε'], 0.90),
            'f': LeetVariant('f', ['|=', 'ƒ', '|#', 'ph', '/=', 'v'], 0.70),
            'g': LeetVariant('g', ['9', '6', '&', '(_+', 'C-', 'gee'], 0.75),
            'h': LeetVariant('h', ['#', '4', '|-|', '}{', ']-[', ')-('], 0.85),
            'i': LeetVariant('i', ['1', '!', '|', '][', 'ι', 'eye'], 0.90),
            'j': LeetVariant('j', ['_|', '_/', ']', ';', '¿', 'ʝ'], 0.65),
            'k': LeetVariant('k', ['X', '|<', '|{', ']{', '‖', 'κ'], 0.70),
            'l': LeetVariant('l', ['1', '|_', '|', '£', 'ℓ', '¬'], 0.85),
            'm': LeetVariant('m', ['|\\/|', '/\\/\\', 'em', ']\\/[', '(v)', '^^'], 0.80),
            'n': LeetVariant('n', ['|\\|', '/\\/', 'И', '^/', ']\\[', '₪'], 0.80),
            'o': LeetVariant('o', ['0', '()', '[]', 'Ω', 'θ', '°'], 0.95),
            'p': LeetVariant('p', ['|*', '|o', '|>', '|7', '¶', 'þ'], 0.75),
            'q': LeetVariant('q', ['0_', '9', '(_,)', 'O,', '¶', 'ℚ'], 0.60),
            'r': LeetVariant('r', ['|2', '|?', '|^', 'lz', '®', 'ʁ'], 0.80),
            's': LeetVariant('s', ['5', '$', 'z', '§', '_/', 'es'], 0.90),
            't': LeetVariant('t', ['7', '+', '†', '´|`', '~|~', '‡'], 0.85),
            'u': LeetVariant('u', ['|_|', '(_)', 'µ', 'บ', 'û', '∪'], 0.75),
            'v': LeetVariant('v', ['\\/', '|/', '‖', '√', '\\\\//', 'υ'], 0.70),
            'w': LeetVariant('w', ['\\/\\/', 'vv', '\\^/', '\\X/', 'ω', 'ψ'], 0.75),
            'x': LeetVariant('x', ['><', '}{', '×', ')(', '‡', 'χ'], 0.80),
            'y': LeetVariant('y', ['`/', '¥', '\\|/', 'φ', 'λ', 'Ч'], 0.70),
            'z': LeetVariant('z', ['2', '~/_', '%', '≥', '≠', 'ζ'], 0.65),
            
            # Numbers that are often used as letters
            '0': LeetVariant('o', ['o', 'O', '()'], 0.90),
            '1': LeetVariant('i', ['i', 'I', 'l', '|'], 0.95),
            '3': LeetVariant('e', ['e', 'E'], 0.90),
            '4': LeetVariant('a', ['a', 'A'], 0.95),
            '5': LeetVariant('s', ['s', 'S'], 0.90),
            '7': LeetVariant('t', ['t', 'T'], 0.85),
            '8': LeetVariant('b', ['b', 'B'], 0.80),
            '9': LeetVariant('g', ['g', 'G'], 0.75),
        }
    
    def _build_leet_patterns(self) -> Dict[str, str]:
        """Build regex patterns for common leet speak patterns"""
        
        return {
            'basic_leet': r'[4@][5$][5$]',  # "ass" pattern
            'elite_leet': r'[|\\\/][3€][3€]7',  # "leet" in elite form
            'hacker_pattern': r'[xX][dD]|[lL][oO][lL]',  # "xd", "lol"
            'number_substitution': r'\d[^\w\s]+\d',  # numbers with symbols
            'repeated_symbols': r'([^\w\s])\1{2,}',  # repeated symbols like !!!
            'word_with_numbers': r'\b\w*\d+\w*\b',  # words containing numbers
            'symbol_separation': r'\w[^\w\s]+\w',  # symbols between letters
        }
    
    def is_leet_username(self, username: str) -> bool:
        """
        Detect if a username contains leet speak patterns
        
        Args:
            username: The username to check
            
        Returns:
            bool: True if leet patterns are detected
        """
        
        if not username or len(username) < 2:
            return False
        
        # Check for common leet patterns
        for pattern_name, pattern in self.patterns.items():
            if re.search(pattern, username, re.IGNORECASE):
                return True
        
        # Check character-level leet substitutions
        leet_char_count = 0
        for char in username.lower():
            if char in self.leet_mapping:
                leet_char_count += 1
        
        # If more than 30% of characters are potential leet substitutions
        leet_ratio = leet_char_count / len(username)
        if leet_ratio > 0.3:
            return True
        
        # Check for mixed alphanumeric patterns (common in leet)
        if re.search(r'[a-zA-Z]+\d+[a-zA-Z]*|\d+[a-zA-Z]+\d*', username):
            return True
        
        return False
    
    def normalize_leet_username(self, username: str, aggressive: bool = False) -> str:
        """
        Normalize leet speak username to standard characters
        
        Args:
            username: The leet username to normalize
            aggressive: Whether to use aggressive normalization (may lose information)
            
        Returns:
            str: Normalized username
        """
        
        if not self.is_leet_username(username):
            return username.lower()
        
        normalized = username.lower()
        
        # Phase 1: Simple character substitutions
        normalized = self._apply_character_substitutions(normalized)
        
        # Phase 2: Pattern-based normalization
        normalized = self._apply_pattern_normalization(normalized)
        
        # Phase 3: Aggressive normalization if requested
        if aggressive:
            normalized = self._apply_aggressive_normalization(normalized)
        
        # Phase 4: Clean up and finalize
        normalized = self._cleanup_normalized_username(normalized)
        
        return normalized
    
    def _apply_character_substitutions(self, username: str) -> str:
        """Apply character-level leet substitutions"""
        
        result = []
        i = 0
        username_lower = username.lower()
        
        while i < len(username_lower):
            char = username_lower[i]
            remaining = len(username_lower) - i
            
            # Check multi-character substitutions first (most specific)
            substituted = False
            
            # Check 2-character sequences
            if remaining >= 2:
                two_chars = username_lower[i:i+2]
                for original, variant in self.leet_mapping.items():
                    for sub in variant.leet_substitutions:
                        if len(sub) == 2 and two_chars == sub.lower():
                            result.append(original)
                            i += 2
                            substituted = True
                            break
                    if substituted:
                        break
            
            # Check 3-character sequences  
            if not substituted and remaining >= 3:
                three_chars = username_lower[i:i+3]
                for original, variant in self.leet_mapping.items():
                    for sub in variant.leet_substitutions:
                        if len(sub) == 3 and three_chars == sub.lower():
                            result.append(original)
                            i += 3
                            substituted = True
                            break
                    if substituted:
                        break
            
            # Single character substitution
            if not substituted:
                if char in self.leet_mapping:
                    result.append(self.leet_mapping[char].original_char)
                else:
                    result.append(char)
                i += 1
        
        return ''.join(result)
    
    def _apply_pattern_normalization(self, username: str) -> str:
        """Apply pattern-based normalization"""
        
        # Common leet word patterns
        pattern_replacements = {
            r'ph': 'f',
            r'ck': 'k', 
            r'qu': 'q',
            r'^ex': 'x',
            r'z$': 's',
            r'([aeiou])\1+': r'\1',  # Reduce repeated vowels
            r'([^aeiou])\1+': r'\1',  # Reduce repeated consonants
        }
        
        normalized = username
        for pattern, replacement in pattern_replacements.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        return normalized
    
    def _apply_aggressive_normalization(self, username: str) -> str:
        """Apply aggressive normalization (may lose some information)"""
        
        # Remove all non-alphanumeric characters (except underscores)
        normalized = re.sub(r'[^a-z0-9_]', '', username)
        
        # Common aggressive substitutions
        aggressive_subs = {
            '0': 'o',
            '1': 'i', 
            '3': 'e',
            '4': 'a',
            '5': 's',
            '7': 't',
            '8': 'b',
            '9': 'g',
        }
        
        for num, letter in aggressive_subs.items():
            normalized = normalized.replace(num, letter)
        
        return normalized
    
    def _cleanup_normalized_username(self, username: str) -> str:
        """Clean up and finalize normalized username"""
        
        # Remove excessive repeated characters (more than 2)
        cleaned = re.sub(r'(.)\1{2,}', r'\1\1', username)
        
        # Ensure it's lowercase
        cleaned = cleaned.lower()
        
        # Remove leading/trailing special characters
        cleaned = cleaned.strip('_-.')
        
        return cleaned
    
    def generate_leet_variants(self, username: str, max_variants: int = 10) -> List[str]:
        """
        Generate possible leet speak variants of a username
        
        Args:
            username: Original username to generate variants for
            max_variants: Maximum number of variants to generate
            
        Returns:
            List of possible leet variants
        """
        
        if not username:
            return []
        
        variants = set()
        username_lower = username.lower()
        
        # Generate variants by substituting common characters
        for i, char in enumerate(username_lower):
            if char in self.leet_mapping:
                variant = self.leet_mapping[char]
                for sub in variant.leet_substitutions[:3]:  # Top 3 most common
                    new_username = (username_lower[:i] + sub + 
                                  username_lower[i+1:])
                    variants.add(new_username)
                    
                    if len(variants) >= max_variants:
                        return list(variants)
        
        return list(variants)[:max_variants]
    
    def get_leet_confidence(self, username: str) -> float:
        """
        Calculate confidence score that a username contains leet speak
        
        Args:
            username: Username to analyze
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        
        if not username or len(username) < 2:
            return 0.0
        
        score_components = []
        
        # 1. Character substitution score
        leet_chars = 0
        for char in username.lower():
            if char in self.leet_mapping:
                leet_chars += 1
        
        char_score = leet_chars / len(username)
        score_components.append(char_score * 0.4)
        
        # 2. Pattern matching score
        pattern_matches = 0
        for pattern in self.patterns.values():
            if re.search(pattern, username, re.IGNORECASE):
                pattern_matches += 1
        
        pattern_score = min(pattern_matches / len(self.patterns), 1.0)
        score_components.append(pattern_score * 0.3)
        
        # 3. Alphanumeric mix score
        alpha_count = sum(1 for c in username if c.isalpha())
        digit_count = sum(1 for c in username if c.isdigit())
        symbol_count = len(username) - alpha_count - digit_count
        
        if alpha_count > 0 and digit_count > 0:
            mix_score = 0.7
        elif symbol_count > 0:
            mix_score = 0.5
        else:
            mix_score = 0.0
        
        score_components.append(mix_score * 0.3)
        
        return min(sum(score_components), 1.0)
    
    def analyze_leet_username(self, username: str) -> Dict[str, any]:
        """
        Comprehensive analysis of a potential leet username
        
        Args:
            username: Username to analyze
            
        Returns:
            Dict with analysis results
        """
        
        return {
            'original_username': username,
            'is_leet': self.is_leet_username(username),
            'confidence': self.get_leet_confidence(username),
            'normalized': self.normalize_leet_username(username),
            'aggressive_normalized': self.normalize_leet_username(username, aggressive=True),
            'common_variants': self.generate_leet_variants(username, 5),
            'character_analysis': self._analyze_leet_characters(username)
        }
    
    def _analyze_leet_characters(self, username: str) -> Dict[str, any]:
        """Analyze leet character usage in username"""
        
        analysis = {
            'total_chars': len(username),
            'leet_chars': 0,
            'substitutions': [],
            'most_common_substitutions': []
        }
        
        for char in username.lower():
            if char in self.leet_mapping:
                analysis['leet_chars'] += 1
                variant = self.leet_mapping[char]
                analysis['substitutions'].append({
                    'original': variant.original_char,
                    'leet_char': char,
                    'frequency': variant.frequency
                })
        
        # Find most common substitutions
        if analysis['substitutions']:
            sorted_subs = sorted(analysis['substitutions'], 
                               key=lambda x: x['frequency'], reverse=True)
            analysis['most_common_substitutions'] = sorted_subs[:3]
        
        analysis['leet_ratio'] = analysis['leet_chars'] / analysis['total_chars']
        
        return analysis

class AdvancedUsernameProcessor:
    """
    Advanced username processor with leet speak handling
    Integrates with the main username checking system
    """
    
    def __init__(self):
        self.leet_processor = LeetProcessor()
        self.logger = logging.getLogger(__name__)
    
    def process_username(self, username: str, platform: str = None) -> Dict[str, any]:
        """
        Process a username with advanced leet speak handling
        
        Args:
            username: Username to process
            platform: Target platform (for platform-specific rules)
            
        Returns:
            Dict with processing results
        """
        
        # Basic cleaning
        cleaned_username = self._clean_username(username)
        
        # Leet speak analysis
        leet_analysis = self.leet_processor.analyze_leet_username(cleaned_username)
        
        # Platform-specific processing
        platform_variants = self._get_platform_variants(cleaned_username, platform)
        
        return {
            'original': username,
            'cleaned': cleaned_username,
            'leet_analysis': leet_analysis,
            'platform_variants': platform_variants,
            'checking_recommendations': self._get_checking_recommendations(leet_analysis, platform)
        }
    
    def _clean_username(self, username: str) -> str:
        """Basic username cleaning"""
        
        if not username:
            return ""
        
        # Remove extra whitespace
        cleaned = username.strip()
        
        # Remove excessive special characters (keep only common ones)
        cleaned = re.sub(r'[^\w\-_.]', '', cleaned)
        
        # Limit length (reasonable username length)
        if len(cleaned) > 30:
            cleaned = cleaned[:30]
        
        return cleaned
    
    def _get_platform_variants(self, username: str, platform: str) -> List[str]:
        """Get platform-specific username variants"""
        
        variants = set()
        
        # Always include the cleaned username
        variants.add(username.lower())
        
        # Platform-specific rules
        if platform in ['instagram', 'tiktok', 'twitter']:
            # These platforms often have case variations
            variants.add(username.upper())
            variants.add(username.title())
        
        if platform in ['github', 'reddit']:
            # Tech platforms may have different normalization
            variants.add(username.replace('-', '_'))
            variants.add(username.replace('_', '-'))
        
        # Add leet variants for comprehensive checking
        if self.leet_processor.is_leet_username(username):
            leet_variants = self.leet_processor.generate_leet_variants(username, 3)
            variants.update(leet_variants)
        
        return list(variants)
    
    def _get_checking_recommendations(self, leet_analysis: Dict, platform: str) -> List[str]:
        """Get recommendations for username checking strategy"""
        
        recommendations = []
        
        if leet_analysis['is_leet']:
            confidence = leet_analysis['confidence']
            
            if confidence > 0.7:
                recommendations.extend([
                    "Check normalized version primarily",
                    "Also check common leet variants",
                    "Consider aggressive normalization for difficult platforms"
                ])
            elif confidence > 0.3:
                recommendations.extend([
                    "Check both original and normalized versions",
                    "Generate and check a few leet variants"
                ])
            else:
                recommendations.append("Standard checking should be sufficient")
        
        # Platform-specific recommendations
        if platform in ['instagram', 'facebook']:
            recommendations.append("These platforms are strict - use normalized versions")
        elif platform in ['github', 'reddit']:
            recommendations.append("Tech platforms may accept various leet forms")
        
        return recommendations

# Example usage and testing
def demonstrate_leet_processing():
    """Demonstrate leet speak processing capabilities"""
    
    processor = AdvancedUsernameProcessor()
    
    # Test cases with various leet usernames
    test_usernames = [
        "xX_dark_5h4d0w_Xx",  # Mixed leet
        "4lph4_num3r1c",      # Basic leet
        "|_33t_h4x0r",        # Advanced leet
        "normal_user",        # Normal username
        "j0hn_do3",           # Simple leet
        "\\/\\/4r10r",        # Complex leet
        "abc123",             # Alphanumeric
        "user_name",          # Standard
    ]
    
    print("🔤 Advanced Leet Speak Processing Demo")
    print("=" * 60)
    
    for username in test_usernames:
        result = processor.process_username(username, "instagram")
        leet_info = result['leet_analysis']
        
        status = "✅ LEET" if leet_info['is_leet'] else "❌ NORMAL"
        confidence = f"{leet_info['confidence']:.0%}"
        normalized = leet_info['normalized']
        
        print(f"\n👤 Username: {username}")
        print(f"   Status: {status}")
        print(f"   Confidence: {confidence}")
        print(f"   Normalized: {normalized}")
        print(f"   Variants: {', '.join(result['platform_variants'][:3])}")
        
        if leet_info['is_leet']:
            print(f"   Recommendations: {', '.join(result['checking_recommendations'])}")

if __name__ == "__main__":
    demonstrate_leet_processing()
