---
title: Clinical Audit Environment
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---
# Clinical Decision Audit Environment (OpenEnv)

## Overview
This project simulates auditing of clinical decisions to detect errors, risks, and missing steps.

## Tasks
- Easy: Identify basic issue in decision
- Medium: Detect missing steps or incorrect treatment
- Hard: Full audit with reasoning

## API Endpoints
- GET /reset → returns new case
- POST /step → submit audit response
- GET /state → current state

## Run locally
```bash
pip install -r requirements.txt
python -m uvicorn api:app --reload
Agent receives clinical case → responds → environment evaluates with partial reward (0–1 scale)
“Deployed on Hugging Face Spaces using FastAPI”

## Problem
Healthcare decisions are often inconsistent. This environment simulates clinical cases and evaluates decisions using an AI-agent style reward system.

## Features
Real-world clinical case simulation
OpenEnv-style API (reset, step)
Multi-level tasks: easy → medium → hard
Reward scoring (0.0 – 1.0)
Partial credit system (not binary)
Deployed on Hugging Face Spaces
