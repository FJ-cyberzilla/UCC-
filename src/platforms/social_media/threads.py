"""
Threads (Meta) username checker with Instagram integration
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform
from core.anti_detection import AdvancedAntiDetection

class ThreadsChecker(BasePlatform):
    """Threads username checker leveraging Instagram integration"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection: AdvancedAntiDetection):
        super().__init__(session, anti_detection)
        self.platform_name = "threads"
        self.base_url = "https://threads.net"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Threads username availability"""
        
        # Threads uses Instagram usernames - same account system
        # We can check both Threads and Instagram endpoints
        
        normalized_username = self.normalize_username(username)
        
        endpoints = [
            f"https://threads.net/@{normalized_username}",
            f"https://www.threads.net/@{normalized_username}",
            f"https://www.instagram.com/{normalized_username}"  # Fallback to Instagram
        ]
        
        headers = self.anti_detection.generate_instagram_headers()
        
        for endpoint in endpoints:
            try:
                async with self.session.get(endpoint, headers=headers, allow_redirects=True) as response:
                    result = await self.analyze_threads_response(response, normalized_username, endpoint)
                    if result['confidence'] > 0.7:
                        return result
            except Exception:
                continue
        
        return self.create_result(
            exists=False,
            confidence=0.4,
            method="http_advanced",
            note="Threads uses Instagram accounts. Check may be limited by anti-bot measures."
        )
    
    async def analyze_threads_response(self, response, username: str, endpoint: str) -> Dict[str, Any]:
        """Analyze Threads/Instagram response"""
        
        content = await response.text()
        final_url = str(response.url)
        
        # Threads/Instagram indicators
        threads_indicators = [
            'threads.net/@' + username,
            'instagram.com/' + username,
            'profile_pic_url',
            'username',
        ]
        
        not_found_indicators = [
            'page not found',
            'sorry.*page',
            'content isn.*available',
        ]
        
        if any(indicator in content for indicator in threads_indicators):
            return self.create_result(
                exists=True,
                confidence=0.85,
                url=f"https://threads.net/@{username}",
                method="http_advanced",
                note="Threads account found (uses Instagram username)"
            )
        elif any(indicator in content for indicator in not_found_indicators):
            return self.create_result(
                exists=False,
                confidence=0.80,
                url=f"https://threads.net/@{username}",
                method="http_advanced"
            )
        
        return self.create_result(
            exists=False,
            confidence=0.5,
            url=endpoint,
            method="http_advanced"
        )
