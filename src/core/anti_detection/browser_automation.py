
"""
Advanced Stealth Browser Automation with Playwright
"""

import asyncio
import random
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

@dataclass
class BrowserProfile:
    """Complete browser profile for stealth automation"""
    user_agent: str
    viewport: Dict[str, int]
    timezone_id: str
    locale: str
    geolocation: Dict[str, float]
    permissions: List[str]
    extra_headers: Dict[str, str]
    storage_state: Optional[Dict] = None

class StealthBrowser:
    """Advanced stealth browser automation with anti-detection features"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.contexts = []
        self.browser_profiles = []
        self.logger = logging.getLogger(__name__)
        
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available. Browser automation disabled.")
    
    async def initialize(self):
        """Initialize the browser automation system"""
        
        if not PLAYWRIGHT_AVAILABLE:
            return False
        
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with stealth options
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-blink-features=AutomationControlled',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                ]
            )
            
            self.logger.info("Stealth browser initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Browser initialization failed: {e}")
            return False
    
    async def create_stealth_context(self, fingerprint: Dict) -> BrowserContext:
        """Create a stealth browser context with advanced anti-detection"""
        
        if not self.browser:
            raise RuntimeError("Browser not initialized")
        
        context = await self.browser.new_context(
            user_agent=fingerprint.get('user_agent'),
            viewport=fingerprint.get('viewport'),
            locale=fingerprint.get('locale', 'en-US'),
            timezone_id=fingerprint.get('timezone_id', 'America/New_York'),
            geolocation=fingerprint.get('geolocation'),
            permissions=['geolocation'],
            extra_http_headers=fingerprint.get('extra_headers', {})
        )
        
        # Apply advanced stealth injections
        await self._inject_stealth_scripts(context, fingerprint)
        
        self.contexts.append(context)
        return context
    
    async def _inject_stealth_scripts(self, context: BrowserContext, fingerprint: Dict):
        """Inject advanced stealth scripts to avoid detection"""
        
        stealth_script = """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Override plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Override languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Mock Chrome runtime
        window.chrome = {
            runtime: {},
            // ... other mocked properties
        };
        
        // Override WebGL vendor and renderer
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return '%WEBGL_VENDOR%';
            }
            if (parameter === 37446) {
                return '%WEBGL_RENDERER%';
            }
            return getParameter.call(this, parameter);
        };
        
        // Mock screen resolution
        Object.defineProperty(screen, 'width', { get: () => %SCREEN_WIDTH% });
        Object.defineProperty(screen, 'height', { get: () => %SCREEN_HEIGHT% });
        Object.defineProperty(screen, 'availWidth', { get: () => %SCREEN_WIDTH% });
        Object.defineProperty(screen, 'availHeight', { get: () => %SCREEN_HEIGHT% });
        Object.defineProperty(screen, 'colorDepth', { get: () => %COLOR_DEPTH% });
        Object.defineProperty(screen, 'pixelDepth', { get: () => %COLOR_DEPTH% });
        
        // Mock hardware concurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => %HARDWARE_CONCURRENCY%,
        });
        
        // Mock device memory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => %DEVICE_MEMORY%,
        });
        
        // Mock battery API
        if ('getBattery' in navigator) {
            navigator.getBattery = () => Promise.resolve({
                charging: true,
                chargingTime: 0,
                dischargingTime: Infinity,
                level: 0.85,
            });
        }
        
        console.log('Stealth injections applied successfully');
        """
        
        # Replace placeholders with actual fingerprint data
        stealth_script = stealth_script.replace('%WEBGL_VENDOR%', fingerprint.get('webgl_vendor', 'Google Inc.'))
        stealth_script = stealth_script.replace('%WEBGL_RENDERER%', fingerprint.get('webgl_renderer', 'ANGLE'))
        stealth_script = stealth_script.replace('%SCREEN_WIDTH%', str(fingerprint.get('screen_width', 1920)))
        stealth_script = stealth_script.replace('%SCREEN_HEIGHT%', str(fingerprint.get('screen_height', 1080)))
        stealth_script = stealth_script.replace('%COLOR_DEPTH%', str(fingerprint.get('color_depth', 24)))
        stealth_script = stealth_script.replace('%HARDWARE_CONCURRENCY%', str(fingerprint.get('hardware_concurrency', 8)))
        stealth_script = stealth_script.replace('%DEVICE_MEMORY%', str(fingerprint.get('device_memory', 8)))
        
        await context.add_init_script(stealth_script)
    
    async def navigate_with_stealth(self, page: Page, url: str, human_behavior: Dict = None):
        """Navigate to URL with human-like behavior simulation"""
        
        behavior = human_behavior or self._generate_human_behavior()
        
        # Simulate human delay before navigation
        await asyncio.sleep(behavior.get('pre_navigation_delay', random.uniform(1.0, 3.0)))
        
        # Navigate to page
        await page.goto(url, wait_until='networkidle')
        
        # Simulate post-navigation behavior
        await self._simulate_human_behavior(page, behavior)
    
    async def _simulate_human_behavior(self, page: Page, behavior: Dict):
        """Simulate realistic human behavior patterns"""
        
        # Random scrolling
        scroll_steps = random.randint(2, 5)
        for _ in range(scroll_steps):
            scroll_amount = random.randint(100, 500)
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Random mouse movements
        viewport = page.viewport_size
        if viewport:
            moves = random.randint(3, 8)
            start_x, start_y = random.randint(100, viewport['width']-100), random.randint(100, viewport['height']-100)
            
            for i in range(moves):
                x = start_x + random.randint(-200, 200)
                y = start_y + random.randint(-100, 100)
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # Random pauses
        await asyncio.sleep(behavior.get('reading_delay', random.uniform(2.0, 5.0)))
    
    def _generate_human_behavior(self) -> Dict:
        """Generate realistic human behavior parameters"""
        
        return {
            'pre_navigation_delay': random.uniform(1.0, 4.0),
            'reading_delay': random.uniform(2.0, 8.0),
            'scroll_intensity': random.uniform(0.5, 1.5),
            'mouse_movement_variance': random.uniform(10, 30),
            'typing_speed': random.uniform(0.1, 0.3)
        }
    
    async def solve_captcha_in_browser(self, page: Page, captcha_selector: str = None) -> Dict:
        """Solve captchas directly in the browser"""
        
        try:
            # Check for different types of captchas
            captcha_type = await self._detect_captcha_type(page)
            
            if captcha_type == 'image_captcha':
                return await self._solve_image_captcha(page, captcha_selector)
            elif captcha_type == 'recaptcha':
                return await self._solve_recaptcha(page)
            elif captcha_type == 'hcaptcha':
                return await self._solve_hcaptcha(page)
            else:
                return {'solved': False, 'error': f'Unsupported captcha type: {captcha_type}'}
                
        except Exception as e:
            self.logger.error(f"Captcha solving failed: {e}")
            return {'solved': False, 'error': str(e)}
    
    async def _detect_captcha_type(self, page: Page) -> str:
        """Detect the type of captcha present on the page"""
        
        # Check for reCAPTCHA
        recaptcha_frames = await page.query_selector_all('iframe[src*="google.com/recaptcha"]')
        if recaptcha_frames:
            return 'recaptcha'
        
        # Check for hCaptcha
        hcaptcha_frames = await page.query_selector_all('iframe[src*="hcaptcha.com"]')
        if hcaptcha_frames:
            return 'hcaptcha'
        
        # Check for image captchas
        image_captchas = await page.query_selector_all('img[src*="captcha"], input[type="image"]')
        if image_captchas:
            return 'image_captcha'
        
        # Check for text-based captchas
        captcha_inputs = await page.query_selector_all('input[name*="captcha"], input[type="text"][class*="captcha"]')
        if captcha_inputs:
            return 'text_captcha'
        
        return 'unknown'
    
    async def _solve_image_captcha(self, page: Page, selector: str = None) -> Dict:
        """Solve image-based captchas in the browser"""
        
        try:
            # Find captcha image
            if selector:
                captcha_image = await page.query_selector(selector)
            else:
                captcha_image = await page.query_selector('img[src*="captcha"]')
            
            if not captcha_image:
                return {'solved': False, 'error': 'Captcha image not found'}
            
            # Take screenshot of captcha
            screenshot = await captcha_image.screenshot()
            
            # Use our AI captcha solver
            from .captcha_solver import AICaptchaSolver
            solver = AICaptchaSolver()
            result = await solver.solve_captcha(screenshot)
            
            if result['solved']:
                # Find input field and enter solution
                input_field = await page.query_selector('input[name*="captcha"], input[type="text"]')
                if input_field:
                    await input_field.fill(result['text'])
                    return {'solved': True, 'text': result['text'], 'confidence': result['confidence']}
            
            return {'solved': False, 'error': 'Could not solve captcha'}
            
        except Exception as e:
            return {'solved': False, 'error': str(e)}
    
    async def _solve_recaptcha(self, page: Page) -> Dict:
        """Solve reCAPTCHA challenges"""
        
        # This would implement advanced reCAPTCHA solving techniques
        # Including audio challenges, image recognition, etc.
        
        return {
            'solved': False,
            'error': 'reCAPTCHA solving requires advanced implementation',
            'note': 'Consider using recaptcha-solving services for production'
        }
    
    async def _solve_hcaptcha(self, page: Page) -> Dict:
        """Solve hCaptcha challenges"""
        
        # Similar to reCAPTCHA, requires advanced implementation
        
        return {
            'solved': False,
            'error': 'hCaptcha solving requires advanced implementation'
        }
    
    async def close(self):
        """Cleanup browser resources"""
        
        for context in self.contexts:
            await context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self.logger.info("Stealth browser closed")
