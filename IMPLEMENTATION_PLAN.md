# WitsKit Detailed Implementation Plan

**Date:** 2025-07-28  
**Project:** WitsKit Strategic Roadmap Implementation  
**Roadmap Reference:** STRATEGIC_ROADMAP.md  

---

## 🔴 Phase 1: Security & Stability (Weeks 1-4)

### **Week 1: Critical Security Vulnerabilities**

#### **Day 1-2: Security Assessment & Planning**

**Task 1.1: Credential Management System**
```bash
# Create secure configuration module
touch witskit/config.py
touch witskit/security/__init__.py
touch witskit/security/credentials.py
touch witskit/security/encryption.py
```

**Implementation:**
```python
# witskit/config.py
from pydantic import BaseSettings, Field
from typing import Optional
import os

class WitsConfig(BaseSettings):
    # Database Configuration
    database_url: str = Field(..., env="WITS_DATABASE_URL")
    database_pool_size: int = Field(20, env="WITS_DB_POOL_SIZE")
    database_timeout: int = Field(30, env="WITS_DB_TIMEOUT")
    
    # Security Configuration  
    api_key: Optional[str] = Field(None, env="WITS_API_KEY")
    jwt_secret: Optional[str] = Field(None, env="WITS_JWT_SECRET")
    encryption_key: Optional[str] = Field(None, env="WITS_ENCRYPTION_KEY")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="WITS_LOG_LEVEL")
    log_format: str = Field("json", env="WITS_LOG_FORMAT")
    
    # Transport Configuration
    tcp_timeout: int = Field(30, env="WITS_TCP_TIMEOUT")
    tcp_retry_attempts: int = Field(3, env="WITS_TCP_RETRY_ATTEMPTS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False

# Global config instance
config = WitsConfig()
```

**Task 1.2: Secure Database Connection**
```python
# witskit/storage/secure_connection.py
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus
import os

class SecureDatabaseManager:
    def __init__(self, config: WitsConfig):
        self.config = config
        self._engine: Optional[Engine] = None
    
    def get_engine(self) -> Engine:
        if not self._engine:
            # Never log the actual URL
            sanitized_url = self._sanitize_url(self.config.database_url)
            logger.info(f"Connecting to database: {sanitized_url}")
            
            self._engine = create_engine(
                self.config.database_url,
                pool_size=self.config.database_pool_size,
                pool_timeout=self.config.database_timeout,
                echo=False,  # Never echo SQL in production
            )
        return self._engine
    
    def _sanitize_url(self, url: str) -> str:
        """Remove credentials from URL for logging"""
        # Implementation to mask credentials
        pass
```

#### **Day 3-4: Input Validation & Sanitization**

**Task 1.3: Secure WITS Frame Validation**
```python
# witskit/security/validation.py
import re
from typing import List, Optional
from pydantic import validator

class SecureWITSFrame(WITSFrame):
    """Security-hardened WITS frame with input validation"""
    
    @validator("raw_data")
    @classmethod
    def validate_secure_input(cls, v: str) -> str:
        # 1. Length validation
        if len(v) > 10000:  # Max frame size
            raise ValueError("WITS frame exceeds maximum size")
        
        # 2. Character validation
        if not re.match(r'^[a-zA-Z0-9\n\r&!.\-+\s]*$', v):
            raise ValueError("WITS frame contains invalid characters")
        
        # 3. Structure validation
        lines = v.strip().split('\n')
        if not (lines[0].strip().startswith('&&') and 
                lines[-1].strip().startswith('!!')):
            raise ValueError("Invalid WITS frame structure")
        
        # 4. Injection prevention
        for line in lines[1:-1]:  # Data lines only
            if not re.match(r'^\d{4}[0-9.\-+\s]*$', line.strip()):
                raise ValueError(f"Invalid data line format: {line}")
        
        return v

class SecureWITSDecoder(WITSDecoder):
    """Security-enhanced WITS decoder"""
    
    def decode_frame(self, raw_frame: str, source: Optional[str] = None) -> DecodedFrame:
        # Use secure frame validation
        secure_frame = SecureWITSFrame(raw_data=raw_frame, source=source)
        return super().decode_frame(raw_frame, source)
    
    def _validate_symbol_code(self, code: str) -> bool:
        """Validate symbol code against injection attacks"""
        return (
            len(code) == 4 and 
            code.isdigit() and
            code in WITS_SYMBOLS
        )
```

