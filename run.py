import os
from app import app

PORT = 8000
if 'PORT' in os.environ:
   PORT = os.environ['PORT']

app.run(host='0.0.0.0', port=PORT, debug=True)


