"""
Real-time Behavior Analysis and Adaptation System
"""

import asyncio
import time
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass
import logging
from collections import deque

@dataclass
class BehaviorPattern:
    """Pattern of user behavior for analysis"""
    action_type: str
    timestamp: float
    duration: float
    success: bool
    metadata: Dict[str, Any]

class BehaviorAnalyzer:
    """Real-time behavior analysis and adaptation system"""
    
    def __init__(self, window_size: int = 100):
        self.behavior_history = deque(maxlen=window_size)
        self.pattern_detector = PatternDetector()
        self.anomaly_detector = AnomalyDetector()
        self.adaptation_engine = AdaptationEngine()
        self.logger = logging.getLogger(__name__)
        
        # Behavior metrics
        self.metrics = {
            'success_rate': 0.0,
            'avg_response_time': 0.0,
            'request_frequency': 0.0,
            'error_patterns': {},
            'detection_events': 0
        }
    
    async def record_behavior(self, action: str, duration: float, success: bool, metadata: Dict = None):
        """Record a behavior pattern"""
        
        pattern = BehaviorPattern(
            action_type=action,
            timestamp=time.time(),
            duration=duration,
            success=success,
            metadata=metadata or {}
        )
        
        self.behavior_history.append(pattern)
        
        # Update metrics
        await self._update_metrics(pattern)
        
        # Detect patterns and anomalies
        await self._analyze_patterns()
        await self._detect_anomalies()
    
    async def _update_metrics(self, pattern: BehaviorPattern):
        """Update behavior metrics"""
        
        # Calculate success rate
        recent_patterns = list(self.behavior_history)[-50:]  # Last 50 actions
        if recent_patterns:
            success_count = sum(1 for p in recent_patterns if p.success)
            self.metrics['success_rate'] = success_count / len(recent_patterns)
        
        # Calculate average response time
        if recent_patterns:
            avg_duration = np.mean([p.duration for p in recent_patterns])
            self.metrics['avg_response_time'] = avg_duration
        
        # Update error patterns
        if not pattern.success:
            error_type = pattern.metadata.get('error_type', 'unknown')
            self.metrics['error_patterns'][error_type] = self.metrics['error_patterns'].get(error_type, 0) + 1
    
    async def _analyze_patterns(self):
        """Analyze behavior patterns for detection risks"""
        
        if len(self.behavior_history) < 10:
            return
        
        # Detect timing patterns that might indicate automation
        timing_pattern = await self.pattern_detector.analyze_timing(self.behavior_history)
        
        if timing_pattern['risk_level'] == 'HIGH':
            self.logger.warning("Detected risky timing pattern")
            await self.adaptation_engine.adapt_timing_strategy()
        
        # Detect request pattern anomalies
        request_pattern = await self.pattern_detector.analyze_requests(self.behavior_history)
        
        if request_pattern['anomaly_detected']:
            self.metrics['detection_events'] += 1
            await self.adaptation_engine.adapt_request_pattern()
    
    async def _detect_anomalies(self):
        """Detect behavioral anomalies"""
        
        if len(self.behavior_history) < 20:
            return
        
        anomalies = await self.anomaly_detector.detect_anomalies(self.behavior_history)
        
        for anomaly in anomalies:
            if anomaly['severity'] > 0.8:
                self.logger.warning(f"Behavioral anomaly detected: {anomaly['type']}")
                await self.adaptation_engine.trigger_evasion_protocol(anomaly)
    
    async def get_adaptation_recommendations(self) -> List[Dict]:
        """Get recommendations for behavior adaptation"""
        
        recommendations = []
        
        # Timing recommendations
        if self.metrics['success_rate'] < 0.7:
            recommendations.append({
                'type': 'timing',
                'action': 'increase_delays',
                'reason': 'Low success rate detected',
                'confidence': 0.8
            })
        
        # Pattern recommendations
        if self.metrics['detection_events'] > 3:
            recommendations.append({
                'type': 'pattern',
                'action': 'change_behavior_sequence',
                'reason': 'Multiple detection events',
                'confidence': 0.9
            })
        
        return recommendations
    
    async def generate_stealth_parameters(self) -> Dict:
        """Generate stealth parameters based on current behavior analysis"""
        
        base_delay = max(1.0, self.metrics['avg_response_time'] * 1.5)
        
        return {
            'request_delay': base_delay + np.random.uniform(0.5, 2.0),
            'randomization_factor': 0.3 if self.metrics['success_rate'] < 0.8 else 0.1,
            'proxy_rotation_frequency': 'high' if self.metrics['detection_events'] > 2 else 'normal',
            'fingerprint_rotation': self.metrics['success_rate'] < 0.6,
            'behavior_simulation_intensity': 'high' if self.metrics['detection_events'] > 0 else 'medium'
        }