#### **Day 5: Secure Logging Implementation**

**Task 1.4: Security-Aware Logging**
```python
# witskit/security/logging.py
import json
import logging
from typing import Any, Dict
from loguru import logger
import structlog

class SecureLogger:
    """Security-aware logging that prevents credential leakage"""
    
    SENSITIVE_FIELDS = {
        'password', 'passwd', 'pwd', 'secret', 'key', 'token', 
        'auth', 'credential', 'private', 'api_key'
    }
    
    def __init__(self):
        self.logger = structlog.get_logger()
    
    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive information from log data"""
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in self.SENSITIVE_FIELDS):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, str) and any(sensitive in value.lower() 
                                              for sensitive in ['password=', 'key=']):
                sanitized[key] = self._mask_credentials(value)
            else:
                sanitized[key] = value
        return sanitized
    
    def _mask_credentials(self, text: str) -> str:
        """Mask credentials in connection strings"""
        patterns = [
            r'(password=)[^;]+',
            r'(key=)[^;]+', 
            r'(secret=)[^;]+',
        ]
        masked = text
        for pattern in patterns:
            masked = re.sub(pattern, r'\1***', masked, flags=re.IGNORECASE)
        return masked
    
    def info(self, message: str, **kwargs):
        sanitized_kwargs = self.sanitize_data(kwargs)
        self.logger.info(message, **sanitized_kwargs)
    
    def error(self, message: str, **kwargs):
        sanitized_kwargs = self.sanitize_data(kwargs)
        self.logger.error(message, **sanitized_kwargs)

# Global secure logger
secure_logger = SecureLogger()
```

### **Week 2: Authentication & Authorization**

#### **Day 6-7: Authentication Framework**

**Task 2.1: JWT-Based Authentication**
```python
# witskit/security/auth.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str] = None
    roles: List[str] = []
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuthManager:
    def __init__(self, jwt_secret: str):
        self.jwt_secret = jwt_secret
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def create_access_token(self, user: User) -> str:
        to_encode = {
            "sub": user.username,
            "roles": user.roles,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        }
        return jwt.encode(to_encode, self.jwt_secret, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
```

**Task 2.2: Role-Based Access Control**
```python
# witskit/security/rbac.py
from enum import Enum
from typing import List, Set
from functools import wraps

class Permission(str, Enum):
    READ_DATA = "data:read"
    WRITE_DATA = "data:write"
    ADMIN_USERS = "users:admin"
    MANAGE_CONNECTIONS = "connections:manage"
    VIEW_ANALYTICS = "analytics:view"

class Role(str, Enum):
    VIEWER = "viewer"
    OPERATOR = "operator" 
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

ROLE_PERMISSIONS = {
    Role.VIEWER: {Permission.READ_DATA, Permission.VIEW_ANALYTICS},
    Role.OPERATOR: {Permission.READ_DATA, Permission.WRITE_DATA, Permission.VIEW_ANALYTICS},
    Role.ADMIN: {Permission.READ_DATA, Permission.WRITE_DATA, Permission.MANAGE_CONNECTIONS, Permission.VIEW_ANALYTICS},
    Role.SUPER_ADMIN: set(Permission),  # All permissions
}

def require_permission(required_permission: Permission):
    """Decorator to enforce permissions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract user from context
            user_roles = get_current_user_roles()  # Implementation needed
            user_permissions = set()
            
            for role in user_roles:
                user_permissions.update(ROLE_PERMISSIONS.get(Role(role), set()))
            
            if required_permission not in user_permissions:
                raise PermissionError(f"Permission {required_permission} required")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

#### **Day 8-9: Secure Transport Layer**

**Task 2.3: TLS/SSL Support**
```python
# witskit/transport/secure_tcp_reader.py
import ssl
import socket
from typing import Optional, Generator

