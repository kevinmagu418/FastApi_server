---
title: Bingwa Scanner API
emoji: 🔍
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🌿 Bingwa Scanner Backend System

This repository contains the FastAPI backend for the Bingwa image scanning and classification system, hosted on Hugging Face Spaces.

## 🚀 Overview

The FastAPI service acts as the bridge for mobile app requests (like BingwaShambani), handling image uploads, processing the machine learning models (like `all-MiniLM-L6-v2`), and returning the analysis results safely.

## ⚙️ Configuration Details
- **Framework:** FastAPI
- **Hosting:** Hugging Face Spaces (Docker SDK)
- **Port:** `7860` (Custom configured via Dockerfile)

## 💻 Running the Server Locally

If you want to run or test the FastAPI server on your local machine:

**1. Install Dependencies**
```bash
# Recommended to use a virtual environment
pip install -r requirements.txt
