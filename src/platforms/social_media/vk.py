"""
VK (VKontakte) username checker with Russian social network support
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class VKChecker(BasePlatform):
    """VKontakte username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "vk"
        self.base_url = "https://vk.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check VK username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze VK response"""
        
        if response.status == 200:
            content = await response.text()
            
            # VK profile indicators (Russian language)
            if 'vk.com/' + username in content and ('профиль' in content or 'profile' in content):
                return self.create_result(
                    exists=True,
                    confidence=0.91,
                    url=f"https://vk.com/{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.84,
                    url=f"https://vk.com/{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.96,
                url=f"https://vk.com/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://vk.com/{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
