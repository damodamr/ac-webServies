from emborec import app
import os

app.secret_key = os.urandom(25)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)