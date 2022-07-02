from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

# app.add_url_rule('/', 'hello',hello_world)

@app.route('/home')
def home():
    return 'Home'

@app.route('/profile/<path:id>')
def profile(id):
    return 'Hello %s' % id

@app.route('/admin')
def admin():
    return 'Hello admin'

@app.route('/guest/<guest>')
def guest(guest):
    return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def user(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest', guest=name))


if __name__=="__main__":
    app.run(debug=True)