class SecureTCPReader(BaseTransport):
    def __init__(
        self,
        host: str,
        port: int,
        use_tls: bool = True,
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
        ca_file: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.socket: Optional[socket.socket] = None
    
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        if self.ca_file:
            context.load_verify_locations(self.ca_file)
        
        if self.cert_file and self.key_file:
            context.load_cert_chain(self.cert_file, self.key_file)
        
        # Security hardening
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
        
        return context
    
    def stream(self) -> Generator[str, None, None]:
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if self.use_tls:
                # Wrap with SSL
                ssl_context = self._create_ssl_context()
                self.socket = ssl_context.wrap_socket(
                    self.socket, 
                    server_hostname=self.host
                )
            
            # Connect
            self.socket.connect((self.host, self.port))
            secure_logger.info("Secure connection established", 
                             host=self.host, port=self.port, tls=self.use_tls)
            
            # Stream data (implementation continues...)
            buffer = ""
            while True:
                try:
                    chunk = self.socket.recv(1024).decode('utf-8', errors='ignore')
                    if not chunk:
                        break
                    
                    buffer += chunk
                    # Process frames...
                    
                except Exception as e:
                    secure_logger.error("Stream error", error=str(e))
                    break
                    
        finally:
            if self.socket:
                self.socket.close()
```

#### **Day 10: Security Testing Framework**

**Task 2.4: Security Test Suite**
```python
# tests/security/test_auth.py
import pytest
from witskit.security.auth import AuthManager
from witskit.security.rbac import require_permission, Permission

class TestAuthentication:
    def setup_method(self):
        self.auth_manager = AuthManager("test-secret-key")
    
    def test_password_hashing(self):
        password = "secure_password_123"
        hashed = self.auth_manager.hash_password(password)
        
        assert hashed != password
        assert self.auth_manager.verify_password(password, hashed)
        assert not self.auth_manager.verify_password("wrong_password", hashed)
    
    def test_jwt_token_creation_verification(self):
        user = User(username="testuser", roles=["operator"])
        token = self.auth_manager.create_access_token(user)
        
        payload = self.auth_manager.verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert "operator" in payload["roles"]
    
    def test_invalid_token_rejection(self):
        invalid_token = "invalid.jwt.token"
        payload = self.auth_manager.verify_token(invalid_token)
        assert payload is None

# tests/security/test_input_validation.py
class TestInputValidation:
    def test_valid_wits_frame_acceptance(self):
        valid_frame = """&&
01083650.40
011323.38
!!"""
        frame = SecureWITSFrame(raw_data=valid_frame)
        assert frame.raw_data == valid_frame
    
    def test_injection_attack_prevention(self):
        malicious_frame = """&&
0108'; DROP TABLE wits_data; --
011323.38
!!"""
        with pytest.raises(ValueError, match="Invalid data line format"):
            SecureWITSFrame(raw_data=malicious_frame)
    
    def test_oversized_frame_rejection(self):
        oversized_frame = "&&\n" + "0108123.45\n" * 1000 + "!!"
        with pytest.raises(ValueError, match="exceeds maximum size"):
            SecureWITSFrame(raw_data=oversized_frame)
```

### **Week 3: Transport Layer Fixes**

#### **Day 11-12: TCP Testing Overhaul**

**Task 3.1: Async Test Infrastructure**
```python
# tests/transport/test_tcp_async.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from witskit.transport.async_tcp_reader import AsyncTCPReader

class MockTCPServer:
    """Mock TCP server for testing"""
    
    def __init__(self, responses: List[str]):
        self.responses = responses
        self.response_index = 0
    
    async def handle_client(self, reader, writer):
        # Send mock WITS frames
        for response in self.responses:
            writer.write(response.encode())
            await writer.drain()
            await asyncio.sleep(0.1)  # Simulate delay
        
        writer.close()
        await writer.wait_closed()
    
    async def start_server(self, host: str = 'localhost', port: int = 0):
        self.server = await asyncio.start_server(
            self.handle_client, host, port
        )
        return self.server.sockets[0].getsockname()[1]  # Return actual port

@pytest.mark.asyncio
class TestAsyncTCPReader:
    async def test_connection_lifecycle(self):
        # Test data
        test_frames = [
            "&&\n01083650.40\n011323.38\n!!",
            "&&\n01083651.20\n011324.15\n!!"
        ]
        
        # Start mock server
        mock_server = MockTCPServer(test_frames)
        port = await mock_server.start_server()
        
        try:
            # Test connection
            reader = AsyncTCPReader("localhost", port)
            frames = []
            
            async for frame in reader.stream():
                frames.append(frame)
                if len(frames) >= 2:
                    break
            
            assert len(frames) == 2
            assert "01083650.40" in frames[0]
            assert "01083651.20" in frames[1]
            
        finally:
            mock_server.server.close()
            await mock_server.server.wait_closed()
    
    async def test_connection_failure_handling(self):
        # Test connection to non-existent server
        reader = AsyncTCPReader("localhost", 99999)
        
        with pytest.raises(ConnectionError):
            async for frame in reader.stream():
                pass
    
    async def test_retry_mechanism(self):
        # Test retry logic with failing connections
        retry_policy = RetryPolicy(max_attempts=3, backoff_factor=0.1)
        reader = AsyncTCPReader("localhost", 99999, retry_policy=retry_policy)
        
        attempt_count = 0
        try:
            async for frame in reader.stream():
                pass
        except ConnectionError:
            # Verify retry attempts were made
            assert reader.connection_attempts == 3
```

**Task 3.2: Circuit Breaker Implementation**
```python
# witskit/transport/resilience.py
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            datetime.utcnow() - self.last_failure_time > 
            timedelta(seconds=self.recovery_timeout)
        )

