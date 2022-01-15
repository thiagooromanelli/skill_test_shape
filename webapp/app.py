from flask import Flask

app = Flask("webapp")


@app.route("/ping")
def ping():
    return {"message": "PONG"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
