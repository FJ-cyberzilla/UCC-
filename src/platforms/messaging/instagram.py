"""
Instagram platform checker with advanced anti-detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class InstagramChecker(BasePlatform):
    """Instagram username checker with anti-detection measures"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "instagram"
        self.base_url = "https://www.instagram.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Instagram username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}/"
        
        # Use advanced anti-detection headers
        headers = self.anti_detection.generate_instagram_headers()
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Instagram response for username availability"""
        
        content = await response.text()
        
        # Instagram-specific indicators
        profile_indicators = [
            'profilePage_',
            '"@context":"https://schema.org"',
            'og:title',
            'profile-header',
        ]
        
        not_found_indicators = [
            'Sorry, this page isn\'t available',
            'The link you followed may be broken',
            '"HttpErrorPage"',
            'Page Not Found'
        ]
        
        exists = any(indicator in content for indicator in profile_indicators)
        not_found = any(indicator in content for indicator in not_found_indicators)
        
        if not_found:
            return self.create_result(
                exists=False,
                confidence=0.95,
                url=f"https://www.instagram.com/{username}",
                method="http_advanced"
            )
        elif exists:
            return self.create_result(
                exists=True,
                confidence=0.98,
                url=f"https://www.instagram.com/{username}",
                method="http_advanced",
                additional_info=self.extract_profile_info(content)
            )
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://www.instagram.com/{username}",
                method="http_advanced",
                note="Uncertain result - may require browser check"
            )
    
    def extract_profile_info(self, content: str) -> Dict[str, Any]:
        """Extract basic profile info from page content"""
        # This would parse the Instagram page for additional info
        return {
            "platform": "instagram",
            "note": "Profile information available via browser automation"
        }
