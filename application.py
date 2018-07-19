import logging
from logging.handlers import RotatingFileHandler

from mypack import create_app
from mypack.settings import DEBUG


application = create_app(debug=DEBUG)


if __name__ == '__main__':
    application.run(threaded=True)