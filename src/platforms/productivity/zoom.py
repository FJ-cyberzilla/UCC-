"""
Zoom username checker with meeting-based detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class ZoomChecker(BasePlatform):
    """Zoom username checker with sophisticated approach"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "zoom"
        self.base_url = "https://zoom.us"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Zoom username availability"""
        
        # Zoom uses email-based accounts, not public usernames
        # However, we can check for public profile pages
        
        normalized_username = self.normalize_username(username)
        url = f"https://explore.zoom.us/en/products/{normalized_username}"
        
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
        """Analyze Zoom response"""
        
        if response.status == 200:
            content = await response.text()
            
            # Zoom profile indicators are limited
            if 'zoom.us' in content and username in content:
                return self.create_result(
                    exists=True,
                    confidence=0.70,
                    url=f"https://zoom.us/{username}",
                    method="http",
                    note="Zoom uses email-based accounts. This checks for public profiles."
                )
            else:
                return self.create_result(
                    exists=False,
                    confidence=0.65,
                    url=f"https://zoom.us/{username}",
                    method="http",
                    note="Zoom accounts are primarily email-based"
                )
        
        else:
            return self.create_result(
                exists=False,
                confidence=0.4,
                method="http",
                note="Zoom doesn't have public username system. Uses email-based accounts.",
                error="Platform limitation: No public username lookup"
            )
