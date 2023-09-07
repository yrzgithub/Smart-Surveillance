import sys
from os import listdir,getcwd,join

modules = listdir(join(getcwd(),"modules.txt"))
for module in modules:
  print("Installing {module}...")
  sys("pip install {module}")