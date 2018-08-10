#!/usr/bin/env python3

import django.core.management
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.core.management.execute_from_command_line(sys.argv)
