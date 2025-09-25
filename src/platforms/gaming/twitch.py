"""
Twitch username checker
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class TwitchChecker(BasePlatform):
    """Twitch username availability checker"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "twitch"
        self.base_url = "https://www.twitch.tv"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Twitch username availability"""
        
        normalized_username = self.normalize_username(username)
        url = f"{self.base_url}/{normalized_username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',  # Twitch web client ID
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                return await self.analyze_response(response, normalized_username)
                
        except Exception as e:
            return self.create_error_result(str(e))
    
    async def analyze_response(self, response, username: str) -> Dict[str, Any]:
        """Analyze Twitch response"""
        
        content = await response.text()
        
        # Twitch profile indicators
        profile_indicators = [
            '"login":"' + username + '"',
            'twitch.tv/' + username,
            'profile-card',
            'channel-header',
        ]
        
        # Not found indicators
        not_found_indicators = [
            'This channel is unavailable',
            'Page not found',
            'error-page',
        ]
        
        if any(indicator in content for indicator in profile_indicators):
            return self.create_result(
                exists=True,
                confidence=0.95,
                url=f"https://www.twitch.tv/{username}",
                method="http"
            )
        elif any(indicator in content for indicator in not_found_indicators) or response.status == 404:
            return self.create_result(
                exists=False,
                confidence=0.98,
                url=f"https://www.twitch.tv/{username}",
                method="http"
            )
        else:
            return self.create_result(
                exists=False,
                confidence=0.7,
                url=f"https://www.twitch.tv/{username}",
                method="http",
                note="Inconclusive result"
            )
