"""
Clubhouse username checker with audio room detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class ClubhouseChecker(BasePlatform):
    """Clubhouse username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "clubhouse"
        self.base_url = "https://www.clubhouse.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Clubhouse username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/@{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Clubhouse response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Clubhouse profile indicators
            if 'clubhouse.com/@' + username in content and 'profile' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.90,
                    url=f"https://clubhouse.com/@{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.82,
                    url=f"https://clubhouse.com/@{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.94,
                url=f"https://clubhouse.com/@{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://clubhouse.com/@{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