class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 1.0,
        max_backoff: float = 60.0
    ):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff
    
    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_attempts - 1:  # Not the last attempt
                    delay = min(
                        self.backoff_factor * (2 ** attempt),
                        self.max_backoff
                    )
                    await asyncio.sleep(delay)
        
        raise last_exception
```

#### **Day 13-14: Error Handling & Monitoring**

**Task 3.3: Comprehensive Error Handling**
```python
# witskit/transport/error_handling.py
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"  
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    CONNECTION = "connection"
    PARSING = "parsing"
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    SYSTEM = "system"

@dataclass
class WitsError:
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Dict[str, Any]
    timestamp: datetime = None
    source: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

class ErrorHandler:
    def __init__(self):
        self.error_callbacks: Dict[ErrorCategory, List[Callable]] = {}
        self.error_counts: Dict[ErrorCategory, int] = {}
    
    def register_callback(self, category: ErrorCategory, callback: Callable):
        if category not in self.error_callbacks:
            self.error_callbacks[category] = []
        self.error_callbacks[category].append(callback)
    
    async def handle_error(self, error: WitsError):
        # Log error
        secure_logger.error(
            "WitsKit error occurred",
            category=error.category.value,
            severity=error.severity.value,
            message=error.message,
            details=error.details,
            source=error.source
        )
        
        # Update error counts
        self.error_counts[error.category] = self.error_counts.get(error.category, 0) + 1
        
        # Execute callbacks
        if error.category in self.error_callbacks:
            for callback in self.error_callbacks[error.category]:
                try:
                    await callback(error)
                except Exception as e:
                    secure_logger.error("Error callback failed", callback_error=str(e))
    
    def get_error_stats(self) -> Dict[str, int]:
        return dict(self.error_counts)

# Global error handler
error_handler = ErrorHandler()
```

### **Week 4: Monitoring & Observability**

#### **Day 15-16: Metrics & Monitoring**

**Task 4.1: Prometheus Metrics**
```python
# witskit/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info
from typing import Dict, Any
import time
from functools import wraps

