"""
Tumblr username checker with blog detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class TumblrChecker(BasePlatform):
    """Tumblr username/blog availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "tumblr"
        self.base_url = "https://tumblr.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Tumblr username/blog availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"https://{normalized_username}.tumblr.com"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Tumblr response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Tumblr blog indicators
            if '.tumblr.com' in content and 'tumblr-theme' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.95,
                    url=f"https://{username}.tumblr.com",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.85,
                    url=f"https://{username}.tumblr.com",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.98,
                url=f"https://{username}.tumblr.com",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://{username}.tumblr.com",
                method="http",
                error=f"HTTP {response.status}"
            )
