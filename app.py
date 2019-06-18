import os, ssl
from sanic import Sanic, response

app = Sanic(__name__)


@app.route("/")
async def index(request):
    return response.json({"Hello,": "world!"})

if __name__ == "__main__":
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("./.ssl/name_of_cert_file.crt", keyfile="./.ssl/name_of_key_file.key")


app.go_fast(host="0.0.0.0", port=8443, ssl=context, workers=os.cpu_count(), debug=True)