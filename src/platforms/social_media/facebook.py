"""
Facebook username checker with anti-detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class FacebookChecker(BasePlatform):
    """Facebook username checker with advanced anti-detection"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "facebook"
        self.base_url = "https://www.facebook.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Facebook username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        # Use mobile user agent to avoid strict detection
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            async with self.session.get(url, headers=headers, allow_redirects=True) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Facebook response"""
        
        content = await response.text()
        final_url = str(response.url)
        
        # Facebook redirects to login for private profiles or non-existent users
        if "login" in final_url or "facebook.com/login" in final_url:
            # Could be private profile or doesn't exist
            return self.create_result(
                exists=False,  # Assume not available for simplicity
                confidence=0.6,
                url=f"https://www.facebook.com/{username}",
                method="http",
                note="Redirected to login - profile may be private or non-existent"
            )
        
        # Check for profile indicators
        profile_indicators = [
            'fb://profile/',
            'content="profile"',
            'fb://page/',
            'entity_id'',
        ]
        
        # Check for "not found" indicators
        not_found_indicators = [
            'This content isn\'t available',
            'Page Not Found',
            'The link you followed may be broken',
        ]
        
        if any(indicator in content for indicator in profile_indicators):
            return self.create_result(
                exists=True,
                confidence=0.85,
                url=f"https://www.facebook.com/{username}",
                method="http"
            )
        elif any(indicator in content for indicator in not_found_indicators):
            return self.create_result(
                exists=False,
                confidence=0.90,
                url=f"https://www.facebook.com/{username}",
                method="http"
            )
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://www.facebook.com/{username}",
                method="http",
                note="Inconclusive - may require browser automation for accurate result"
            )
