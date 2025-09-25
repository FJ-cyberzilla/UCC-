"""
LinkedIn username checker with advanced handling
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class LinkedInChecker(BasePlatform):
    """LinkedIn username checker with auth wall handling"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "linkedin"
        self.base_url = "https://linkedin.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check LinkedIn username availability"""
        
        normalized_username = self.normalize_username(username)
        
        # Try multiple URL formats
        urls = [
            f"{self.base_url}/in/{normalized_username}",
            f"{self.base_url}/pub/{normalized_username}"
        ]
        
        headers = self.anti_detection.generate_linkedin_headers()
        
        for url in urls:
            try:
                async with self.session.get(url, headers=headers, allow_redirects=True) as response:
                    result = await self.analyze_response(response, normalized_username, url)
                    if result['confidence'] > 0.7:  # Accept confident result
                        return result
                        
            except Exception as e:
                continue
        
        return self.create_error_result("All URL attempts failed")
    
    async def analyze_response(self, response, username: str, url: str) -> Dict[str, Any]:
        """Analyze LinkedIn response with auth wall detection"""
        
        content = await response.text()
        final_url = str(response.url)
        
        # Check for login redirect (auth wall)
        if "login" in final_url or "auth" in final_url:
            # Auth wall often means profile exists but requires login
            return self.create_result(
                exists=True,
                confidence=0.75,
                url=url,
                method="http_advanced",
                note="Profile likely exists but requires authentication to view"
            )
        
        # Check for profile indicators
        profile_indicators = [
            'profile-topcard',
            'pv-top-card',
            'profile-info',
            '"@type":"Person"'
        ]
        
        # Check for "not found" indicators
        not_found_indicators = [
            'This profile doesn\'t exist',
            '404',
            'Page not found'
        ]
        
        if any(indicator in content for indicator in profile_indicators):
            return self.create_result(
                exists=True,
                confidence=0.90,
                url=url,
                method="http_advanced"
            )
        elif any(indicator in content for indicator in not_found_indicators):
            return self.create_result(
                exists=False,
                confidence=0.85,
                url=url,
                method="http_advanced"
            )
        else:
            return self.create_result(
                exists=False,
                confidence=0.6,
                url=url,
                method="http_advanced",
                note="Inconclusive - LinkedIn often requires browser automation"
            )