class WitsMetrics:
    def __init__(self):
        # Connection metrics
        self.connections_total = Counter(
            'wits_connections_total',
            'Total number of connections attempted',
            ['transport_type', 'status']
        )
        
        # Processing metrics
        self.frames_processed_total = Counter(
            'wits_frames_processed_total',
            'Total number of WITS frames processed',
            ['source', 'status']
        )
        
        self.frame_processing_duration = Histogram(
            'wits_frame_processing_seconds',
            'Time spent processing WITS frames',
            ['operation']
        )
        
        # System metrics
        self.active_connections = Gauge(
            'wits_active_connections',
            'Number of active connections',
            ['transport_type']
        )
        
        self.error_rate = Counter(
            'wits_errors_total',
            'Total number of errors',
            ['error_type', 'severity']
        )
        
        # Data quality metrics
        self.data_quality_score = Gauge(
            'wits_data_quality_score',
            'Data quality score (0-1)',
            ['source']
        )
        
        # System info
        self.system_info = Info(
            'wits_system_info',
            'System information'
        )
    
    def record_connection_attempt(self, transport_type: str, success: bool):
        status = 'success' if success else 'failure'
        self.connections_total.labels(
            transport_type=transport_type,
            status=status
        ).inc()
    
    def record_frame_processed(self, source: str, success: bool):
        status = 'success' if success else 'failure'
        self.frames_processed_total.labels(
            source=source,
            status=status
        ).inc()
    
    def record_error(self, error_type: str, severity: str):
        self.error_rate.labels(
            error_type=error_type,
            severity=severity
        ).inc()

# Global metrics instance
metrics = WitsMetrics()

