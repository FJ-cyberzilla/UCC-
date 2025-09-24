"""
Advanced Kerberos Username Validation
Enterprise-level username enumeration through Kerberos protocol analysis
"""

import asyncio
import socket
import struct
import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import logging
import hashlib
import hmac
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import asn1crypto.core
import asn1crypto.kerberos

# Try to import additional cryptographic libraries
try:
    from Crypto.Cipher import AES, DES, DES3
    from Crypto.Hash import MD4, MD5
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

@dataclass
class KerberosConfig:
    """Kerberos configuration for username validation"""
    kdc_host: str = 'localhost'
    kdc_port: int = 88
    realm: str = 'EXAMPLE.COM'
    timeout: int = 10
    max_retries: int = 3

@dataclass
class KerberosValidationResult:
    """Result of Kerberos username validation"""
    username: str
    exists: bool
    confidence: float
    error: Optional[str] = None
    preauth_required: bool = False
    account_locked: bool = False
    password_expired: bool = False
    additional_info: Dict = None

class KerberosUsernameValidator:
    """
    Advanced Kerberos username validator using protocol-level analysis
    Can detect valid usernames through Kerberos error code analysis
    """
    
    def __init__(self, config: KerberosConfig = None):
        self.config = config or KerberosConfig()
        self.logger = logging.getLogger(__name__)
        self.socket_timeout = self.config.timeout
        self.sequence_number = 1
        
        # Kerberos message types
        self.AS_REQ = 10
        self.AS_REP = 11
        self.ERROR = 30
        
        # Pre-authentication types
        self.PA_ENC_TIMESTAMP = 2
        self.PA_PK_AS_REQ = 16
        self.PA_ETYPE_INFO2 = 19
        
        # Error codes for username enumeration
        self.ERROR_CODES = {
            # Username exists but pre-auth required
            'PREAUTH_REQUIRED': 25,
            # Username doesn't exist
            'CLIENT_NOT_FOUND': 6,
            # Account locked/disabled
            'CLIENT_REVOKED': 8,
            # Password expired
            'PASSWORD_EXPIRED': 32,
        }
        
        # Encryption types supported
        self.ENCRYPTION_TYPES = {
            1: 'des-cbc-crc',
            3: 'des-cbc-md5',
            16: 'aes128-cts-hmac-sha1-96',
            17: 'aes256-cts-hmac-sha1-96',
            18: 'aes128-cts-hmac-sha256-128',
            19: 'aes256-cts-hmac-sha384-192',
            23: 'rc4-hmac',  # NT hash
        }

    async def validate_username(self, username: str, domain: str = None) -> KerberosValidationResult:
        """
        Validate username existence through Kerberos protocol analysis
        
        Args:
            username: Target username to validate
            domain: Domain/realm (optional, uses config realm if not provided)
        
        Returns:
            KerberosValidationResult with existence confidence
        """
        
        realm = domain or self.config.realm
        principal = f"{username}@{realm}"
        
        self.logger.info(f"Validating Kerberos username: {principal}")
        
        try:
            # Method 1: Basic AS-REQ without pre-authentication
            result = await self._as_request_validation(principal)
            if result.exists or result.error:
                return result
            
            # Method 2: Pre-authentication probing
            if result.preauth_required:
                result = await self._preauth_probing(principal)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Kerberos validation failed for {principal}: {e}")
            return KerberosValidationResult(
                username=username,
                exists=False,
                confidence=0.0,
                error=str(e)
            )

    async def _as_request_validation(self, principal: str) -> KerberosValidationResult:
        """
        Perform AS-REQ validation without pre-authentication
        Analyzes error codes to determine username existence
        """
        
        try:
            # Create AS-REQ message
            as_req = self._build_as_req(principal)
            
            # Send to KDC and get response
            response = await self._send_kerberos_message(as_req)
            
            if not response:
                return KerberosValidationResult(
                    username=principal.split('@')[0],
                    exists=False,
                    confidence=0.1,
                    error="No response from KDC"
                )
            
            # Parse response to determine username status
            return self._analyze_as_response(response, principal)
            
        except Exception as e:
            return KerberosValidationResult(
                username=principal.split('@')[0],
                exists=False,
                confidence=0.0,
                error=f"AS-REQ validation failed: {e}"
            )

    async def _preauth_probing(self, principal: str) -> KerberosValidationResult:
        """
        Perform pre-authentication probing for more accurate detection
        """
        
        try:
            # Get pre-authentication requirements
            pa_data = await self._get_preauth_data(principal)
            
            if not pa_data:
                return KerberosValidationResult(
                    username=principal.split('@')[0],
                    exists=True,  # Pre-auth required means username exists
                    confidence=0.85,
                    preauth_required=True
                )
            
            # Try different pre-auth methods to gather more info
            result = await self._try_preauth_methods(principal, pa_data)
            return result
            
        except Exception as e:
            self.logger.warning(f"Pre-auth probing failed for {principal}: {e}")
            # Fallback to basic detection
            return KerberosValidationResult(
                username=principal.split('@')[0],
                exists=True,
                confidence=0.7,
                preauth_required=True,
                error=f"Pre-auth probing failed: {e}"
            )

    def _build_as_req(self, principal: str) -> bytes:
        """
        Build AS-REQ Kerberos message
        """
        
        # Current time
        now = int(time.time())
        
        # Build the AS-REQ structure
        as_req = {
            'pvno': 5,  # Kerberos version 5
            'msg-type': self.AS_REQ,
            'padata': [],  # No pre-authentication
            'req-body': {
                'kdc-options': {
                    'forwardable': False,
                    'proxiable': False,
                    'allow-postdate': False,
                    'renewable': False,
                },
                'cname': {
                    'name-type': 1,  # NT-PRINCIPAL
                    'name-string': [principal.split('@')[0]]
                },
                'realm': principal.split('@')[1],
                'sname': {
                    'name-type': 2,  # NT-SRV-INST
                    'name-string': ['krbtgt', principal.split('@')[1]]
                },
                'till': now + 3600,  # 1 hour validity
                'rtime': now + 3600,
                'nonce': self._generate_nonce(),
                'etype': [18, 17, 16, 23, 3, 1]  # Supported encryption types
            }
        }
        
        return self._encode_kerberos_message(as_req)

    def _build_preauth_req(self, principal: str, pa_data: List) -> bytes:
        """
        Build AS-REQ with pre-authentication data
        """
        
        as_req = self._build_as_req(principal)
        # Add pre-authentication data
        # This would be implemented based on the specific pre-auth type
        
        return as_req

    async def _send_kerberos_message(self, message: bytes) -> Optional[bytes]:
        """
        Send Kerberos message to KDC and receive response
        """
        
        try:
            # Create TCP connection to KDC
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.config.kdc_host, self.config.kdc_port),
                timeout=self.socket_timeout
            )
            
            try:
                # Kerberos messages are length-prefixed
                message_len = struct.pack('>I', len(message))
                writer.write(message_len + message)
                await writer.drain()
                
                # Read response length
                len_data = await asyncio.wait_for(reader.read(4), timeout=self.socket_timeout)
                if len(len_data) != 4:
                    return None
                
                response_len = struct.unpack('>I', len_data)[0]
                
                # Read response
                response = await asyncio.wait_for(reader.read(response_len), timeout=self.socket_timeout)
                return response
                
            finally:
                writer.close()
                await writer.wait_closed()
                
        except (asyncio.TimeoutError, ConnectionError, OSError) as e:
            self.logger.warning(f"Network error communicating with KDC: {e}")
            return None

    def _analyze_as_response(self, response: bytes, principal: str) -> KerberosValidationResult:
        """
        Analyze AS-REP or ERROR response to determine username status
        """
        
        try:
            # Parse the response
            parsed_response = self._decode_kerberos_message(response)
            msg_type = parsed_response.get('msg-type')
            
            if msg_type == self.AS_REP:
                # Received AS-REP - extremely rare without pre-auth, but indicates valid user
                return KerberosValidationResult(
                    username=principal.split('@')[0],
                    exists=True,
                    confidence=0.99,
                    preauth_required=False
                )
            
            elif msg_type == self.ERROR:
                # Analyze error code for username enumeration
                error_code = parsed_response.get('error-code', 0)
                return self._interpret_error_code(error_code, principal)
            
            else:
                return KerberosValidationResult(
                    username=principal.split('@')[0],
                    exists=False,
                    confidence=0.3,
                    error=f"Unexpected message type: {msg_type}"
                )
                
        except Exception as e:
            return KerberosValidationResult(
                username=principal.split('@')[0],
                exists=False,
                confidence=0.2,
                error=f"Response analysis failed: {e}"
            )

    def _interpret_error_code(self, error_code: int, principal: str) -> KerberosValidationResult:
        """
        Interpret Kerberos error codes for username validation
        """
        
        username = principal.split('@')[0]
        
        if error_code == self.ERROR_CODES['PREAUTH_REQUIRED']:
            # Pre-authentication required - username exists!
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.95,
                preauth_required=True
            )
        
        elif error_code == self.ERROR_CODES['CLIENT_NOT_FOUND']:
            # Client not found - username doesn't exist
            return KerberosValidationResult(
                username=username,
                exists=False,
                confidence=0.90,
                error="Username not found in Kerberos database"
            )
        
        elif error_code == self.ERROR_CODES['CLIENT_REVOKED']:
            # Client revoked - username exists but account is locked/disabled
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.98,
                account_locked=True,
                error="Account is locked or disabled"
            )
        
        elif error_code == self.ERROR_CODES['PASSWORD_EXPIRED']:
            # Password expired - username exists but password needs changing
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.98,
                password_expired=True,
                error="Password has expired"
            )
        
        else:
            # Other error codes - ambiguous results
            confidence = 0.5  # Neutral confidence
            exists = None
            
            # Some error codes still indicate username existence
            if error_code in [7, 9, 10]:  # Various policy violations
                exists = True
                confidence = 0.8
            
            return KerberosValidationResult(
                username=username,
                exists=exists if exists is not None else False,
                confidence=confidence,
                error=f"Kerberos error code: {error_code}"
            )

    async def _get_preauth_data(self, principal: str) -> Optional[List]:
        """
        Retrieve pre-authentication data requirements from KDC
        """
        
        try:
            # Send initial AS-REQ to get pre-auth requirements
            as_req = self._build_as_req(principal)
            response = await self._send_kerberos_message(as_req)
            
            if response:
                parsed = self._decode_kerberos_message(response)
                if parsed.get('msg-type') == self.ERROR:
                    return parsed.get('padata', [])
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Failed to get pre-auth data for {principal}: {e}")
            return None

    async def _try_preauth_methods(self, principal: str, pa_data: List) -> KerberosValidationResult:
        """
        Try different pre-authentication methods to gather more information
        """
        
        username = principal.split('@')[0]
        
        # Analyze available pre-auth types
        pa_types = [pa.get('padata-type') for pa in pa_data]
        
        if self.PA_ENC_TIMESTAMP in pa_types:
            # Timestamp pre-auth - most common
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.97,
                preauth_required=True,
                additional_info={'preauth_type': 'enc_timestamp'}
            )
        
        elif self.PA_PK_AS_REQ in pa_types:
            # Public key pre-auth
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.96,
                preauth_required=True,
                additional_info={'preauth_type': 'pk_init'}
            )
        
        else:
            # Other pre-auth types
            return KerberosValidationResult(
                username=username,
                exists=True,
                confidence=0.90,
                preauth_required=True,
                additional_info={'preauth_types': pa_types}
            )

    def _encode_kerberos_message(self, message_dict: Dict) -> bytes:
        """
        Encode Python dictionary to Kerberos ASN.1 format
        This is a simplified implementation
        """
        
        # In a full implementation, this would use asn1crypto or similar
        # to properly encode the Kerberos messages
        
        # Placeholder implementation
        try:
            # Simple serialization for demonstration
            # Real implementation would use proper ASN.1 encoding
            import json
            return json.dumps(message_dict).encode()
        except:
            # Fallback to basic encoding
            return str(message_dict).encode()

    def _decode_kerberos_message(self, message_bytes: bytes) -> Dict:
        """
        Decode Kerberos ASN.1 message to Python dictionary
        """
        
        try:
            # Placeholder implementation
            # Real implementation would use proper ASN.1 decoding
            import json
            return json.loads(message_bytes.decode())
        except:
            # Basic parsing for error codes
            message_str = message_bytes.decode('latin-1', errors='ignore')
            
            # Extract basic information
            result = {'msg-type': self.ERROR}  # Default to error
            
            # Simple error code extraction (simplified)
            if 'PREAUTH_REQUIRED' in message_str:
                result['error-code'] = self.ERROR_CODES['PREAUTH_REQUIRED']
            elif 'CLIENT_NOT_FOUND' in message_str:
                result['error-code'] = self.ERROR_CODES['CLIENT_NOT_FOUND']
            
            return result

    def _generate_nonce(self) -> int:
        """Generate random nonce for Kerberos messages"""
        self.sequence_number += 1
        return (int(time.time()) << 16) | (self.sequence_number & 0xFFFF)

    async def batch_validate_usernames(self, usernames: List[str], domain: str = None) -> Dict[str, KerberosValidationResult]:
        """
        Validate multiple usernames efficiently
        
        Args:
            usernames: List of usernames to validate
            domain: Domain/realm for validation
        
        Returns:
            Dictionary mapping usernames to validation results
        """
        
        results = {}
        
        # Use semaphore to limit concurrent connections
        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent connections
        
        async def validate_single(username: str):
            async with semaphore:
                result = await self.validate_username(username, domain)
                return username, result
        
        # Validate all usernames concurrently
        tasks = [validate_single(username) for username in usernames]
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in completed:
            if isinstance(result, tuple) and len(result) == 2:
                username, validation_result = result
                if isinstance(validation_result, KerberosValidationResult):
                    results[username] = validation_result
        
        return results

