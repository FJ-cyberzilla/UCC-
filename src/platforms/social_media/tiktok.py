"""
TikTok username checker with anti-detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class TikTokChecker(BasePlatform):
    """TikTok username checker with advanced anti-detection"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "tiktok"
        self.base_url = "https://www.tiktok.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check TikTok username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/@{normalized_username}"
        
        # TikTok requires specific headers to avoid blocking
        headers = self.anti_detection.generate_tiktok_headers()
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze TikTok response"""
        
        content = await response.text()
        
        # TikTok profile indicators
        profile_indicators = [
            '"userInfo":{',
            '"uniqueId":"',
            'tiktok.com/@' + username,
            'profile.avatar',
        ]
        
        # Not found indicators
        not_found_indicators = [
            '"type":"notfound"',
            'Couldn\'t find this account',
            'Page not found',
        ]
        
        if any(indicator in content for indicator in profile_indicators):
            return self.create_result(
                exists=True,
                confidence=0.92,
                url=f"https://www.tiktok.com/@{username}",
                method="http_advanced"
            )
        elif any(indicator in content for indicator in not_found_indicators):
            return self.create_result(
                exists=False,
                confidence=0.95,
                url=f"https://www.tiktok.com/@{username}",
                method="http_advanced"
            )
        else:
            # Check status code as fallback
            if response.status == 404:
                return self.create_result(
                    exists=False,
                    confidence=0.85,
                    url=f"https://www.tiktok.com/@{username}",
                    method="http_advanced"
                )
            elif response.status == 200:
                return self.create_result(
                    exists=True,
                    confidence=0.80,
                    url=f"https://www.tiktok.com/@{username}",
                    method="http_advanced"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.5,
                    url=f"https://www.tiktok.com/@{username}",
                    method="http_advanced",
                    error=f"Unexpected status: {response.status}"
                )
