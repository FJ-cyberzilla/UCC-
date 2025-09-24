"""
Advanced IP/Geolocation Rotation with Intelligent Routing
Multi-protocol support, geographic diversity, and AI-based selection
"""

import asyncio
import aiohttp
import random
import time
import json
import ipaddress
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import logging
from collections import defaultdict
import math

@dataclass
class AdvancedProxy:
    """Advanced proxy with comprehensive metadata"""
    url: str
    protocol: str  # http, https, socks4, socks5
    anonymity: str  # transparent, anonymous, elite
    geographic: Dict[str, str]  # country, city, isp
    performance: Dict[str, float]  # speed, uptime, reliability
    last_used: float
    usage_count: int
    failure_count: int
    whitelisted: bool
    premium: bool

@dataclass
class GeographicProfile:
    """Geographic routing profile"""
    target_country: Optional[str]
    avoid_countries: Set[str]
    preferred_cities: List[str]
    diversity_required: bool
    max_same_country: int

class AdvancedProxyRotator:
    """Advanced IP rotation with geographic intelligence"""
    
    def __init__(self):
        self.proxies: Dict[str, AdvancedProxy] = {}
        self.proxy_sources: List[str] = []
        self.geo_cache: Dict[str, Dict] = {}
        self.performance_metrics = defaultdict(list)
        self.logger = logging.getLogger(__name__)
        
        # AI-based selection parameters
        self.selection_weights = {
            'performance': 0.25,
            'geographic_diversity': 0.20,
            'anonymity': 0.15,
            'freshness': 0.10,
            'reliability': 0.30
        }
        
        self._initialize_proxy_sources()
    
    def _initialize_proxy_sources(self):
        """Initialize multiple proxy sources"""
        
        self.proxy_sources = [
            # Free proxy sources
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            
            # Premium sources (would require API keys in production)
            # "https://premium-proxy-provider.com/api/proxies",
        ]
    
    async def initialize(self, preload_count: int = 200):
        """Initialize with a large pool of proxies"""
        
        self.logger.info("Loading advanced proxy pool...")
        
        # Load from multiple sources concurrently
        tasks = []
        for source in self.proxy_sources:
            task = asyncio.create_task(self._load_proxies_from_source(source))
            tasks.append(task)
        
        # Wait for all sources to load
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Test and validate proxies
        await self._validate_proxy_pool(preload_count)
        
        self.logger.info(f"Advanced proxy rotator initialized with {len(self.proxies)} proxies")
    
    async def _load_proxies_from_source(self, source_url: str) -> int:
        """Load proxies from a specific source"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        proxies = self._parse_proxy_list(content, source_url)
                        
                        added_count = 0
                        for proxy_url in proxies:
                            if self._add_proxy(proxy_url, source_url):
                                added_count += 1
                        
                        self.logger.debug(f"Loaded {added_count} proxies from {source_url}")
                        return added_count
        
        except Exception as e:
            self.logger.warning(f"Failed to load proxies from {source_url}: {e}")
            return 0
    
    def _parse_proxy_list(self, content: str, source_url: str) -> List[str]:
        """Parse various proxy list formats"""
        
        proxies = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Handle different proxy format
            if ':' in line:
                if line.count(':') == 1:
                    # IP:PORT format
                    proxies.append(f"http://{line}")
                elif line.count(':') == 2:
                    # IP:PORT:USER:PASS format
                    parts = line.split(':')
                    if len(parts) == 4:
                        ip, port, user, password = parts
                        proxies.append(f"http://{user}:{password}@{ip}:{port}")
        
        return proxies
    
    def _add_proxy(self, proxy_url: str, source: str) -> bool:
        """Add a proxy to the pool with initial metadata"""
        
        try:
            # Extract basic information from URL
            if proxy_url not in self.proxies:
                proxy = AdvancedProxy(
                    url=proxy_url,
                    protocol=self._detect_protocol(proxy_url),
                    anonymity="unknown",
                    geographic={"country": "unknown", "city": "unknown", "isp": "unknown"},
                    performance={"speed": 1.0, "uptime": 0.5, "reliability": 0.5},
                    last_used=0.0,
                    usage_count=0,
                    failure_count=0,
                    whitelisted=False,
                    premium=False
                )
                
                self.proxies[proxy_url] = proxy
                return True
        
        except Exception as e:
            self.logger.debug(f"Failed to add proxy {proxy_url}: {e}")
        
        return False
    
    def _detect_protocol(self, proxy_url: str) -> str:
        """Detect proxy protocol from URL"""
        
        if proxy_url.startswith('socks5://'):
            return 'socks5'
        elif proxy_url.startswith('socks4://'):
            return 'socks4'
        elif proxy_url.startswith('https://'):
            return 'https'
        else:
            return 'http'
    
    async def _validate_proxy_pool(self, max_test: int):
        """Validate and geolocate proxy pool"""
        
        test_urls = [
            "http://httpbin.org/ip",
            "http://api.ipify.org?format=json",
            "http://ipinfo.io/json"
        ]
        
        proxies_to_test = list(self.proxies.keys())[:max_test]
        semaphore = asyncio.Semaphore(10)  # Limit concurrent tests
        
        async def test_proxy(proxy_url: str):
            async with semaphore:
                await self._test_and_geolocate_proxy(proxy_url, test_urls)
        
        # Test proxies concurrently
        tasks = [test_proxy(proxy) for proxy in proxies_to_test]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Remove failed proxies
        initial_count = len(self.proxies)
        self.proxies = {k: v for k, v in self.proxies.items() if v.performance['reliability'] > 0.1}
        
        self.logger.info(f"Proxy validation complete. {len(self.proxies)}/{initial_count} proxies valid")
    
    async def _test_and_geolocate_proxy(self, proxy_url: str, test_urls: List[str]):
        """Test proxy and geolocate it"""
        
        proxy = self.proxies[proxy_url]
        
        try:
            connector = aiohttp.TCPConnector()
            timeout = aiohttp.ClientTimeout(total=15)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                start_time = time.time()
                
                for test_url in test_urls:
                    try:
                        async with session.get(test_url, proxy=proxy_url) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                # Extract IP and geolocation information
                                if 'ip' in data:
                                    await self._geolocate_proxy(proxy, data['ip'])
                                
                                # Update performance metrics
                                response_time = time.time() - start_time
                                self._update_proxy_performance(proxy, True, response_time)
                                return
                    
                    except Exception as e:
                        continue
                
                # All test URLs failed
                self._update_proxy_performance(proxy, False, 0.0)
        
        except Exception as e:
            self._update_proxy_performance(proxy, False, 0.0)
    
    async def _geolocate_proxy(self, proxy: AdvancedProxy, ip_address: str):
        """Geolocate proxy IP address"""
        
        try:
            if ip_address in self.geo_cache:
                geo_data = self.geo_cache[ip_address]
            else:
                # Use ipinfo.io for geolocation (free tier)
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://ipinfo.io/{ip_address}/json") as response:
                        if response.status == 200:
                            geo_data = await response.json()
                            self.geo_cache[ip_address] = geo_data
            
            # Update proxy geographic information
            proxy.geographic = {
                'country': geo_data.get('country', 'unknown'),
                'city': geo_data.get('city', 'unknown'),
                'isp': geo_data.get('org', 'unknown'),
                'ip': ip_address
            }
            
        except Exception as e:
            self.logger.debug(f"Geolocation failed for {ip_address}: {e}")
    
    def _update_proxy_performance(self, proxy: AdvancedProxy, success: bool, response_time: float):
        """Update proxy performance metrics"""
        
        # Update reliability (moving average)
        alpha = 0.1
        current_reliability = proxy.performance['reliability']
        if success:
            new_reliability = (1 - alpha) * current_reliability + alpha * 1.0
            proxy.performance['speed'] = (1 - alpha) * proxy.performance['speed'] + alpha * (1.0 / max(response_time, 0.1))
        else:
            new_reliability = (1 - alpha) * current_reliability + alpha * 0.0
            proxy.failure_count += 1
        
        proxy.performance['reliability'] = new_reliability
        proxy.performance['uptime'] = 1.0 - (proxy.failure_count / max(proxy.usage_count, 1))
    
    async def get_optimal_proxy(self, 
                              geographic_profile: Optional[GeographicProfile] = None,
                              target_anonymity: str = "elite",
                              protocol_preference: List[str] = None) -> Optional[str]:
        """Get optimal proxy using AI-based selection"""
        
        if not self.proxies:
            return None
        
        # Filter proxies based on requirements
        candidate_proxies = self._filter_candidates(
            geographic_profile, 
            target_anonymity, 
            protocol_preference or ["socks5", "https", "http"]
        )
        
        if not candidate_proxies:
            self.logger.warning("No proxies match the specified criteria")
            return None
        
        # Score candidates using AI-based algorithm
        scored_proxies = []
        for proxy in candidate_proxies:
            score = self._calculate_proxy_score(proxy, geographic_profile)
            scored_proxies.append((proxy, score))
        
        # Select best proxy
        scored_proxies.sort(key=lambda x: x[1], reverse=True)
        best_proxy = scored_proxies[0][0]
        
        # Update usage statistics
        best_proxy.last_used = time.time()
        best_proxy.usage_count += 1
        
        return best_proxy.url
    
    def _filter_candidates(self, 
                          geographic_profile: Optional[GeographicProfile],
                          anonymity: str,
                          protocols: List[str]) -> List[AdvancedProxy]:
        """Filter proxy candidates based on requirements"""
        
        candidates = []
        
        for proxy in self.proxies.values():
            # Check protocol
            if proxy.protocol not in protocols:
                continue
            
            # Check anonymity
            if anonymity != "any" and proxy.anonymity != anonymity:
                continue
            
            # Check geographic restrictions
            if geographic_profile:
                country = proxy.geographic['country']
                
                # Check avoided countries
                if country in geographic_profile.avoid_countries:
                    continue
                
                # Check target country
                if (geographic_profile.target_country and 
                    geographic_profile.target_country != country):
                    continue
            
            # Minimum reliability threshold
            if proxy.performance['reliability'] < 0.3:
                continue
            
            candidates.append(proxy)
        
        return candidates
    
    def _calculate_proxy_score(self, proxy: AdvancedProxy, 
                             geographic_profile: Optional[GeographicProfile]) -> float:
        """Calculate AI-based proxy selection score"""
        
        score = 0.0
        
        # Performance score (speed + reliability)
        perf_score = (proxy.performance['speed'] * 0.6 + 
                     proxy.performance['reliability'] * 0.4)
        score += perf_score * self.selection_weights['performance']
        
        # Geographic diversity score
        geo_score = self._calculate_geographic_score(proxy, geographic_profile)
        score += geo_score * self.selection_weights['geographic_diversity']
        
        # Anonymity score
        anonymity_scores = {"transparent": 0.3, "anonymous": 0.7, "elite": 1.0}
        anonymity_score = anonymity_scores.get(proxy.anonymity, 0.5)
        score += anonymity_score * self.selection_weights['anonymity']
        
        # Freshness score (prefer less recently used proxies)
        time_since_use = time.time() - proxy.last_used
        freshness_score = min(time_since_use / 3600.0, 1.0)  # Normalize to 1 hour
        score += freshness_score * self.selection_weights['freshness']
        
        # Reliability score (uptime and failure rate)
        reliability_score = proxy.performance['uptime']
        score += reliability_score * self.selection_weights['reliability']
        
        return score
    
    def _calculate_geographic_score(self, proxy: AdvancedProxy, 
                                  geographic_profile: Optional[GeographicProfile]) -> float:
        """Calculate geographic diversity score"""
        
        if not geographic_profile:
            return 0.7  # Neutral score when no profile specified
        
        score = 0.5  # Base score
        
        # Bonus for preferred cities
        if proxy.geographic['city'] in geographic_profile.preferred_cities:
            score += 0.3
        
        # Bonus for country diversity
        if geographic_profile.diversity_required:
            # Calculate how many times this country has been used recently
            country_usage = self._get_recent_country_usage(proxy.geographic['country'])
            max_allowed = geographic_profile.max_same_country
            
            if country_usage < max_allowed:
                diversity_bonus = (max_allowed - country_usage) / max_allowed * 0.4
                score += diversity_bonus
        
        return min(score, 1.0)
    
    def _get_recent_country_usage(self, country: str) -> int:
        """Get recent usage count for a country"""
        
        recent_threshold = time.time() - 3600  # 1 hour window
        count = 0
        
        for proxy in self.proxies.values():
            if (proxy.usage_count > 0 and 
                proxy.last_used > recent_threshold and 
                proxy.geographic['country'] == country):
                count += 1
        
        return count
    
    async def rotate_geographic_sequence(self, 
                                       count: int,
                                       geographic_profile: GeographicProfile) -> List[str]:
        """Get a sequence of proxies with geographic rotation"""
        
        proxies = []
        used_countries = set()
        
        for i in range(count):
            # Update profile to enforce diversity
            current_profile = GeographicProfile(
                target_country=geographic_profile.target_country,
                avoid_countries=geographic_profile.avoid_countries.union(used_countries),
                preferred_cities=geographic_profile.preferred_cities,
                diversity_required=True,
                max_same_country=1  # Maximum one proxy per country in sequence
            )
            
            proxy_url = await self.get_optimal_proxy(current_profile)
            if proxy_url:
                proxies.append(proxy_url)
                proxy = self.proxies[proxy_url]
                used_countries.add(proxy.geographic['country'])
            else:
                break
        
        return proxies
    
    async def get_proxy_statistics(self) -> Dict[str, Any]:
        """Get comprehensive proxy pool statistics"""
        
        total_proxies = len(self.proxies)
        if total_proxies == 0:
            return {"error": "No proxies available"}
        
        # Geographic distribution
        countries = defaultdict(int)
        protocols = defaultdict(int)
        anonymity_levels = defaultdict(int)
        
        for proxy in self.proxies.values():
            countries[proxy.geographic['country']] += 1
            protocols[proxy.protocol] += 1
            anonymity_levels[proxy.anonymity] += 1
        
        # Performance statistics
        reliabilities = [p.performance['reliability'] for p in self.proxies.values()]
        speeds = [p.performance['speed'] for p in self.proxies.values()]
        
        return {
            "total_proxies": total_proxies,
            "geographic_distribution": dict(countries),
            "protocol_distribution": dict(protocols),
            "anonymity_distribution": dict(anonymity_levels),
            "average_reliability": sum(reliabilities) / len(reliabilities),
            "average_speed": sum(speeds) / len(speeds),
            "premium_proxies": sum(1 for p in self.proxies.values() if p.premium),
            "whitelisted_proxies": sum(1 for p in self.proxies.values() if p.whitelisted)
        }
