# importing flask (Install it using python -m pip install flask)
from flask import *
from flask import Response


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='megaman', password='megaman'))
users.append(User(id=2, username='loai', password='loai'))

app = Flask(__name__)  # initialising flask
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


# defining the routes for the home() funtion (Multiple routes can be used as seen here)
@app.route("/")
def homepage():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = None
        for x in users:
            if x.username == username:
                user = x
                break
        if user == None:
            return redirect(url_for('login'))

        if user and user.password != password:
            return redirect(url_for('login'))
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('terminal'))

        return redirect(url_for('login'))

    return render_template('login.html')


# defining the routes for the account() funtion
# @app.route("/account", methods=["POST"])
# def account():
#     admin = "megaman"
#     adminpassword = "hackerone"
#     usr = ""  # Creating a variable usr
#     pss = ""
#     if (request.method == "POST"):  # Checking if the method of request was post
#         usr = request.form["username"]
#         pss = request.form["password"]
#         # if name is not defined it is set to default string
#         if not usr or (usr != admin or pss != adminpassword):
#             return redirect("login")

#     # rendering our account.html contained within /templates
#         return redirect("terminal")


@app.route("/terminal")
def terminal():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('terminal.html')
    # rendering our home.html contained within /templates


if __name__ == "__main__":  # checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True, port=4949)  # running flask (Initalised on line 4)
