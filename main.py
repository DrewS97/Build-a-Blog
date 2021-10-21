from flask import Flask, render_template, request

app = Flask('app')

@app.route('/')
def start_page():
  return render_template("index.html")

@app.route('/addBlogPost')
def create_post():
  return render_template("addBlogPost.html")

app.run(host='0.0.0.0', port=8080)