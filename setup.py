from setuptools import setup
import py2exe  # NOQA

setup(name="conmon",
      description="Connection Monitor",
      version="0.1.0",
      console=["conmon.py"],
      options={
          "py2exe": {
              "includes": ["psutil", "click"],
              "dll_excludes": ["mswsock.dll"]
          }
      },
      data_files=["logcfg.yml"]
      )
