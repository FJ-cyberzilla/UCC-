"""
GitHub username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class GitHubChecker(BasePlatform):
    """GitHub username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "github"
        self.base_url = "https://github.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check GitHub username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.github.v3+json',
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze GitHub response"""
        
        if response.status == 200:
            # GitHub returns user data for existing users
            try:
                # Try to parse as JSON first (API response)
                data = await response.json()
                if 'login' in data and data['login'].lower() == username.lower():
                    return self.create_result(
                        exists=True,
                        confidence=0.99,
                        url=f"https://github.com/{username}",
                        method="api",
                        additional_info={
                            "name": data.get('name'),
                            "public_repos": data.get('public_repos'),
                            "followers": data.get('followers')
                        }
                    )
            except:
                # Fallback to HTML check
                content = await response.text()
                if f'github.com/{username}' in content and 'profile' in content:
                    return self.create_result(
                        exists=True,
                        confidence=0.98,
                        url=f"https://github.com/{username}",
                        method="http"
                    )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.99,
                url=f"https://github.com/{username}",
                method="http"
            )
        
        return self.create_result(
            exists=False,
            confidence=0.9,
            url=f"https://github.com/{username}",
            method="http"
        )
