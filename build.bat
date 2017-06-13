dist\conmon.exe stop
dist\conmon.exe remove
pyinstaller -F --hidden-import=win32timezone conmon.py -i conmon.ico --version-file version.py
copy config.yml dist\
dist\conmon.exe --startup=auto install
dist\conmon.exe start