class AdvancedKerberosTechniques:
    """
    Advanced Kerberos techniques for enterprise environments
    """
    
    def __init__(self, validator: KerberosUsernameValidator):
        self.validator = validator
        self.logger = logging.getLogger(__name__)
    
    async def user_enumeration_via_udp(self, usernames: List[str], domain: str) -> Dict[str, bool]:
        """
        User enumeration via UDP Kerberos packets (faster but less reliable)
        """
        
        results = {}
        
        for username in usernames:
            try:
                # UDP-based quick check
                result = await self._udp_kerberos_check(f"{username}@{domain}")
                results[username] = result
                
                # Small delay to avoid detection
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.debug(f"UDP check failed for {username}: {e}")
                results[username] = False
        
        return results
    
    async def _udp_kerberos_check(self, principal: str) -> bool:
        """
        Quick UDP-based Kerberos check
        """
        
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.validator.config.timeout)
            
            # Build minimal AS-REQ
            as_req = self.validator._build_as_req(principal)
            
            # Send via UDP
            kdc_address = (self.validator.config.kdc_host, self.validator.config.kdc_port)
            sock.sendto(as_req, kdc_address)
            
            # Wait for response
            response, _ = sock.recvfrom(4096)
            sock.close()
            
            # Quick analysis of response
            return b'PREAUTH_REQUIRED' in response or b'AS-REP' in response
            
        except socket.timeout:
            return False  # No response often means user doesn't exist
        except Exception:
            return False
    
    async def timing_attack_enumeration(self, usernames: List[str], domain: str) -> Dict[str, float]:
        """
        Timing-based username enumeration attack
        Measures response times to infer username existence
        """
        
        timing_results = {}
        
        for username in usernames:
            try:
                principal = f"{username}@{domain}"
                
                # Measure response time
                start_time = time.time()
                await self.validator.validate_username(username, domain)
                end_time = time.time()
                
                response_time = end_time - start_time
                timing_results[username] = response_time
                
            except Exception as e:
                self.logger.debug(f"Timing attack failed for {username}: {e}")
                timing_results[username] = float('inf')
        
        # Analyze timing patterns
        return self._analyze_timing_patterns(timing_results)
    
    def _analyze_timing_patterns(self, timings: Dict[str, float]) -> Dict[str, float]:
        """
        Analyze timing patterns to infer username existence
        """
        
        if not timings:
            return {}
        
        # Calculate statistics
        valid_timings = [t for t in timings.values() if t != float('inf')]
        if not valid_timings:
            return {user: 0.0 for user in timings.keys()}
        
        avg_time = sum(valid_timings) / len(valid_timings)
        std_time = (sum((t - avg_time) ** 2 for t in valid_timings) / len(valid_timings)) ** 0.5
        
        # Score based on deviation from average
        results = {}
        for username, timing in timings.items():
            if timing == float('inf'):
                results[username] = 0.0
            else:
                # Users that exist often have different response times
                deviation = abs(timing - avg_time) / std_time if std_time > 0 else 0
                confidence = min(deviation * 0.5, 1.0)  # Normalize to 0-1
                results[username] = confidence
        
        return results

