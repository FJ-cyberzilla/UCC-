"""
Eitaa username checker (Iranian platform)
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class EitaaChecker(BasePlatform):
    """Eitaa messenger username checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "eitaa"
        self.base_url = "https://eitaa.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Eitaa username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fa-IR,fa;q=0.9,en;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Eitaa response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Eitaa specific indicators
            if 'eitaa.com/' + username in content and 'channel' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.88,
                    url=f"https://eitaa.com/{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.80,
                    url=f"https://eitaa.com/{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.92,
                url=f"https://eitaa.com/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.6,
                url=f"https://eitaa.com/{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
