@echo off
C:\Users\yuese\AppData\Local\Programs\Python\Python310\python.exe -m nuitka --standalone --show-progress --show-memory --enable-plugin=numpy --enable-plugin=rich --output-dir=out main.windows.py
pause
