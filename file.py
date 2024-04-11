import sys
import os

print(sys.path)
print('----')
pythonpath = os.environ.get('PYTHONPATH', '').split(os.pathsep)
print(pythonpath)
