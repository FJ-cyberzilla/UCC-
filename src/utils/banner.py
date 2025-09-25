"""
ASCII art banners and displays
"""

from utils.colors import Colors

def show_banner():
    """Display main banner"""
    banner = f"""
{Colors.BRIGHT_CYAN}
    ╔═╗┬ ┬┌─┐┌┬┐┌─┐┬─┐┌─┐  ╔═╗┌─┐┌─┐┌┬┐┌─┐┬─┐  ╔═╗┌─┐┌─┐┌┬┐┌─┐┬─┐
    ║  ├─┤├┤  │ ├┤ ├┬┘└─┐  ║ ║├┤ ├─┤ │ ├┤ ├┬┘  ║  ├─┤└─┐ │ ├┤ ├┬┘
    ╚═╝┴ ┴└─┘ ┴ └─┘┴└─└─┘  ╚═╝└─┘┴ ┴ ┴ └─┘┴└─  ╚═╝┴ ┴└─┘ ┴ └─┘┴└─
    
    {Colors.BRIGHT_MAGENTA}🎯 50+ Platforms • 🛡️ Anti-Detection • ⚡ Lightning Fast • 🎨 Beautiful CLI{Colors.ENDC}
    
    {Colors.BRIGHT_YELLOW}>>> The Ultimate Username Availability Checker <<<{Colors.ENDC}
    
{Colors.BRIGHT_GREEN}
    🔥 Featured Platforms:{Colors.ENDC}
    {Colors.CYAN}• Signal • LinkedIn • Telegram • Bluesky • Facebook • Reddit • Twitch{Colors.ENDC}
    {Colors.CYAN}• Discord • Instagram • TikTok • WhatsApp • Roblox • Teams • Viber{Colors.ENDC}
    {Colors.CYAN}• Pinterest • Iranian Apps • AI Platforms • Gaming • Tech • Creative{Colors.ENDC}
    
{Colors.BRIGHT_RED}    ⚠️  Use responsibly and respect platform Terms of Service!{Colors.ENDC}
"""
    print(banner)

def show_platform_banner(platforms):
    """Display platform selection banner"""
    print(f"\n{Colors.BRIGHT_GREEN}🎯 Selected Platforms ({len(platforms)}):{Colors.ENDC}")
    for i, platform in enumerate(platforms, 1):
        print(f"    {Colors.CYAN}{i:2d}. {platform}{Colors.ENDC}")

def show_results_banner(username):
    """Display results banner"""
    print(f"\n{Colors.BRIGHT_GREEN}📊 Results for: {Colors.BRIGHT_CYAN}{username}{Colors.ENDC}")
    print(f"{Colors.GRAY}{'='*60}{Colors.ENDC}")
