# 🎯 UltimateUsernameChecker

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/FJ-Cyberzilla/UltimateUsernameChecker?style=social)](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/FJ-Cyberzilla/UltimateUsernameChecker)](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/graphs/commit-activity)

> **The most advanced username availability checker that dominates modern anti-bot systems**

UltimateUsernameChecker is a powerful, multi-strategy username availability checker that can bypass advanced anti-bot protections, solve CAPTCHAs, and check username availability across 50+ platforms with military-grade precision.

## 🚀 Features

### 🛡️ **Advanced Anti-Detection**
- **Browser Fingerprinting Evasion** - Dynamic fingerprint generation with realistic hardware/software combinations
- **Cloudflare Bypass** - Advanced TLS fingerprinting and JavaScript challenge solving
- **CAPTCHA Solving** - Automated OCR with image preprocessing and enhancement
- **Behavioral Simulation** - Human-like mouse movements and timing patterns

### 🎯 **Multiple Attack Strategies**
- **HTTP Basic** - Fast, lightweight HTTP requests for simple checks
- **HTTP Advanced** - Stealth HTTP with rotating fingerprints and headers
- **Browser Light** - Lightweight browser automation for JavaScript-heavy sites
- **Browser Advanced** - Full stealth browser with Playwright and undetected Chrome
- **API Based** - Official API integration for maximum accuracy

### 🌐 **Platform Support**
- **50+ Platforms** - Instagram, Twitter, GitHub, LinkedIn, Discord, TikTok, and more
- **Smart Strategy Selection** - Automatically chooses the best method for each platform
- **Real-time Adaptation** - Switches strategies if one method fails

### 📊 **Professional Features**
- **Batch Processing** - Check multiple usernames simultaneously
- **Detailed Reporting** - Comprehensive analysis with confidence scores
- **Performance Tracking** - Success rates, response times, and statistics
- **Export Options** - JSON, CSV, and formatted reports

## 🔧 Installation

### Quick Install
```bash
git clone https://github.com/FJ-Cyberzilla/UltimateUsernameChecker.git
cd UltimateUsernameChecker
chmod +x scripts/install.sh
./scripts/install.sh
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/FJ-Cyberzilla/UltimateUsernameChecker.git
cd UltimateUsernameChecker

# Install basic requirements
pip install -r requirements.txt

# Install advanced features (optional)
pip install -r requirements_advanced.txt

# Install Playwright browsers
playwright install chromium

# Setup Tesseract OCR (for CAPTCHA solving)
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from GitHub releases
```

### Termux Installation
```bash
# Special setup for Android Termux
chmod +x scripts/setup_termux.sh
./scripts/setup_termux.sh
```

## 🎮 Quick Start

### Interactive Mode
```bash
python main.py
```

### Command Line Usage
```bash
# Check single username
python main.py check johndoe --platforms instagram twitter github

# Batch check from file
python main.py batch usernames.txt --output results.json

# Advanced mode with all features
python main.py check johndoe --strategy advanced --solve-captcha --use-proxies
```

### Python API
```python
import asyncio
from src.core.checker_engine import UltimateChecker

async def main():
    config = {
        'strategy': 'advanced',
        'platforms': ['instagram', 'twitter', 'github'],
        'api_keys': {
            'discord': 'your_bot_token',
            'linkedin': 'your_access_token'
        }
    }
    
    async with UltimateChecker(config) as checker:
        results = await checker.check_username('johndoe')
        print(f"Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📋 Configuration

### Environment Setup
```bash
# Copy the example environment file
cp .env.example .env

# Edit with your API keys and settings
nano .env
```

### API Keys (Optional)
```env
# Discord Bot Token (for Discord checking)
DISCORD_BOT_TOKEN=your_discord_bot_token

# LinkedIn Access Token (for LinkedIn API)
LINKEDIN_ACCESS_TOKEN=your_linkedin_token

# Instagram Access Token (for Instagram API)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token

# Proxy Configuration
PROXY_LIST=http://proxy1:port,http://proxy2:port
```

### Advanced Configuration
```python
# config/settings.py
STRATEGY_CONFIG = {
    'http_basic': {
        'timeout': 10,
        'max_retries': 3,
        'rate_limit': 1.0
    },
    'browser_advanced': {
        'headless': True,
        'stealth_mode': True,
        'solve_captcha': True,
        'human_behavior': True
    }
}
```

## 🎯 Supported Platforms

### Social Media
- Instagram, Twitter/X, Facebook, TikTok, Snapchat, LinkedIn
- Discord, Telegram, WhatsApp Business, Pinterest
- YouTube, Twitch, Reddit, Clubhouse

### Technology
- GitHub, GitLab, BitBucket, Stack Overflow, Dev.to
- Docker Hub, npm, PyPI, Hacker News

### Creative
- Behance, Dribbble, DeviantArt, ArtStation, 500px
- Figma, Adobe Creative Cloud, Canva

### Professional
- AngelList, ProductHunt, Crunchbase, Glassdoor
- Medium, Substack, Hashnode, Ghost

### Gaming
- Steam, Epic Games, Battle.net, Origin, Uplay
- Xbox Live, PlayStation Network, Nintendo Account

*And 20+ more platforms...*

## 🔥 Advanced Usage

### Strategy Selection
```bash
# Use specific strategy
python main.py check username --strategy browser_advanced

# Fallback chain (try multiple strategies)
python main.py check username --strategies http_basic,http_advanced,browser_light
```

### Batch Processing
```bash
# Check multiple usernames
python main.py batch --file usernames.txt --platforms instagram,twitter --output report.json

