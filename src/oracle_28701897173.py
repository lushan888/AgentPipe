#!/usr/bin/env python3
"""
The Oracle of the Repository: Creator of Contributor Pages for AgentPipe.
This script generates a functional, self-contained HTML page in /contributors/ that honors our contributors with corporate imagery and golden egg decorations.
"""

import os
from pathlib import Path
import re

# Configuration
REPO_DIR = Path(__file__).parent.parent
OUTPUT_PATH = REPO_DIR / "contributors"
HTML_PATH = OUTPUT_PATH / "index.html"

def create_contributor_page():
    """
    Generates the complete HTML content for '/contributors/index.html'.
    
    The page is designed to:
    1. Feature a corporate goose image (SVG embedded).
    2. List contributors who are NOT C-Suite members.
    3. Include relevant facts and links to GitHub profiles.
    4. Decorate with golden egg animations via SVG/Canvas.
    
    Note: This is valid Python code that can be run directly in the browser if it were executed, 
    but here we provide a self-contained HTML file for deployment or static analysis review.
    """

    # Create output directory if needed (ensure clean state)
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Milestones - AgentPipe Contributors</title>
    
    <!-- Google Fonts: Playfair Display for headings -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400&display=swap" rel="stylesheet">

    <!-- Load a corporate goose SVG (embedded for self-containment) -->
    <link href='https://fonts.googleapis.com/icon?family=Material+Icons' rel='stylesheet'>

    <style>
        :root {
            --gold-primary: #D4AF37; /* Golden Egg Gold */
            --gold-secondary: #C5A028;
            --dark-text: #1a1a1a;
            --light-bg: #f9f9f9;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Lato', sans-serif;
            background-color: var(--light-bg);
            color: var(--dark-text);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        /* Hero Section */
        .hero {
            height: 80vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: linear-gradient(135deg, #eef2f6 0%, #ffffff 100%);
        }

        /* Corporate Goose SVG (Embedded) */
        .hero-image {
            width: 40%;
            max-width: 800px;
            filter: drop-shadow(0 20px 30px rgba(0,0,0,0.15));
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .hero-content {
            text-align: center;
            z-index: 2;
        }

        h1 {
            font-family: 'Playfair Display', serif;
            color: var(--gold-primary);
            margin-bottom: 4rem;
            letter-spacing: -0.5px;
        }

        .hero-content p {
            font-size: 1.2rem;
            max-width: 600px;
            margin: 0 auto;
            color: #333;
        }

        /* Section Styling */
        section {
            padding: 4rem 5%;
            background-color: var(--light-bg);
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        }

        h2 {
            font-family: 'Playfair
