"""
Mastodon username checker with instance detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class MastodonChecker(BasePlatform):
    """Mastodon username checker with federated instance support"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "mastodon"
        self.base_url = "https://mastodon.social"  # Default instance
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Mastodon username across popular instances"""
        
        normalized_username = self.normalize_username(username)
        
        # Popular Mastodon instances to check
        instances = [
            "mastodon.social",
            "mstdn.social", 
            "fosstodon.org",
            "hachyderm.io",
            "tech.lgbt",
            "infosec.exchange"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/activity+json, application/json',
        }
        
        for instance in instances:
            url = f"https://{instance}/@{normalized_username}"
            
            try:
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return self.create_result(
                            exists=True,
                            confidence=0.92,
                            url=url,
                            method="http",
                            additional_info={"instance": instance},
                            note="Mastodon is federated. User found on specific instance."
                        )
            except Exception:
                continue
        
        # Also check the Webfinger protocol
        webfinger_url = f"https://mastodon.social/.well-known/webfinger?resource=acct:{normalized_username}@mastodon.social"
        
        try:
            async with self.session.get(webfinger_url, headers=headers) as response:
                if response.status == 200:
                    return self.create_result(
                        exists=True,
                        confidence=0.95,
                        url=f"https://mastodon.social/@{normalized_username}",
                        method="webfinger",
                        note="User found via Webfinger protocol"
                    )
        except Exception:
            pass
        
        return self.create_result(
            exists=False,
            confidence=0.85,
            method="http",
            note="Mastodon is federated. User not found on checked instances.",
            error="User not found on popular Mastodon instances"
        )