def track_processing_time(operation: str):
    """Decorator to track processing time"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                metrics.frame_processing_duration.labels(
                    operation=operation
                ).observe(duration)
        return wrapper
    return decorator
```

**Task 4.2: Health Checks**
```python
# witskit/monitoring/health.py
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: Optional[str] = None
    details: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.details is None:
            self.details = {}

class HealthMonitor:
    def __init__(self):
        self.checks: Dict[str, Callable] = {}
    
    def register_check(self, name: str, check_func: Callable):
        self.checks[name] = check_func
    
    async def run_all_checks(self) -> List[HealthCheck]:
        results = []
        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                if isinstance(result, HealthCheck):
                    results.append(result)
                else:
                    # Assume boolean return
                    status = HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY
                    results.append(HealthCheck(name=name, status=status))
            except Exception as e:
                results.append(HealthCheck(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Check failed: {str(e)}"
                ))
        return results
    
    async def get_overall_health(self) -> HealthCheck:
        checks = await self.run_all_checks()
        
        # Determine overall status
        if all(check.status == HealthStatus.HEALTHY for check in checks):
            overall_status = HealthStatus.HEALTHY
        elif any(check.status == HealthStatus.UNHEALTHY for check in checks):
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.DEGRADED
        
        return HealthCheck(
            name="overall",
            status=overall_status,
            details={
                "individual_checks": {
                    check.name: check.status.value for check in checks
                }
            }
        )

# Built-in health checks
async def database_health_check() -> HealthCheck:
    """Check database connectivity"""
    try:
        # Test database connection
        engine = get_database_engine()
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        
        return HealthCheck(
            name="database",
            status=HealthStatus.HEALTHY,
            message="Database connection successful"
        )
    except Exception as e:
        return HealthCheck(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message=f"Database connection failed: {str(e)}"
        )

async def memory_health_check() -> HealthCheck:
    """Check memory usage"""
    import psutil
    
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    
    if memory_percent > 90:
        status = HealthStatus.UNHEALTHY
        message = f"Memory usage critical: {memory_percent}%"
    elif memory_percent > 75:
        status = HealthStatus.DEGRADED
        message = f"Memory usage high: {memory_percent}%"
    else:
        status = HealthStatus.HEALTHY
        message = f"Memory usage normal: {memory_percent}%"
    
    return HealthCheck(
        name="memory",
        status=status,
        message=message,
        details={"memory_percent": memory_percent}
    )

# Global health monitor
health_monitor = HealthMonitor()
health_monitor.register_check("database", database_health_check)
health_monitor.register_check("memory", memory_health_check)
```

#### **Day 17-18: Environment & Deployment Configuration**

**Task 4.3: Environment Configuration**
```bash
# Create environment files
cat > .env.example << 'EOF'
# Database Configuration
WITS_DATABASE_URL=postgresql://user:password@localhost:5432/witsdb
WITS_DB_POOL_SIZE=20
WITS_DB_TIMEOUT=30

# Security Configuration
WITS_API_KEY=your-api-key-here
WITS_JWT_SECRET=your-jwt-secret-here
WITS_ENCRYPTION_KEY=your-encryption-key-here

# Logging Configuration
WITS_LOG_LEVEL=INFO
WITS_LOG_FORMAT=json

# Transport Configuration
WITS_TCP_TIMEOUT=30
WITS_TCP_RETRY_ATTEMPTS=3

# Monitoring Configuration
WITS_METRICS_ENABLED=true
WITS_METRICS_PORT=9090
WITS_HEALTH_CHECK_PORT=8080
EOF

# Production environment template
cat > .env.production << 'EOF'
# Production Database - Use environment-specific values
WITS_DATABASE_URL=${DATABASE_URL}
WITS_DB_POOL_SIZE=50
WITS_DB_TIMEOUT=60

# Security - Use secure values from secret management
WITS_API_KEY=${API_KEY}
WITS_JWT_SECRET=${JWT_SECRET}
WITS_ENCRYPTION_KEY=${ENCRYPTION_KEY}

# Production Logging
WITS_LOG_LEVEL=WARNING
WITS_LOG_FORMAT=json

# Production Transport Settings
WITS_TCP_TIMEOUT=60
WITS_TCP_RETRY_ATTEMPTS=5

# Monitoring
WITS_METRICS_ENABLED=true
WITS_METRICS_PORT=9090
WITS_HEALTH_CHECK_PORT=8080
EOF
```

**Task 4.4: Docker Production Setup**
```docker
# Dockerfile.production
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r witskit && useradd -r -g witskit witskit

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY --chown=witskit:witskit . /app
WORKDIR /app

# Install application
RUN pip install -e .

# Switch to non-root user
USER witskit

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Default command
CMD ["witskit", "stream", "--config", "/app/config/production.yaml"]

# Expose ports
EXPOSE 8080 9090
```

---

## 📋 Implementation Checklist

### **Week 1: Critical Security**
- [ ] Create secure configuration system (`config.py`)
- [ ] Implement credential management (no hardcoded secrets)
- [ ] Add input validation for WITS frames
- [ ] Create secure logging system (redact sensitive data)
- [ ] Security test suite

### **Week 2: Authentication & Authorization**  
- [ ] JWT-based authentication system
- [ ] Role-based access control (RBAC)
- [ ] TLS/SSL support for transport layer
- [ ] Security testing framework
- [ ] Penetration testing preparation

### **Week 3: Transport Layer Fixes**
- [ ] Fix TCP transport testing with proper async mocks
- [ ] Implement circuit breaker pattern
- [ ] Add retry mechanisms with exponential backoff
- [ ] Comprehensive error handling system
- [ ] Connection lifecycle management

### **Week 4: Monitoring & Observability**
- [ ] Prometheus metrics collection
- [ ] Health check endpoints
- [ ] Structured logging with correlation IDs
- [ ] Error tracking and alerting
- [ ] Docker production configuration

### **Success Criteria for Phase 1**
- ✅ Zero critical security vulnerabilities
- ✅ All tests passing (including TCP transport)
- ✅ Environment-based configuration
- ✅ Production-ready Docker images
- ✅ Monitoring and health checks operational

---

*This implementation plan provides step-by-step technical details for Phase 1. Each task includes code examples, configuration templates, and specific deliverables to ensure successful completion.*