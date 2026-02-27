#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration module for exposure detection
"""

import os
from pathlib import Path

# Get the directory containing this file
CONFIG_DIR = Path(__file__).parent

# Default configuration file path
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "exposure_config.json")

__all__ = ['CONFIG_DIR', 'DEFAULT_CONFIG_FILE']