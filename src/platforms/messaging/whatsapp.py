"""
WhatsApp username checker (limited due to privacy)
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class WhatsAppChecker(BasePlatform):
    """WhatsApp availability checker - limited functionality"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "whatsapp"
        self.base_url = "https://web.whatsapp.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check WhatsApp - very limited due to encryption"""
        
        return self.create_result(
            exists=False,
            confidence=0.0,
            method="api",
            note="WhatsApp usernames are not publicly searchable. Requires phone number verification.",
            error="Platform limitation: WhatsApp uses phone numbers, not public usernames"
        )
