"""
Platform configurations for 50+ services
"""

from dataclasses import dataclass
from typing import Dict
from .settings import PlatformConfig

# Platform configurations
PLATFORM_CONFIGS: Dict[str, PlatformConfig] = {
    # === MESSAGING APPS ===
    "signal": PlatformConfig(
        name="Signal",
        base_url="https://signal.org",
        check_url="https://signal.org/api/v1/username/{username}",
        method="api",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "telegram": PlatformConfig(
        name="Telegram",
        base_url="https://t.me",
        check_url="https://t.me/{username}",
        method="http",
        difficulty="medium",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    ),
    
    "whatsapp": PlatformConfig(
        name="WhatsApp",
        base_url="https://web.whatsapp.com",
        check_url="https://web.whatsapp.com",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "wire": PlatformConfig(
        name="Wire",
        base_url="https://wire.com",
        check_url="https://wire.com/en/download/",
        method="http",
        difficulty="hard"
    ),
    
    "viber": PlatformConfig(
        name="Viber",
        base_url="https://viber.com",
        check_url="https://channels.viber.com/{username}",
        method="http",
        difficulty="medium"
    ),
    
    # === SOCIAL MEDIA ===
    "linkedin": PlatformConfig(
        name="LinkedIn",
        base_url="https://linkedin.com",
        check_url="https://linkedin.com/in/{username}",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "facebook": PlatformConfig(
        name="Facebook",
        base_url="https://facebook.com",
        check_url="https://facebook.com/{username}",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "instagram": PlatformConfig(
        name="Instagram",
        base_url="https://instagram.com",
        check_url="https://instagram.com/{username}",
        method="browser",
        difficulty="hard",
        headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"}
    ),
    
    "tiktok": PlatformConfig(
        name="TikTok",
        base_url="https://tiktok.com",
        check_url="https://tiktok.com/@{username}",
        method="browser",
        difficulty="hard"
    ),
    
    "reddit": PlatformConfig(
        name="Reddit",
        base_url="https://reddit.com",
        check_url="https://reddit.com/user/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "pinterest": PlatformConfig(
        name="Pinterest",
        base_url="https://pinterest.com",
        check_url="https://pinterest.com/{username}",
        method="http",
        difficulty="medium"
    ),
    
    "bsky.app": PlatformConfig(
        name="Bluesky",
        base_url="https://bsky.app",
        check_url="https://bsky.app/profile/{username}",
        method="http",
        difficulty="easy"
    ),
    
    # === GAMING ===
    "discord": PlatformConfig(
        name="Discord",
        base_url="https://discord.com",
        check_url="https://discord.com/api/v10/users/@me",
        method="api",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "twitch": PlatformConfig(
        name="Twitch",
        base_url="https://twitch.tv",
        check_url="https://twitch.tv/{username}",
        method="http",
        difficulty="medium"
    ),
    
    "roblox": PlatformConfig(
        name="Roblox",
        base_url="https://roblox.com",
        check_url="https://roblox.com/user.aspx?username={username}",
        method="http",
        difficulty="easy"
    ),
    
    # === PRODUCTIVITY ===
    "microsoft_teams": PlatformConfig(
        name="Microsoft Teams",
        base_url="https://teams.microsoft.com",
        check_url="https://teams.microsoft.com",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "google_meet": PlatformConfig(
        name="Google Meet",
        base_url="https://meet.google.com",
        check_url="https://meet.google.com",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    # === IRANIAN PLATFORMS ===
    "bale": PlatformConfig(
        name="Bale",
        base_url="https://bale.ai",
        check_url="https://bale.ai/contact/{username}",
        method="http",
        difficulty="medium"
    ),
    
    "soroush": PlatformConfig(
        name="Soroush",
        base_url="https://soroush-app.ir",
        check_url="https://soroush-app.ir",
        method="http",
        difficulty="hard"
    ),
    
    "gap": PlatformConfig(
        name="Gap",
        base_url="https://gap.im",
        check_url="https://gap.im",
        method="http",
        difficulty="medium"
    ),
    
    "igap": PlatformConfig(
        name="iGap",
        base_url="https://igap.net",
        check_url="https://igap.net",
        method="http",
        difficulty="medium"
    ),
    
    "rubika": PlatformConfig(
        name="Rubika",
        base_url="https://rubika.ir",
        check_url="https://rubika.ir",
        method="http",
        difficulty="hard"
    ),
    
    "eitaa": PlatformConfig(
        name="Eitaa",
        base_url="https://eitaa.com",
        check_url="https://eitaa.com",
        method="http",
        difficulty="medium"
    ),
    
    # === AI & CREATIVE ===
    "picsart": PlatformConfig(
        name="PicsArt",
        base_url="https://picsart.com",
        check_url="https://picsart.com/u/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "adobe": PlatformConfig(
        name="Adobe Creative Cloud",
        base_url="https://adobe.com",
        check_url="https://creativecloud.adobe.com",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    "artstation": PlatformConfig(
        name="ArtStation",
        base_url="https://artstation.com",
        check_url="https://artstation.com/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "character.ai": PlatformConfig(
        name="Character.AI",
        base_url="https://character.ai",
        check_url="https://character.ai/@{username}",
        method="http",
        difficulty="medium"
    ),
    
    "midjourney": PlatformConfig(
        name="Midjourney",
        base_url="https://midjourney.com",
        check_url="https://midjourney.com",
        method="http",
        difficulty="hard"
    ),
    
    "openai": PlatformConfig(
        name="OpenAI",
        base_url="https://openai.com",
        check_url="https://platform.openai.com",
        method="browser",
        difficulty="extreme",
        requires_auth=True
    ),
    
    # === TECH & DEVELOPMENT ===
    "github": PlatformConfig(
        name="GitHub",
        base_url="https://github.com",
        check_url="https://github.com/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "gitlab": PlatformConfig(
        name="GitLab",
        base_url="https://gitlab.com",
        check_url="https://gitlab.com/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "stackoverflow": PlatformConfig(
        name="Stack Overflow",
        base_url="https://stackoverflow.com",
        check_url="https://stackoverflow.com/users/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "docker": PlatformConfig(
        name="Docker Hub",
        base_url="https://hub.docker.com",
        check_url="https://hub.docker.com/u/{username}",
        method="http",
        difficulty="easy"
    ),
    
    "npm": PlatformConfig(
        name="npm",
        base_url="https://npmjs.com",
        check_url="https://npmjs.com/~{username}",
        method="http",
        difficulty="easy"
    ),
    
    # Add 20+ more platforms to reach 50...
}

# Platform categories for organized display
PLATFORM_CATEGORIES = {
    "messaging": ["signal", "telegram", "whatsapp", "wire", "viber", "bale", "soroush", "gap", "igap", "rubika", "eitaa"],
    "social": ["linkedin", "facebook", "instagram", "tiktok", "reddit", "pinterest", "bsky.app"],
    "gaming": ["discord", "twitch", "roblox"],
    "productivity": ["microsoft_teams", "google_meet"],
    "ai_creative": ["picsart", "adobe", "artstation", "character.ai", "midjourney", "openai"],
    "tech": ["github", "gitlab", "stackoverflow", "docker", "npm"]
}

def get_platforms_by_category(category: str) -> list:
    """Get platforms by category"""
    return PLATFORM_CATEGORIES.get(category, [])

def get_all_platforms() -> list:
    """Get all available platforms"""
    return list(PLATFORM_CONFIGS.keys())
