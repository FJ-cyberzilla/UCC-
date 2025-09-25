"""
Telegram username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class TelegramChecker(BasePlatform):
    """Telegram username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "telegram"
        self.base_url = "https://t.me"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Telegram username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers, allow_redirects=False) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Telegram response"""
        
        # Telegram returns 200 for valid users, 404 for unavailable
        if response.status == 200:
            content = await response.text()
            
            # Check for "This channel doesn't exist" or similar
            if "doesn't exist" in content.lower() or "not found" in content.lower():
                return self.create_result(
                    exists=False,
                    confidence=0.95,
                    url=f"https://t.me/{username}",
                    method="http"
                )
            
            return self.create_result(
                exists=True,
                confidence=0.90,
                url=f"https://t.me/{username}",
                method="http"
            )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.99,
                url=f"https://t.me/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.5,
                url=f"https://t.me/{username}",
                method="http",
                error=f"Unexpected status code: {response.status}"
            )
