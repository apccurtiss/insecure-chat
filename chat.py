#!/bin/env python
import logging
from app import create_app, socketio

app = create_app(debug=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    socketio.run(app)
