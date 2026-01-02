#!/bin/bash

# Talos Demonstration Sequence
# Usage: ./demo.sh

echo "🚀 Booting Talos Sentinel Agent..."
echo "======================================"

# 1. Enforce Simulation Mode for Safety
# This ensures no real funds are risked during the presentation.
export TALOS_MODE="SIMULATION"
export MAX_TX_PER_SESSION=5

echo "[CONFIG] Execution Mode: $TALOS_MODE"
echo "[CONFIG] Safety Guardrails: ENABLED"
echo "======================================"

# 2. Execute the Main Mission Routine
python mission_night.py

echo "======================================"
echo "✅ Demo Sequence Concluded Successfully."
