from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True

list_of_errors = []
save_data = {"usr":"", "eml":""}

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify-password']
    email = request.form['email']

    save_data["usr"] = username
    save_data["eml"] = email

    #username error check
    error_checker(username, "username_error")

    #password error check
    error_checker(password, "password_error")

    #verify password error check
    if verify_password != password:
        if "verify-password_error" not in list_of_errors:
            list_of_errors.append("verify-password_error")
    elif "verify-password_error" in list_of_errors:
        list_of_errors.remove("verify-password_error")

    #email error check
    if email != '':
        if email.count(".") != 1 or email.count("@") != 1:
            if "email_error" not in list_of_errors:
                list_of_errors.append("email_error")
        else: error_checker(email, "email_error")
    elif "email_error" in list_of_errors:
        list_of_errors.remove("email_error")

    if len(list_of_errors) > 0:
        return redirect("/?error=")

    return render_template('welcome.html', username=username)


def error_checker(field, err_type):
    if len(field) < 3 or len(field) > 20 or ' ' in field:
        if err_type not in list_of_errors:
            list_of_errors.append(err_type)
    elif err_type in list_of_errors:
        list_of_errors.remove(err_type)


@app.route("/")
def index():
    encoded_error = request.args.get("error")

    return render_template('index.html', 
    list_of_errors=list_of_errors, save_data=save_data,
    error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()