#!/usr/bin/env bash

# ---------------------------------------------------
# Script: run.sh
# Purpose: Start FastAPI application using uvicorn
# Safe: uses strict mode and quoted variables
# ---------------------------------------------------

set -euo pipefail

APP="main:app"

python -m uvicorn "$APP" --reload