"""
Bale messenger username checker (Iranian platform)
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class BaleChecker(BasePlatform):
    """Bale messenger username checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "bale"
        self.base_url = "https://bale.ai"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Bale username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/contact/{normalized_username}"
        
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
        """Analyze Bale response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Check for user profile indicators
            if 'contact-info' in content or 'user-profile' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.90,
                    url=f"https://bale.ai/contact/{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.85,
                    url=f"https://bale.ai/contact/{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.95,
                url=f"https://bale.ai/contact/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.6,
                url=f"https://bale.ai/contact/{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
