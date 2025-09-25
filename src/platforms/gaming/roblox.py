"""
Roblox username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class RobloxChecker(BasePlatform):
    """Roblox username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "roblox"
        self.base_url = "https://www.roblox.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Roblox username availability"""
        
        normalized_username = self.normalize_username(username)
        
        # Roblox API endpoint for username validation
        url = f"https://auth.roblox.com/v2/usernames/validate?request.username={normalized_username}&request.birthday=2000-01-01"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Roblox API response"""
        
        if response.status == 200:
            try:
                data = await response.json()
                
                # Roblox returns specific codes for username availability
                if data.get('code') == 0:  # Username is valid and available
                    return self.create_result(
                        exists=False,
                        confidence=0.99,
                        url=f"https://www.roblox.com/user.aspx?username={username}",
                        method="api"
                    )
                elif data.get('code') == 1:  # Username is taken
                    return self.create_result(
                        exists=True,
                        confidence=0.99,
                        url=f"https://www.roblox.com/user.aspx?username={username}",
                        method="api"
                    )
                else:
                    return self.create_result(
                        exists=False,
                        confidence=0.7,
                        url=f"https://www.roblox.com/user.aspx?username={username}",
                        method="api",
                        error=f"API returned code: {data.get('code')}"
                    )
                    
            except Exception as e:
                return self.create_error_result(f"JSON parse error: {e}")
        
        return self.create_result(
            exists=False,
            confidence=0.5,
            url=f"https://www.roblox.com/user.aspx?username={username}",
            method="api",
            error=f"HTTP {response.status}"
        )
