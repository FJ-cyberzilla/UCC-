"""
Element (Matrix) username checker with homeserver detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class ElementChecker(BasePlatform):
    """Element/Matrix username checker with homeserver support"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "element"
        self.base_url = "https://app.element.io"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Element/Matrix username availability"""
        
        normalized_username = self.normalize_username(username)
        
        # Matrix is federated - check multiple homeservers
        homeservers = [
            "matrix.org",
            "element.io", 
            "gitter.im",
            "libera.chat"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        for homeserver in homeservers:
            # Check via Matrix federation API
            url = f"https://{homeserver}/_matrix/client/r0/profile/@{normalized_username}:{homeserver}"
            
            try:
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'displayname' in data:
                            return self.create_result(
                                exists=True,
                                confidence=0.94,
                                url=f"https://app.element.io/#/@{normalized_username}:{homeserver}",
                                method="matrix_api",
                                additional_info={"homeserver": homeserver},
                                note="Matrix user found on specific homeserver"
                            )
            except Exception:
                continue
        
        return self.create_result(
            exists=False,
            confidence=0.88,
            method="matrix_api",
            note="Matrix is federated. User not found on checked homeservers.",
            error="User not found on popular Matrix homeservers"
        )
