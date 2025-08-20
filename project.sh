#!/usr/bin/env bash

# Create project root
mkdir -p stock_dashboard

# Create subfolders
mkdir -p stock_dashboard/stock_data
mkdir -p stock_dashboard/templates
mkdir -p stock_dashboard/static

# Create empty files
touch stock_dashboard/app.py
touch stock_dashboard/requirements.txt
touch stock_dashboard/templates/dashboard.html
touch stock_dashboard/static/style.css

echo "✅ stock_dashboard folder structure created!"
