"""
Slack username checker with workspace detection
"""

import aiohttp
from typing import Dict, Any
from platforms.base import BasePlatform

class SlackChecker(BasePlatform):
    """Slack username checker with workspace-based approach"""
    
    def __init__(self, session: aiohttp.ClientSession, anti_detection=None):
        super().__init__(session, anti_detection)
        self.platform_name = "slack"
        self.base_url = "https://slack.com"
    
    async def check_username(self, username: str) -> Dict[str, Any]:
        """Check Slack username availability"""
        
        # Slack usernames are workspace-specific
        # We can check common public workspaces or community pages
        
        normalized_username = self.normalize_username(username)
        
        # Try different Slack community URLs
        community_urls = [
            f"https://{normalized_username}.slack.com",
            f"https://app.slack.com/client/{normalized_username}",
            f"https://slack.com/@{normalized_username}"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        for url in community_urls:
            try:
                async with self.session.get(url, headers=headers, allow_redirects=False) as response:
                    if response.status in [200, 301, 302]:
                        return self.create_result(
                            exists=True,
                            confidence=0.75,
                            url=url,
                            method="http",
                            note="Slack workspace or community found. Usernames are workspace-specific."
                        )
            except Exception:
                continue
        
        return self.create_result(
            exists=False,
            confidence=0.6,
            method="http",
            note="Slack usernames are workspace-specific. No public global username system.",
            error="Platform limitation: Workspace-specific usernames"
        )
