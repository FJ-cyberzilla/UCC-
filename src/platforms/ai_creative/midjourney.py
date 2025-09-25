"""
Midjourney username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class MidjourneyChecker(BasePlatform):
    """Midjourney username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "midjourney"
        self.base_url = "https://midjourney.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Midjourney username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/app/users/{normalized_username}"
        
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
        """Analyze Midjourney response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Midjourney profile indicators
            if 'midjourney.com/app/users/' in content and 'profile' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.89,
                    url=f"https://midjourney.com/app/users/{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.82,
                    url=f"https://midjourney.com/app/users/{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.93,
                url=f"https://midjourney.com/app/users/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://midjourney.com/app/users/{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
