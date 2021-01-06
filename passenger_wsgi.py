import sys, os

sys.path.append(os.getcwd())

sys.path.append('app')

from app import app as application

if __name__ == '__main__':
    app.run(threaded=True)