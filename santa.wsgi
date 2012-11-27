import logging, sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/home/andrew/secret-santa/')
from secret_santa import app as application

sys.stdout = sys.stderr
