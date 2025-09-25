#!/usr/bin/env python3
"""
Ultimate Username Checker - Web UI + CLI
"""

import click
import json
import sys
import os
from flask import Flask, render_template, request, jsonify, send_file
from threading import Thread
import webbrowser
import time

# Import our modules from the same package
from .checker import UsernameChecker
from .generator import UsernameGenerator
from .export import ExportManager

app = Flask(__name__)

class UltimateUsernameChecker:
    def __init__(self):
        self.checker = UsernameChecker()
        self.generator = UsernameGenerator()
        self.exporter = ExportManager()
    
    def check_username(self, username, platforms=None):
        return self.checker.check_username(username, platforms)
    
    def batch_check(self, usernames, platforms=None):
        return self.checker.batch_check(usernames, platforms)
    
    def generate_usernames(self, base_words, count=10, style="combined"):
        return self.generator.generate_usernames(base_words, count, style)
    
    def export_results(self, results, format_type, filename=None):
        return self.exporter.export(results, format_type, filename)

# Global instance
ultimate_checker = UltimateUsernameChecker()

# Web Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_username():
    data = request.json
    username = data.get('username', '').strip()
    platforms = data.get('platforms', None)
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        results = ultimate_checker.check_username(username, platforms)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch-check', methods=['POST'])
def batch_check():
    data = request.json
    usernames_text = data.get('usernames', '')
    platforms = data.get('platforms', None)
    
    if not usernames_text:
        return jsonify({'error': 'Usernames are required'}), 400
    
    usernames = [u.strip() for u in usernames_text.split('\n') if u.strip()]
    
    try:
        results = ultimate_checker.batch_check(usernames, platforms)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_usernames():
    data = request.json
    base_words = data.get('base_words', '')
    count = int(data.get('count', 10))
    style = data.get('style', 'combined')
    
    if not base_words:
        return jsonify({'error': 'Base words are required'}), 400
    
    base_words_list = [w.strip() for w in base_words.split(',') if w.strip()]
    
    try:
        results = ultimate_checker.generate_usernames(base_words_list, count, style)
        return jsonify({'usernames': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_results():
    data = request.json
    results = data.get('results', {})
    format_type = data.get('format', 'json')
    
    try:
        filename = ultimate_checker.export_results(results, format_type)
        return jsonify({'filename': filename, 'message': f'Exported to {filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# CLI Commands
@click.group()
def cli():
    """Ultimate Username Checker - Check username availability across multiple platforms."""
    pass

@cli.command()
@click.argument('username')
@click.option('--platforms', '-p', help='Specific platforms to check (comma-separated)')
@click.option('--output', '-o', type=click.Choice(['json', 'csv', 'txt']), help='Output format')
def check(username, platforms, output):
    """Check username availability."""
    platform_list = [p.strip() for p in platforms.split(',')] if platforms else None
    
    results = ultimate_checker.check_username(username, platform_list)
    
    if output:
        filename = ultimate_checker.export_results(results, output, f"{username}_check")
        click.echo(f"Results exported to {filename}")
    else:
        click.echo(json.dumps(results, indent=2))

@cli.command()
@click.argument('input_file', type=click.File('r'))
@click.option('--platforms', '-p', help='Specific platforms to check (comma-separated)')
@click.option('--output', '-o', type=click.Choice(['json', 'csv', 'txt']), help='Output format')
def batch(input_file, platforms, output):
    """Batch check usernames from a file."""
    usernames = [line.strip() for line in input_file if line.strip()]
    platform_list = [p.strip() for p in platforms.split(',')] if platforms else None
    
    results = ultimate_checker.batch_check(usernames, platform_list)
    
    if output:
        filename = ultimate_checker.export_results(results, output, "batch_check_results")
        click.echo(f"Results exported to {filename}")
    else:
        click.echo(json.dumps(results, indent=2))

@cli.command()
@click.argument('base_words')
@click.option('--count', '-c', default=10, help='Number of usernames to generate')
@click.option('--style', '-s', default='combined', 
              type=click.Choice(['simple', 'numbers', 'specialchars', 'combined']),
              help='Username generation style')
def generate(base_words, count, style):
    """Generate username suggestions."""
    base_words_list = [w.strip() for w in base_words.split(',')]
    
    usernames = ultimate_checker.generate_usernames(base_words_list, count, style)
    
    click.echo("Generated usernames:")
    for username in usernames:
        click.echo(f"  - {username}")

def start_web_server(host='127.0.0.1', port=5000, open_browser=True):
    """Start the web server."""
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    
    if open_browser:
        # Open browser after a short delay
        def open_browser_delayed():
            time.sleep(1.5)
            webbrowser.open(f'http://{host}:{port}')
        
        Thread(target=open_browser_delayed).start()
    
    print(f"Starting web server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    app.run(host=host, port=port, debug=False)

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--no-browser', is_flag=True, help='Do not open browser automatically')
def web(host, port, no_browser):
    """Start the web interface."""
    start_web_server(host, port, not no_browser)

if __name__ == '__main__':
    # Check if we're running in web mode or CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        # Remove 'web' from args so Click doesn't see it
        sys.argv.pop(1)
        if len(sys.argv) == 1:  # Only 'web' was provided
            start_web_server()
        else:
            cli()
    else:
        cli()
