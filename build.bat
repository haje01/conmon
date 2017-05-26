dist\conmon.exe stop
dist\conmon.exe remove
pyinstaller -F --hidden-import=win32timezone conmon.py
copy _config.yml dist\
dist\conmon.exe --startup=auto install
dist\conmon.exe start
