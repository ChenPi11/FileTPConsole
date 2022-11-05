@echo off
nuitka --standalone --show-progress --show-memory --enable-plugin=numpy --output-dir=out main.windows.py
pause