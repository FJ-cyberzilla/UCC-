"""
GitLab username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class GitLabChecker(BasePlatform):
    """GitLab username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "gitlab"
        self.base_url = "https://gitlab.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check GitLab username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
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
        """Analyze GitLab response"""
        
        if response.status == 200:
            content = await response.text()
            
            # GitLab profile indicators
            if 'gitlab.com/' + username in content and 'profile' in content:
                return self.create_result(
                    exists=True,
                    confidence=0.97,
                    url=f"https://gitlab.com/{username}",
                    method="http"
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.90,
                    url=f"https://gitlab.com/{username}",
                    method="http"
                )
        
        elif response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.99,
                url=f"https://gitlab.com/{username}",
                method="http"
            )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.8,
                url=f"https://gitlab.com/{username}",
                method="http",
                error=f"HTTP {response.status}"
            )
