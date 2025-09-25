"""
Ultimate Orchestration Engine
Ties together all advanced components into a unified intelligent system
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import logging
from pathlib import Path
import yaml

# Import all our advanced components
from config.settings import UltimateConfig
from core.anti_detection.advanced_proxy_rotator import AdvancedProxyRotator, GeographicProfile
from core.anti_detection.sandbox_evasion import SandboxEvader
from core.anti_detection.kerberos_validator import KerberosUsernameValidator, KerberosConfig
from core.anti_detection.generic_mitigations import GenericMitigationAnalyzer, MitigationDatabase
from core.anti_detection.captcha_solver import AICaptchaSolver
from core.anti_detection.browser_automation import StealthBrowser
from core.anti_detection.fingerprint_manager import FingerprintManager, AdvancedFingerprint
from core.anti_detection.ml_detector import MLDetectionEvader
from utils.leet_processor import AdvancedUsernameProcessor
from platforms.base import BasePlatform
from strategies.base import BaseStrategy, StrategyType

@dataclass
class CheckRequest:
    """A username checking request with full context"""
    username: str
    platforms: List[str]
    priority: int = 1
    check_id: str = None
    user_context: Dict[str, Any] = field(default_factory=dict)
    requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CheckResult:
    """Comprehensive result of a username check"""
    request: CheckRequest
    platform_results: Dict[str, Dict[str, Any]]
    overall_stats: Dict[str, Any]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class UltimateOrchestrator:
    """
    Ultimate orchestration engine that coordinates all advanced components
    for intelligent, adaptive username checking
    """
    
    def __init__(self, config: UltimateConfig = None):
        self.config = config or UltimateConfig()
        self.logger = self._setup_logging()
        
        # Initialize all core components
        self.components = {}
        self._initialize_components()
        
        # State management
        self.active_requests: Dict[str, CheckRequest] = {}
        self.request_history: List[CheckResult] = []
        self.platform_intelligence: Dict[str, Dict] = {}
        self.performance_metrics: Dict[str, Any] = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'average_confidence': 0.0,
            'component_performance': {}
        }
        
        self.logger.info("🚀 Ultimate Orchestrator initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup advanced logging"""
        
        logger = logging.getLogger('UltimateOrchestrator')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger

    def _initialize_components(self):
        """Initialize all advanced components"""
        
        self.logger.info("Initializing advanced components...")
        
        # 1. Anti-detection components
        self.components['fingerprint_manager'] = FingerprintManager()
        self.components['proxy_rotator'] = AdvancedProxyRotator()
        self.components['sandbox_evader'] = SandboxEvader()
        self.components['mitigation_analyzer'] = GenericMitigationAnalyzer()
        self.components['ml_detector'] = MLDetectionEvader()
        self.components['captcha_solver'] = AICaptchaSolver()
        
        # 2. Platform intelligence
        self.components['kerberos_validator'] = KerberosUsernameValidator()
        self.components['username_processor'] = AdvancedUsernameProcessor()
        self.components['mitigation_database'] = MitigationDatabase()
        
        # 3. Execution engines
        self.components['browser_automation'] = StealthBrowser()
        
        self.logger.info("✅ All components initialized")

    async def initialize(self):
        """Initialize the orchestrator and all components"""
        
        self.logger.info("Starting orchestrator initialization...")
        
        # Initialize async components
        init_tasks = []
        
        if 'proxy_rotator' in self.components:
            init_tasks.append(self.components['proxy_rotator'].initialize())
        if 'ml_detector' in self.components:
            init_tasks.append(self.components['ml_detector'].load_models())
        if 'browser_automation' in self.components:
            init_tasks.append(self.components['browser_automation'].initialize())
        
        # Wait for all async initializations
        if init_tasks:
            await asyncio.gather(*init_tasks, return_exceptions=True)
        
        # Load platform intelligence
        await self._load_platform_intelligence()
        
        self.logger.info("🎯 Orchestrator fully initialized and ready")

    async def _load_platform_intelligence(self):
        """Load platform-specific intelligence and configurations"""
        
        # This would load from database or configuration files
        self.platform_intelligence = {
            'instagram': {
                'difficulty': 'high',
                'recommended_strategy': 'browser_advanced',
                'mitigations': ['canvas_fingerprinting', 'behavioral_analysis'],
                'check_timeout': 30,
                'retry_attempts': 2
            },
            'github': {
                'difficulty': 'low',
                'recommended_strategy': 'http_advanced',
                'mitigations': ['rate_limiting'],
                'check_timeout': 10,
                'retry_attempts': 3
            },
            'reddit': {
                'difficulty': 'medium',
                'recommended_strategy': 'http_basic',
                'mitigations': ['header_analysis'],
                'check_timeout': 15,
                'retry_attempts': 2
            }
            # Add more platforms...
        }

    async def check_username(self, username: str, platforms: List[str] = None, 
                           priority: int = 1, **kwargs) -> CheckResult:
        """
        Main method to check username availability across platforms
        
        Args:
            username: Target username to check
            platforms: List of platforms to check (None = all available)
            priority: Check priority (1-10, higher = more resources)
            **kwargs: Additional options
            
        Returns:
            CheckResult with comprehensive results
        """
        
        # Generate unique check ID
        check_id = f"check_{int(time.time())}_{hash(username) % 10000:04d}"
        
        # Create check request
        request = CheckRequest(
            username=username,
            platforms=platforms or list(self.platform_intelligence.keys()),
            priority=priority,
            check_id=check_id,
            user_context=kwargs
        )
        
        self.active_requests[check_id] = request
        self.performance_metrics['total_checks'] += 1
        
        self.logger.info(f"🔍 Starting check {check_id} for '{username}' on {len(request.platforms)} platforms")
        
        try:
            # Execute the comprehensive check
            result = await self._execute_comprehensive_check(request)
            
            self.performance_metrics['successful_checks'] += 1
            self.request_history.append(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Check {check_id} failed: {e}")
            self.performance_metrics['failed_checks'] += 1
            
            # Return error result
            return CheckResult(
                request=request,
                platform_results={},
                overall_stats={'error': str(e), 'success': False},
                recommendations=['Retry with different parameters'],
                metadata={'error': True, 'exception': str(e)}
            )
        
        finally:
            # Clean up
            if check_id in self.active_requests:
                del self.active_requests[check_id]

    async def _execute_comprehensive_check(self, request: CheckRequest) -> CheckResult:
        """
        Execute a comprehensive username check with all advanced features
        """
        
        start_time = time.time()
        
        # Phase 1: Pre-processing and analysis
        pre_analysis = await self._pre_process_request(request)
        
        # Phase 2: Platform-specific checking
        platform_results = {}
        platform_tasks = []
        
        for platform in request.platforms:
            task = self._check_single_platform(platform, request, pre_analysis)
            platform_tasks.append(task)
        
        # Execute platform checks with concurrency control
        results = await self._execute_with_concurrency_control(platform_tasks, request.priority)
        
        for platform, result in zip(request.platforms, results):
            if isinstance(result, Exception):
                platform_results[platform] = {
                    'success': False,
                    'error': str(result),
                    'confidence': 0.0
                }
            else:
                platform_results[platform] = result
        
        # Phase 3: Post-analysis and recommendations
        post_analysis = await self._post_process_results(request, platform_results)
        
        # Calculate overall statistics
        overall_stats = self._calculate_overall_stats(platform_results)
        
        execution_time = time.time() - start_time
        
        return CheckResult(
            request=request,
            platform_results=platform_results,
            overall_stats={
                **overall_stats,
                'execution_time': execution_time,
                'platforms_checked': len(platform_results),
                'success_rate': overall_stats.get('success_rate', 0.0)
            },
            recommendations=post_analysis['recommendations'],
            metadata={
                'pre_analysis': pre_analysis,
                'post_analysis': post_analysis,
                'execution_time': execution_time
            }
        )

    async def _pre_process_request(self, request: CheckRequest) -> Dict[str, Any]:
        """
        Pre-process the check request with advanced analysis
        """
        
        analysis = {
            'username_analysis': {},
            'platform_analysis': {},
            'risk_assessment': {},
            'strategy_recommendations': []
        }
        
        # 1. Username analysis with leet processing
        username_analysis = self.components['username_processor'].process_username(
            request.username, 
            'multi_platform'  # Generic analysis for multiple platforms
        )
        analysis['username_analysis'] = username_analysis
        
        # 2. Platform-specific analysis
        for platform in request.platforms:
            platform_info = self.platform_intelligence.get(platform, {})
            mitigation_analysis = await self.components['mitigation_analyzer'].analyze_platform_mitigations(
                platform, 
                {'url': f'https://{platform}.com', 'content': ''}  # Simulated response
            )
            
            analysis['platform_analysis'][platform] = {
                'platform_info': platform_info,
                'mitigation_analysis': mitigation_analysis,
                'recommended_strategy': platform_info.get('recommended_strategy', 'http_advanced')
            }
        
        # 3. Risk assessment
        analysis['risk_assessment'] = await self._assess_risk(request, analysis)
        
        # 4. Strategy recommendations
        analysis['strategy_recommendations'] = self._generate_strategy_recommendations(analysis)
        
        return analysis

    async def _assess_risk(self, request: CheckRequest, analysis: Dict) -> Dict[str, Any]:
        """Assess risk level for this checking operation"""
        
        risk_factors = []
        
        # Username complexity risk
        leet_confidence = analysis['username_analysis']['leet_analysis']['confidence']
        if leet_confidence > 0.7:
            risk_factors.append(('leet_username', 0.3))
        
        # Platform difficulty risk
        high_risk_platforms = [
            p for p in request.platforms 
            if self.platform_intelligence.get(p, {}).get('difficulty') in ['high', 'very_high']
        ]
        if high_risk_platforms:
            risk_factors.append(('high_risk_platforms', 0.4 * len(high_risk_platforms)))
        
        # Volume risk
        if len(request.platforms) > 10:
            risk_factors.append(('high_volume', 0.2))
        
        total_risk = sum(factor[1] for factor in risk_factors)
        
        return {
            'risk_level': 'high' if total_risk > 0.7 else 'medium' if total_risk > 0.3 else 'low',
            'risk_score': total_risk,
            'risk_factors': risk_factors,
            'recommended_precautions': self._get_risk_precautions(total_risk)
        }

    def _get_risk_precautions(self, risk_score: float) -> List[str]:
        """Get recommended precautions based on risk score"""
        
        if risk_score > 0.7:
            return [
                "Use residential proxies",
                "Enable full stealth mode",
                "Implement aggressive delays",
                "Use browser automation for all checks"
            ]
        elif risk_score > 0.3:
            return [
                "Rotate proxies between platforms",
                "Use moderate delays",
                "Enable basic stealth features"
            ]
        else:
            return [
                "Standard checking parameters",
                "Minimal delays acceptable"
            ]

    def _generate_strategy_recommendations(self, analysis: Dict) -> List[str]:
        """Generate strategy recommendations based on analysis"""
        
        recommendations = []
        
        # Platform-specific strategies
        for platform, platform_analysis in analysis['platform_analysis'].items():
            strategy = platform_analysis['recommended_strategy']
            recommendations.append(f"{platform}: Use {strategy} strategy")
        
        # Risk-based strategies
        risk_level = analysis['risk_assessment']['risk_level']
        if risk_level == 'high':
            recommendations.extend([
                "Enable sandbox detection and evasion",
                "Use ML-based detection evasion",
                "Implement advanced proxy rotation"
            ])
        
        return recommendations

    async def _check_single_platform(self, platform: str, request: CheckRequest, 
                                   pre_analysis: Dict) -> Dict[str, Any]:
        """
        Check username availability on a single platform with adaptive strategy
        """
        
        platform_start = time.time()
        
        try:
            # Get platform intelligence
            platform_info = self.platform_intelligence.get(platform, {})
            strategy_type = platform_info.get('recommended_strategy', 'http_advanced')
            
            # Select appropriate strategy
            strategy = await self._select_checking_strategy(platform, strategy_type, pre_analysis)
            
            # Prepare checking parameters
            check_params = await self._prepare_check_parameters(platform, request, pre_analysis)
            
            # Execute the check
            result = await strategy.check_username(platform, request.username, check_params)
            
            # Post-process the result
            processed_result = await self._process_platform_result(platform, result, pre_analysis)
            
            # Update performance metrics
            execution_time = time.time() - platform_start
            self._update_component_performance(platform, execution_time, True)
            
            return processed_result
            
        except Exception as e:
            self.logger.error(f"Platform check failed for {platform}: {e}")
            
            # Update performance metrics
            execution_time = time.time() - platform_start
            self._update_component_performance(platform, execution_time, False)
            
            return {
                'success': False,
                'error': str(e),
                'confidence': 0.0,
                'execution_time': execution_time
            }

    async def _select_checking_strategy(self, platform: str, strategy_type: str, 
                                      pre_analysis: Dict) -> BaseStrategy:
        """
        Select appropriate checking strategy based on platform and analysis
        """
        
        # This would interface with our strategy system
        # For now, return a mock strategy interface
        
        class AdaptiveStrategy:
            async def check_username(self, platform, username, params):
                # Mock implementation - would integrate with actual strategies
                return {
                    'exists': False,
                    'confidence': 0.8,
                    'method': strategy_type,
                    'platform': platform
                }
        
        return AdaptiveStrategy()

    async def _prepare_check_parameters(self, platform: str, request: CheckRequest,
                                      pre_analysis: Dict) -> Dict[str, Any]:
        """
        Prepare advanced checking parameters for a platform
        """
        
        params = {
            'platform': platform,
            'username': request.username,
            'strategy': pre_analysis['platform_analysis'][platform]['recommended_strategy'],
            'risk_level': pre_analysis['risk_assessment']['risk_level'],
            'leet_analysis': pre_analysis['username_analysis']['leet_analysis']
        }
        
        # Add anti-detection parameters based on risk
        if pre_analysis['risk_assessment']['risk_level'] in ['high', 'medium']:
            params.update({
                'use_proxy': True,
                'enable_stealth': True,
                'captcha_solving': True,
                'fingerprint_rotation': True
            })
            
            # Get appropriate proxy
            if 'proxy_rotator' in self.components:
                geo_profile = GeographicProfile(
                    target_country=None,  # Any country
                    avoid_countries=set(),  # No restrictions
                    preferred_cities=[],
                    diversity_required=True,
                    max_same_country=3
                )
                
                proxy = await self.components['proxy_rotator'].get_optimal_proxy(geo_profile)
                if proxy:
                    params['proxy'] = proxy
        
        return params

    async def _process_platform_result(self, platform: str, result: Dict, 
                                     pre_analysis: Dict) -> Dict[str, Any]:
        """
        Process and enhance platform check results
        """
        
        processed = result.copy()
        
        # Add confidence scoring
        if 'confidence' not in processed:
            processed['confidence'] = self._calculate_result_confidence(platform, result, pre_analysis)
        
        # Add platform intelligence
        processed['platform_intelligence'] = self.platform_intelligence.get(platform, {})
        
        # Add mitigation analysis
        platform_analysis = pre_analysis['platform_analysis'].get(platform, {})
        processed['mitigation_analysis'] = platform_analysis.get('mitigation_analysis', [])
        
        return processed

    def _calculate_result_confidence(self, platform: str, result: Dict, pre_analysis: Dict) -> float:
        """Calculate confidence score for a check result"""
        
        base_confidence = result.get('confidence', 0.5)
        
        # Adjust based on platform difficulty
        platform_info = self.platform_intelligence.get(platform, {})
        difficulty = platform_info.get('difficulty', 'medium')
        
        difficulty_multipliers = {
            'low': 1.1,
            'medium': 1.0,
            'high': 0.9,
            'very_high': 0.8
        }
        
        confidence = base_confidence * difficulty_multipliers.get(difficulty, 1.0)
        
        return min(confidence, 1.0)

    async def _execute_with_concurrency_control(self, tasks: List, priority: int) -> List:
        """
        Execute tasks with intelligent concurrency control
        """
        
        # Adjust concurrency based on priority and system load
        if priority >= 8:  # High priority
            concurrency_limit = 10
        elif priority >= 5:  # Medium priority
            concurrency_limit = 5
        else:  # Low priority
            concurrency_limit = 3
        
        # Use semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrency_limit)
        
        async def bounded_task(task):
            async with semaphore:
                return await task
        
        bounded_tasks = [bounded_task(task) for task in tasks]
        return await asyncio.gather(*bounded_tasks, return_exceptions=True)

    async def _post_process_results(self, request: CheckRequest, 
                                  platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-process results and generate recommendations
        """
        
        analysis = {
            'successful_checks': 0,
            'failed_checks': 0,
            'average_confidence': 0.0,
            'platform_analysis': {},
            'recommendations': []
        }
        
        confidences = []
        
        for platform, result in platform_results.items():
            if result.get('success', False):
                analysis['successful_checks'] += 1
                confidences.append(result.get('confidence', 0.0))
            else:
                analysis['failed_checks'] += 1
            
            # Platform-specific analysis
            analysis['platform_analysis'][platform] = {
                'success': result.get('success', False),
                'confidence': result.get('confidence', 0.0),
                'method': result.get('method', 'unknown'),
                'needs_retry': self._needs_retry(platform, result)
            }
        
        # Calculate average confidence
        if confidences:
            analysis['average_confidence'] = sum(confidences) / len(confidences)
            self.performance_metrics['average_confidence'] = (
                self.performance_metrics['average_confidence'] + analysis['average_confidence']
            ) / 2
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_post_recommendations(request, platform_results, analysis)
        
        return analysis

    def _needs_retry(self, platform: str, result: Dict) -> bool:
        """Determine if a platform check needs retry"""
        
        if result.get('success', False):
            return False
        
        # Retry if confidence is low but no clear error
        if result.get('confidence', 0.0) < 0.5 and 'error' not in result:
            return True
        
        # Retry on specific error types
        error = result.get('error', '').lower()
        retry_errors = ['timeout', 'rate limit', 'temporary', 'captcha']
        
        if any(retry_error in error for retry_error in retry_errors):
            return True
        
        return False

    def _generate_post_recommendations(self, request: CheckRequest, 
                                     platform_results: Dict, analysis: Dict) -> List[str]:
        """Generate post-check recommendations"""
        
        recommendations = []
        
        # Success rate recommendations
        success_rate = analysis['successful_checks'] / len(platform_results) if platform_results else 0
        
        if success_rate < 0.5:
            recommendations.extend([
                "Consider using higher-quality proxies",
                "Increase delay between requests",
                "Try alternative checking strategies for failed platforms"
            ])
        
        # Platform-specific recommendations
        for platform, result in platform_results.items():
            if not result.get('success', False) and self._needs_retry(platform, result):
                recommendations.append(f"Retry {platform} with different parameters")
        
        # Confidence-based recommendations
        if analysis['average_confidence'] < 0.7:
            recommendations.append("Results have low confidence - consider manual verification")
        
        return recommendations

    def _calculate_overall_stats(self, platform_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall statistics from platform results"""
        
        total = len(platform_results)
        successful = sum(1 for r in platform_results.values() if r.get('success', False))
        confidences = [r.get('confidence', 0.0) for r in platform_results.values() if r.get('success', False)]
        
        return {
            'total_platforms': total,
            'successful_checks': successful,
            'failed_checks': total - successful,
            'success_rate': successful / total if total > 0 else 0.0,
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0.0,
            'max_confidence': max(confidences) if confidences else 0.0,
            'min_confidence': min(confidences) if confidences else 0.0
        }

    def _update_component_performance(self, platform: str, execution_time: float, success: bool):
        """Update component performance metrics"""
        
        if platform not in self.performance_metrics['component_performance']:
            self.performance_metrics['component_performance'][platform] = {
                'total_checks': 0,
                'successful_checks': 0,
                'average_time': 0.0,
                'last_check': time.time()
            }
        
        perf = self.performance_metrics['component_performance'][platform]
        perf['total_checks'] += 1
        
        if success:
            perf['successful_checks'] += 1
        
        # Update average time (moving average)
        alpha = 0.1
        perf['average_time'] = (1 - alpha) * perf['average_time'] + alpha * execution_time
        perf['last_check'] = time.time()

    async def batch_check_usernames(self, usernames: List[str], platforms: List[str] = None,
                                  max_concurrent: int = 5) -> Dict[str, CheckResult]:
        """
        Perform batch username checking with intelligent resource management
        """
        
        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def check_single_user(username: str):
            async with semaphore:
                result = await self.check_username(username, platforms)
                return username, result
        
        # Create tasks for all usernames
        tasks = [check_single_user(username) for username in usernames]
        
        # Execute with progress tracking
        completed = 0
        total = len(tasks)
        
        for task in asyncio.as_completed(tasks):
            username, result = await task
            results[username] = result
            
            completed += 1
            progress = (completed / total) * 100
            self.logger.info(f"📊 Batch progress: {completed}/{total} ({progress:.1f}%)")
        
        return results

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        return {
            'performance_metrics': self.performance_metrics,
            'active_requests': len(self.active_requests),
            'total_checks_completed': len(self.request_history),
            'component_status': {
                name: 'active' for name in self.components.keys()
            },
            'platform_intelligence': {
                'total_platforms': len(self.platform_intelligence),
                'platforms_loaded': list(self.platform_intelligence.keys())
            },
            'system_health': self._assess_system_health()
        }

    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health"""
        
        health_indicators = []
        
        # Check component health
        for name, component in self.components.items():
            if hasattr(component, 'health_check'):
                try:
                    health = component.health_check()
                    health_indicators.append((name, health))
                except Exception as e:
                    health_indicators.append((name, f"error: {e}"))
        
        # Check performance health
        success_rate = (self.performance_metrics['successful_checks'] / 
                       self.performance_metrics['total_checks']) if self.performance_metrics['total_checks'] > 0 else 0
        
        if success_rate > 0.8:
            performance_health = 'excellent'
        elif success_rate > 0.6:
            performance_health = 'good'
        elif success_rate > 0.4:
            performance_health = 'fair'
        else:
            performance_health = 'poor'
        
        return {
            'overall_health': 'healthy' if success_rate > 0.6 else 'degraded',
            'performance_health': performance_health,
            'success_rate': success_rate,
            'component_health': dict(health_indicators)
        }

    async def shutdown(self):
        """Gracefully shutdown the orchestrator and all components"""
        
        self.logger.info("Shutting down orchestrator...")
        
        # Shutdown browser automation
        if 'browser_automation' in self.components:
            await self.components['browser_automation'].close()
        
        # Close other resources
        if 'proxy_rotator' in self.components:
            # Proxy rotator cleanup if needed
            pass
        
        self.logger.info("Orchestrator shutdown complete")

# Advanced result visualization and export
class ResultProcessor:
    """Process and export check results in various formats"""
    
    @staticmethod
    def generate_detailed_report(check_result: CheckResult) -> str:
        """Generate detailed text report"""
        
        report = []
        report.append("🎯 ULTIMATE USERNAME CHECK REPORT")
        report.append("=" * 60)
        report.append(f"Username: {check_result.request.username}")
        report.append(f"Platforms Checked: {len(check_result.platform_results)}")
        report.append(f"Overall Success Rate: {check_result.overall_stats.get('success_rate', 0):.1%}")
        report.append(f"Execution Time: {check_result.overall_stats.get('execution_time', 0):.2f}s")
        report.append("")
        
        # Platform results
        report.append("PLATFORM RESULTS:")
        report.append("-" * 40)
        
        for platform, result in check_result.platform_results.items():
            status = "✅ AVAILABLE" if not result.get('exists', False) else "❌ TAKEN"
            confidence = result.get('confidence', 0)
            method = result.get('method', 'unknown')
            
            report.append(f"{platform:15} {status:15} Confidence: {confidence:.1%} Method: {method}")
            
            if 'error' in result:
                report.append(f"    Error: {result['error']}")
        
        # Recommendations
        if check_result.recommendations:
            report.append("")
            report.append("RECOMMENDATIONS:")
            report.append("-" * 40)
            for rec in check_result.recommendations:
                report.append(f"• {rec}")
        
        return "\n".join(report)
    
    @staticmethod
    def export_to_json(check_result: CheckResult, filename: str = None) -> str:
        """Export results to JSON format"""
        
        export_data = {
            'check_id': check_result.request.check_id,
            'username': check_result.request.username,
            'timestamp': time.time(),
            'overall_stats': check_result.overall_stats,
            'platform_results': check_result.platform_results,
            'recommendations': check_result.recommendations,
            'metadata': check_result.metadata
        }
        
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def export_to_csv(check_results: List[CheckResult], filename: str = None) -> str:
        """Export multiple results to CSV format"""
        
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Username', 'Platform', 'Available', 'Confidence', 'Method', 'Timestamp'])
        
        for result in check_results:
            for platform, platform_result in result.platform_results.items():
                available = not platform_result.get('exists', False)
                confidence = platform_result.get('confidence', 0)
                method = platform_result.get('method', 'unknown')
                
                writer.writerow([
                    result.request.username,
                    platform,
                    available,
                    confidence,
                    method,
                    time.strftime('%Y-%m-%d %H:%M:%S')
                ])
        
        csv_content = output.getvalue()
        
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                f.write(csv_content)
        
        return csv_content

# Example usage
async def demonstrate_orchestrator():
    """Demonstrate the ultimate orchestrator in action"""
    
    print("🚀 ULTIMATE USERNAME CHECK ORCHESTRATOR DEMO")
    print("=" * 60)
    
    # Create configuration
    config = UltimateConfig()
    
    # Initialize orchestrator
    orchestrator = UltimateOrchestrator(config)
    await orchestrator.initialize()
    
    # Check system status
    status = orchestrator.get_system_status()
    print(f"✅ System Status: {status['system_health']['overall_health']}")
    print(f"📊 Platforms Loaded: {len(status['platform_intelligence']['platforms_loaded'])}")
    
    # Test username check
    test_usernames = ["john_doe", "xX_dark_5h4d0w_Xx", "test_user_123"]
    test_platforms = ["instagram", "github", "reddit"]
    
    for username in test_usernames:
        print(f"\n🔍 Checking username: {username}")
        print("-" * 40)
        
        result = await orchestrator.check_username(username, test_platforms)
        
        # Display results
        for platform, platform_result in result.platform_results.items():
            status = "✅ AVAILABLE" if not platform_result.get('exists', False) else "❌ TAKEN"
            confidence = platform_result.get('confidence', 0)
            print(f"   {platform:12} {status:15} Confidence: {confidence:.1%}")
    
    # Generate report
    if test_usernames:
        sample_result = await orchestrator.check_username(test_usernames[0], test_platforms[:1])
        report = ResultProcessor.generate_detailed_report(sample_result)
        print(f"\n📄 Sample Report:\n{report}")
    
    # Cleanup
    await orchestrator.shutdown()
    print("\n🎉 Demonstration completed successfully!")

if __name__ == "__main__":
    asyncio.run(demonstrate_orchestrator())