# Parallel processing
python main.py batch --file usernames.txt --workers 5 --delay 2
```

### Proxy Usage
```bash
# Use proxy list
python main.py check username --proxy-file proxies.txt

# Single proxy
python main.py check username --proxy http://proxy:port
```

### CAPTCHA Solving
```bash
# Enable automatic CAPTCHA solving
python main.py check username --solve-captcha --ocr-engine tesseract

# Advanced OCR settings
python main.py check username --solve-captcha --ocr-config advanced
```

## 📊 Output Examples

### Console Output
```
🎯 ULTIMATE USERNAME CHECKER
═══════════════════════════════════════════════════════
Username: johndoe
Platforms: instagram, twitter, github, linkedin
Strategy: advanced

🔍 Checking Instagram... ✅ AVAILABLE (95% confidence)
🔍 Checking Twitter... ❌ TAKEN (98% confidence)
🔍 Checking GitHub... ✅ AVAILABLE (99% confidence)  
🔍 Checking LinkedIn... ✅ AVAILABLE (85% confidence)

📊 SUMMARY
Available: 3/4 platforms (75%)
Total time: 12.4 seconds
Success rate: 100%
```

### JSON Output
```json
{
  "username": "johndoe",
  "timestamp": "2024-01-15T10:30:00Z",
  "results": {
    "instagram": {
      "available": true,
      "confidence": 0.95,
      "method": "browser_advanced",
      "response_time": 2.1,
      "url": "https://instagram.com/johndoe"
    },
    "twitter": {
      "available": false,
      "confidence": 0.98,
      "method": "api",
      "response_time": 0.8,
      "url": "https://twitter.com/johndoe",
      "additional_info": {
        "followers": "1.2K",
        "verified": false
      }
    }
  },
  "summary": {
    "total_platforms": 4,
    "available_count": 3,
    "availability_rate": 0.75
  }
}
```

## ⚙️ Requirements

### System Requirements
- **Python 3.8+**
- **4GB RAM** (minimum), 8GB+ recommended for advanced features
- **Internet Connection** (obviously)
- **200MB Disk Space** for dependencies

### Dependencies
```txt
# Core
aiohttp>=3.8.0
asyncio-throttle>=1.0.2
rich>=13.0.0
click>=8.0.0

# Browser Automation
playwright>=1.35.0
selenium>=4.10.0
undetected-chromedriver>=3.5.0

# Anti-Detection
selenium-stealth>=1.0.6
fake-useragent>=1.4.0
requests-html>=0.10.0

# CAPTCHA Solving
opencv-python>=4.8.0
pytesseract>=0.3.10
Pillow>=10.0.0
numpy>=1.24.0

# Data Processing
beautifulsoup4>=4.12.0
lxml>=4.9.0
pandas>=2.0.0
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Platforms
1. Create a new platform file in `src/platforms/`
2. Inherit from `BasePlatform`
3. Implement the required methods
4. Add configuration to `config/platforms.py`
5. Submit a pull request

### Improving Anti-Detection
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-detection-bypass`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Bug Reports
Please use the [GitHub Issues](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/issues) to report bugs.

Include:
- Platform affected
- Strategy used
- Error message
- Steps to reproduce

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate research purposes only. Users are responsible for complying with:

- Platform Terms of Service
- Local and international laws
- Rate limiting and respectful usage
- Privacy and data protection regulations

The authors are not responsible for any misuse of this software.

## 🛡️ Ethical Usage

Please use this tool responsibly:

- ✅ **DO**: Check availability for your own usernames
- ✅ **DO**: Research username patterns for academic purposes  
- ✅ **DO**: Verify brand name availability across platforms
- ❌ **DON'T**: Harass or stalk individuals
- ❌ **DON'T**: Violate platform Terms of Service
- ❌ **DON'T**: Use for malicious purposes

## 🔧 Troubleshooting

### Common Issues

**1. Browser not launching**
```bash
# Install browsers manually
playwright install chromium
playwright install firefox
```

**2. CAPTCHA solving not working**
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr  # Ubuntu
brew install tesseract             # macOS
```

**3. Proxy connection errors**
```bash
# Test proxy connectivity
python -c "import requests; print(requests.get('https://httpbin.org/ip', proxies={'http': 'your_proxy'}).text)"
```

**4. Rate limiting issues**
```bash
# Increase delays between requests
python main.py check username --delay 5 --max-workers 1
```

### Performance Optimization

- Use `http_basic` strategy for simple platforms
- Enable proxy rotation for high-volume checking
- Adjust worker count based on your system specs
- Use SSD storage for better performance

## 📞 Support

### Documentation
- [Platform List](docs/PLATFORMS.md) - Complete list of supported platforms
- [Advanced Usage](docs/ADVANCED.md) - Advanced configuration and usage

### Contact
- **Author**: [FJ-Cyberzilla](https://github.com/FJ-Cyberzilla)
- **Email**: [cyberzilla.systems@gmail.com](mailto:cyberzilla.systems@gmail.com)
- **GitHub**: [https://github.com/FJ-Cyberzilla/UltimateUsernameChecker](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker)

### Community
- **Issues**: [GitHub Issues](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/discussions)
- **Pull Requests**: [Contributions Welcome](https://github.com/FJ-Cyberzilla/UltimateUsernameChecker/pulls)

---

<div align="center">

**⭐ Star this repository if you find it useful! ⭐**

Made with ⚡ by [FJ-Cyberzilla](https://github.com/FJ-Cyberzilla)

*"Dominating username availability checking since 2024"*

</div>