# Utility functions for Kerberos operations
class KerberosUtils:
    """Utility functions for Kerberos operations"""
    
    @staticmethod
    def normalize_username(username: str, domain: str = None) -> str:
        """Normalize username to principal format"""
        
        if '@' in username:
            return username.upper()
        elif domain:
            return f"{username.upper()}@{domain.upper()}"
        else:
            return username.upper()
    
    @staticmethod
    def extract_domain_from_principal(principal: str) -> str:
        """Extract domain from Kerberos principal"""
        
        if '@' in principal:
            return principal.split('@')[1]
        return ''
    
    @staticmethod
    def is_valid_principal(principal: str) -> bool:
        """Validate Kerberos principal format"""
        
        if not principal or '@' not in principal:
            return False
        
        username, domain = principal.split('@', 1)
        return bool(username.strip()) and bool(domain.strip())
    
    @staticmethod
    async def discover_kdc(domain: str) -> List[str]:
        """Discover KDC servers for a domain using DNS SRV records"""
        
        try:
            import dns.resolver
            import dns.rdatatype
            
            kdc_servers = []
            
            # Try _kerberos._tcp SRV record
            try:
                answers = dns.resolver.resolve(f'_kerberos._tcp.{domain}', 'SRV')
                for answer in answers:
                    kdc_servers.append(str(answer.target).rstrip('.'))
            except dns.resolver.NoAnswer:
                pass
            
            # Try _kerberos._udp SRV record
            try:
                answers = dns.resolver.resolve(f'_kerberos._udp.{domain}', 'SRV')
                for answer in answers:
                    kdc_servers.append(str(answer.target).rstrip('.'))
            except dns.resolver.NoAnswer:
                pass
            
            # Fallback to domain itself
            if not kdc_servers:
                kdc_servers.append(domain)
            
            return kdc_servers
            
        except ImportError:
            # DNS resolution not available
            return [domain]
        except Exception as e:
            logging.getLogger(__name__).warning(f"KDC discovery failed for {domain}: {e}")
            return [domain]

# Example usage
async def demonstrate_kerberos_validation():
    """Demonstrate Kerberos username validation"""
    
    config = KerberosConfig(
        kdc_host='dc01.corporate.com',
        realm='CORPORATE.COM',
        timeout=5
    )
    
    validator = KerberosUsernameValidator(config)
    
    # Test usernames
    test_usernames = ['administrator', 'john.doe', 'nonexistent.user', 'service.account']
    
    print("🔐 Kerberos Username Validation Demo")
    print("=" * 50)
    
    for username in test_usernames:
        result = await validator.validate_username(username)
        
        status = "✅ EXISTS" if result.exists else "❌ NOT FOUND"
        confidence = f"{result.confidence:.0%}"
        
        print(f"{username:20} {status:15} Confidence: {confidence}")
        
        if result.preauth_required:
            print(f"{'':22} Pre-authentication required")
        if result.account_locked:
            print(f"{'':22} 🔒 Account locked")
        if result.password_expired:
            print(f"{'':22} ⚠️ Password expired")
        if result.error:
            print(f"{'':22} Error: {result.error}")

if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_kerberos_validation())
