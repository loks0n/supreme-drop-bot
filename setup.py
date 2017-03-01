import sys
import os
import requests
from multiprocessing import Queue
from cx_Freeze import setup, Executable
#os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")       (requests.certs.where(),'cacert.pem')
os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Python36-32\\tcl\\tk8.6"
build_exe_options = {
	"packages": ["multiprocessing","time", "sys", "requests", "hashlib", "os","json", "requests", "bs4", "splinter","selenium", "pygubu"],
	"include_files": ["tcl86t.dll", "tk86t.dll", "gui.ui", "favicon.ico", "config.json", "chromedriver.exe", "README.md"]
}
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(  name = "Supreme Drop Bot",
        version = "1.0",
        description = "Supreme Drop Bot",
        options = {"build_exe": build_exe_options},
executables = [Executable("main.py", base=base)])
