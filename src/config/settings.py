"""
Configuration settings for the Ultimate Username Checker
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class RateLimitConfig:
    requests_per_second: float = 0.5
    burst_capacity: int = 5
    timeout: int = 10
    retry_attempts: int = 3

@dataclass
class AntiDetectionConfig:
    enable_fingerprinting: bool = True
    enable_captcha_solving: bool = False
    enable_cloudflare_bypass: bool = True
    human_behavior_simulation: bool = True
    fingerprint_pool_size: int = 10

@dataclass
class ProxyConfig:
    enable_rotation: bool = False
    proxy_list: List[str] = field(default_factory=list)
    max_failures: int = 3
    test_proxies: bool = True

@dataclass
class OutputConfig:
    save_to_file: bool = True
    output_format: str = "json"  # json, csv, txt
    output_dir: Path = Path("results")
    verbose: bool = False
    show_confidence: bool = True

@dataclass
class UltimateConfig:
    # Core settings
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    anti_detection: AntiDetectionConfig = field(default_factory=AntiDetectionConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    
    # Feature flags
    enable_advanced: bool = False
    enable_proxy_rotation: bool = False
    enable_api_fallback: bool = True
    
    # API keys
    api_keys: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        # Load from environment variables
        self._load_from_env()
        
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Rate limiting
        if os.getenv('REQUESTS_PER_SECOND'):
            self.rate_limit.requests_per_second = float(os.getenv('REQUESTS_PER_SECOND'))
        
        # API keys
        for key in ['INSTAGRAM', 'TWITTER', 'GITHUB', 'REDDIT']:
            env_key = f"{key}_API_KEY"
            if os.getenv(env_key):
                self.api_keys[key.lower()] = os.getenv(env_key)
        
        # Proxy settings
        if os.getenv('PROXY_LIST'):
            self.proxy.proxy_list = os.getenv('PROXY_LIST').split(',')
            self.proxy.enable_rotation = True

@dataclass
class PlatformConfig:
    name: str
    base_url: str
    check_url: str
    method: str  # http, api, browser
    difficulty: str  # easy, medium, hard, extreme
    requires_auth: bool = False
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 10
