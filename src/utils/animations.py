"""
Loading animations and progress indicators
"""

import asyncio
import sys
import time
from itertools import cycle
from utils.colors import Colors

class LoadingAnimation:
    def __init__(self, message="Loading..."):
        self.message = message
        self.spinner = cycle(['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'])
        self.running = False
        
    async def __aenter__(self):
        self.running = True
        asyncio.create_task(self.animate())
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
        
    async def animate(self):
        while self.running:
            for frame in self.spinner:
                if not self.running:
                    break
                sys.stdout.write(f'\r{Colors.YELLOW}{frame}{Colors.ENDC} {self.message}')
                sys.stdout.flush()
                await asyncio.sleep(0.1)

def loading_animation(message):
    """Context manager for loading animation"""
    return LoadingAnimation(message)

class ProgressBar:
    def __init__(self, total, description="Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.width = 50
        
    def update(self, n=1):
        self.current += n
        self.display()
        
    def display(self):
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        percent_display = f"{percent:.1%}"
        
        sys.stdout.write(f'\r{Colors.CYAN}{self.description}:{Colors.ENDC} |{bar}| {percent_display} ({self.current}/{self.total})')
        sys.stdout.flush()
        
    def finish(self):
        sys.stdout.write('\n')
        sys.stdout.flush()
