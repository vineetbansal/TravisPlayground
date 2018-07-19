from mypack import create_app
from mypack.settings import DEBUG


application = create_app(debug=DEBUG)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=80, threaded=True)