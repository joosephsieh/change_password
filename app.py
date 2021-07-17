from flask import Flask, request, render_template
from libs.func import validate_password, save_password

app = Flask(__name__)


@app.route("/change_password", methods=["POST"])
def change_password():
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    is_valid, message = validate_password(old_password, new_password)
    if is_valid:
        is_saved = save_password(new_password)
        if is_saved:
            return message, 200
        else:
            return "Unknown error", 500
    return message, 400


if __name__ == '__main__':
    app.run()
