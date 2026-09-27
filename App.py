from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import urllib.robotparser

app = Flask(__name__)

EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

HTML = """
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>School Email Finder</title>
    <style>
        body { font-family: Arial; max-width: 700px; margin: 40px auto; padding: 20px; }
        input, button { width: 100%; padding: 12px; margin: 8px 0; box-sizing: border-box; }
        button { background: #111; color: white; border: 0; border-radius: 6px; }
        .email { padding: 8px; border-bottom: 1px solid #ddd; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>School Email Finder</h1>
    <p>Find publicly displayed email addresses on a school's website.</p>

    <form method="post">
        <input name="url" placeholder="https://example-school.com" required>
        <button type="submit">Find Public Emails</button>
    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    {% if emails %}
        <h2>Public emails found: {{ emails