class PatternDetector:
    """Detect patterns in behavior that might indicate automation"""
    
    async def analyze_timing(self, behavior_history: deque) -> Dict:
        """Analyze timing patterns for automation detection"""
        
        timings = [pattern.duration for pattern in behavior_history]
        
        if len(timings) < 5:
            return {'risk_level': 'LOW', 'confidence': 0.0}
        
        # Check for too-perfect timing (indicating automation)
        cv = np.std(timings) / np.mean(timings)  # Coefficient of variation
        
        if cv < 0.1:  # Very low variation
            return {'risk_level': 'HIGH', 'confidence': 0.9, 'pattern': 'consistent_timing'}
        elif cv < 0.3:
            return {'risk_level': 'MEDIUM', 'confidence': 0.7, 'pattern': 'low_variation_timing'}
        else:
            return {'risk_level': 'LOW', 'confidence': 0.8, 'pattern': 'human_like_timing'}
    
    async def analyze_requests(self, behavior_history: deque) -> Dict:
        """Analyze request patterns for anomalies"""
        
        # Analyze frequency and sequence patterns
        timestamps = [pattern.timestamp for pattern in behavior_history]
        intervals = np.diff(timestamps)
        
        if len(intervals) < 3:
            return {'anomaly_detected': False}
        
        # Detect burst patterns
        burst_threshold = np.percentile(intervals, 10)
        burst_count = sum(1 for interval in intervals if interval < burst_threshold)
        
        burst_ratio = burst_count / len(intervals)
        
        if burst_ratio > 0.3:
            return {
                'anomaly_detected': True,
                'type': 'request_burst',
                'severity': min(burst_ratio, 1.0)
            }
        
        return {'anomaly_detected': False}

class AnomalyDetector:
    """Detect behavioral anomalies that might trigger detection"""
    
    async def detect_anomalies(self, behavior_history: deque) -> List[Dict]:
        """Detect various types of behavioral anomalies"""
        
        anomalies = []
        
        # Check for error spikes
        error_anomaly = await self._detect_error_anomalies(behavior_history)
        if error_anomaly:
            anomalies.append(error_anomaly)
        
        # Check for timing anomalies
        timing_anomaly = await self._detect_timing_anomalies(behavior_history)
        if timing_anomaly:
            anomalies.append(timing_anomaly)
        
        return anomalies
    
    async def _detect_error_anomalies(self, behavior_history: deque) -> Optional[Dict]:
        """Detect anomalies in error patterns"""
        
        recent_patterns = list(behavior_history)[-20:]
        error_count = sum(1 for p in recent_patterns if not p.success)
        
        if error_count > 5:  # More than 25% errors in recent actions
            return {
                'type': 'error_spike',
                'severity': min(error_count / 20.0, 1.0),
                'description': f'High error rate: {error_count}/20 recent actions failed'
            }
        
        return None
    
    async def _detect_timing_anomalies(self, behavior_history: deque) -> Optional[Dict]:
        """Detect timing anomalies"""
        
        recent_timings = [p.duration for p in list(behavior_history)[-10:]]
        
        if len(recent_timings) < 5:
            return None
        
        # Use Z-score to detect outliers
        mean_timing = np.mean(recent_timings)
        std_timing = np.std(recent_timings)
        
        if std_timing == 0:
            return None
        
        z_scores = [(t - mean_timing) / std_timing for t in recent_timings]
        outlier_count = sum(1 for z in z_scores if abs(z) > 2.0)
        
        if outlier_count > 2:
            return {
                'type': 'timing_outliers',
                'severity': outlier_count / len(recent_timings),
                'description': f'Multiple timing outliers detected: {outlier_count}'
            }
        
        return None

class AdaptationEngine:
    """Engine for adapting behavior based on analysis"""
    
    async def adapt_timing_strategy(self):
        """Adapt timing strategy based on detection patterns"""
        
        # Increase randomization in delays
        # Change timing patterns
        pass
    
    async def adapt_request_pattern(self):
        """Adapt request patterns to avoid detection"""
        
        # Change the sequence and frequency of requests
        # Introduce more human-like variability
        pass
    
    async def trigger_evasion_protocol(self, anomaly: Dict):
        """Trigger specific evasion protocols based on anomaly type"""
        
        if anomaly['type'] == 'error_spike':
            # Switch to more conservative mode
            await self._activate_stealth_mode()
        
        elif anomaly['type'] == 'timing_outliers':
            # Reset timing patterns
            await self._reset_timing_strategy()
    
    async def _activate_stealth_mode(self):
        """Activate maximum stealth mode"""
        
        # Implement stealth protocol
        pass
    
    async def _reset_timing_strategy(self):
        """Reset and randomize timing strategy"""
        
        # Implement timing reset
        pass
