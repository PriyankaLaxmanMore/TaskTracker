#!/usr/bin/env bash

# ---------------------------------------------------
# Script: test.sh
# Purpose: Run pytest with coverage report
# ---------------------------------------------------

set -euo pipefail

export PYTHONPATH="."

pytest --cov=. --cov-report=term-missing