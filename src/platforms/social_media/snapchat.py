"""
Snapchat username checker with advanced detection
"""

import aiohttp
import re
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class SnapchatChecker(BasePlatform):
    """Snapchat username checker with sophisticated detection"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "snapchat"
        self.base_url = "https://www.snapchat.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Snapchat username with advanced techniques"""
        
        normalized_username = self.normalize_username(username)
        
        # Snapchat uses multiple endpoints for validation
        endpoints = [
            f"https://www.snapchat.com/add/{normalized_username}",
            f"https://story.snapchat.com/@{normalized_username}"
        ]
        
        headers = self.anti_detection.generate_snapchat_headers()
        
        for endpoint in endpoints:
            try:
                async with self.session.get(endpoint, headers=headers, allow_redirects=True) as response:
                    result = await self.analyze_snapchat_response(response, normalized_username, endpoint)
                    if result['confidence'] > 0.8:
                        return result
            except Exception:
                continue
        
        return self.create_result(
            exists=False,
            confidence=0.3,
            method="http_advanced",
            note="Snapchat requires sophisticated detection. Try browser automation."
        )
    
    async def analyze_snapchat_response(self, response, username: str, endpoint: str) -> Dict[str, Any]:
        """Advanced Snapchat response analysis"""
        
        content = await response.text()
        final_url = str(response.url)
        
        # Snapchat-specific patterns
        profile_patterns = [
            r'snapchat\.com/add/' + re.escape(username),
            r'\"username\"\s*:\s*\"' + re.escape(username) + '\"',
            r'displayName.*' + re.escape(username),
        ]
        
        not_found_patterns = [
            r'user not found',
            r'couldn\'t find',
            r'page not found',
            r'error.*404',
        ]
        
        # Check for profile indicators
        for pattern in profile_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return self.create_result(
                    exists=True,
                    confidence=0.85,
                    url=f"https://www.snapchat.com/add/{username}",
                    method="http_advanced"
                )
        
        # Check for not found indicators
        for pattern in not_found_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return self.create_result(
                    exists=False,
                    confidence=0.88,
                    url=f"https://www.snapchat.com/add/{username}",
                    method="http_advanced"
                )
        
        # Analyze URL patterns
        if 'add/' in final_url and username in final_url:
            return self.create_result(
                exists=True,
                confidence=0.75,
                url=final_url,
                method="http_advanced"
            )
        
        return self.create_result(
            exists=False,
            confidence=0.5,
            url=endpoint,
            method="http_advanced",
            note="Inconclusive - Snapchat has strong anti-bot measures"
        )
