"""
Advanced proxy rotation with ML-based selection
"""

import asyncio
import aiohttp
import random
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging

@dataclass
class ProxyPerformance:
    """Proxy performance metrics"""
    proxy: str
    success_rate: float
    avg_response_time: float
    last_used: float
    failure_count: int
    geographic_location: str
    anonymity_level: str

class AdvancedProxyRotator:
    """ML-enhanced proxy rotation system"""
    
    def __init__(self):
        self.proxies = []
        self.performance_metrics = {}
        self.blacklisted_proxies = set()
        self.geo_distribution = {}
        self.logger = logging.getLogger(__name__)
        
        # ML-based selection weights
        self.selection_weights = {
            'success_rate': 0.4,
            'response_time': 0.3,
            'geographic_diversity': 0.2,
            'anonymity': 0.1
        }
    
    async def initialize(self):
        """Initialize proxy system"""
        await self._load_proxy_sources()
        await self._test_all_proxies()
    
    async def _load_proxy_sources(self):
        """Load proxies from multiple sources"""
        
        # Free proxy sources (would be expanded in production)
        free_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        
        for source in free_sources:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(source) as response:
                        if response.status == 200:
                            text = await response.text()
                            proxies = [p.strip() for p in text.split('\n') if p.strip()]
                            self.proxies.extend(proxies)
            except Exception as e:
                self.logger.warning(f"Failed to load proxies from {source}: {e}")
        
        # Remove duplicates
        self.proxies = list(set(self.proxies))
        self.logger.info(f"Loaded {len(self.proxies)} proxies")
    
    async def _test_all_proxies(self):
        """Test all proxies for functionality"""
        
        test_url = "http://httpbin.org/ip"
        timeout = aiohttp.ClientTimeout(total=10)
        
        async def test_proxy(proxy):
            try:
                connector = aiohttp.TCPConnector()
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    start_time = time.time()
                    async with session.get(test_url, proxy=f"http://{proxy}") as response:
                        if response.status == 200:
                            response_time = time.time() - start_time
                            self.performance_metrics[proxy] = ProxyPerformance(
                                proxy=proxy,
                                success_rate=1.0,
                                avg_response_time=response_time,
                                last_used=time.time(),
                                failure_count=0,
                                geographic_location="Unknown",  # Would geolocate in production
                                anonymity_level="Unknown"
                            )
                            return True
            except Exception:
                self.blacklisted_proxies.add(proxy)
                return False
        
        # Test proxies concurrently
        tasks = [test_proxy(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        working_proxies = sum(1 for r in results if r is True)
        self.logger.info(f"Found {working_proxies} working proxies out of {len(self.proxies)}")
    
    async def get_optimal_proxy(self, target_url: str) -> Optional[str]:
        """Get optimal proxy using ML-based selection"""
        
        if not self.performance_metrics:
            return None
        
        # Filter working proxies
        working_proxies = [
            p for p in self.performance_metrics.values() 
            if p.proxy not in self.blacklisted_proxies
        ]
        
        if not working_proxies:
            return None
        
        # Calculate scores for each proxy
        scored_proxies = []
        for proxy in working_proxies:
            score = self._calculate_proxy_score(proxy, target_url)
            scored_proxies.append((proxy, score))
        
        # Select proxy with highest score
        scored_proxies.sort(key=lambda x: x[1], reverse=True)
        best_proxy = scored_proxies[0][0]
        
        # Update usage statistics
        best_proxy.last_used = time.time()
        
        return f"http://{best_proxy.proxy}"
    
    def _calculate_proxy_score(self, proxy: ProxyPerformance, target_url: str) -> float:
        """Calculate proxy selection score using multiple factors"""
        
        score = 0.0
        
        # Success rate factor
        score += proxy.success_rate * self.selection_weights['success_rate']
        
        # Response time factor (inverse)
        time_factor = max(0, 1 - (proxy.avg_response_time / 10.0))
        score += time_factor * self.selection_weights['response_time']
        
        # Geographic diversity factor
        geo_score = self._calculate_geo_diversity(proxy, target_url)
        score += geo_score * self.selection_weights['geographic_diversity']
        
        # Anonymity factor
        anonymity_score = self._calculate_anonymity_score(proxy.anonymity_level)
        score += anonymity_score * self.selection_weights['anonymity']
        
        return score
    
    def _calculate_geo_diversity(self, proxy: ProxyPerformance, target_url: str) -> float:
        """Calculate geographic diversity score"""
        # Would implement actual geolocation logic
        return random.uniform(0.7, 1.0)
    
    def _calculate_anonymity_score(self, anonymity: str) -> float:
        """Calculate anonymity score"""
        anonymity_levels = {
            "transparent": 0.3,
            "anonymous": 0.7,
            "elite": 1.0,
            "unknown": 0.5
        }
        return anonymity_levels.get(anonymity, 0.5)
    
    async def report_proxy_performance(self, proxy: str, success: bool, response_time: float):
        """Report proxy performance for ML learning"""
        
        if proxy not in self.performance_metrics:
            return
        
        metrics = self.performance_metrics[proxy]
        
        # Update success rate (moving average)
        alpha = 0.1  # Learning rate
        if success:
            metrics.success_rate = (1 - alpha) * metrics.success_rate + alpha * 1.0
        else:
            metrics.success_rate = (1 - alpha) * metrics.success_rate + alpha * 0.0
            metrics.failure_count += 1
            
            # Blacklist after too many failures
            if metrics.failure_count > 5:
                self.blacklisted_proxies.add(proxy)
        
        # Update response time (moving average)
        metrics.avg_response_time = (1 - alpha) * metrics.avg_response_time + alpha * response_time
