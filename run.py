from app import app
import os


app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 5000))
app.debug = True
app.run()