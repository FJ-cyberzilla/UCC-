"""
Reddit username checker - simple and reliable
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class RedditChecker(BasePlatform):
    """Reddit username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "reddit"
        self.base_url = "https://www.reddit.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Reddit username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/user/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            async with self.session.get(url, headers=headers, allow_redirects=False) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Reddit response"""
        
        # Reddit returns 200 for existing users, 404 for non-existent
        if response.status == 200:
            # Try to parse JSON response for user data
            try:
                data = await response.json()
                if 'data' in data and 'name' in data['data']:
                    return self.create_result(
                        exists=True,
                        confidence=0.99,
                        url=f"https://www.reddit.com/user/{username}",
                        method="http",
                        additional_info={
                            "account_created": data['data'].get('created_utc'),
                            "karma": data['data'].get('total_karma')
                        }
                    )
            except:
                # Fallback to HTML check
                content = await response.text()
                if f"u/{username}" in content:
                    return self.create_result(
                        exists=True,
                        confidence=0.98,
                        url=f"https://www.reddit.com/user/{username}",
                        method="http"
                    )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.99,
                url=f"https://www.reddit.com/user/{username}",
                method="http"
            )
        
        return self.create_result(
            exists=False,
            confidence=0.8,
            url=f"https://www.reddit.com/user/{username}",
            method="http"
        )
