import logging, sys, os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,os.path.abspath('.'))
from secret_santa import app as application

sys.stdout = sys.stderr
