from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask('app')

#Set up DB
DATABASE = 'blogPosts.db'
db = sqlite3.connect(DATABASE)
cursor = db.cursor() # create a cursor object
cursor.execute('CREATE TABLE IF NOT EXISTS blogPosts (\
ID INTEGER PRIMARY KEY AUTOINCREMENT, \
TITLE TEXT NOT NULL, \
BODY TEXT NOT NULL)')
db.commit() # save changes
db.close()

#Render Home Page
@app.route('/')
def start_page():
  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  query = cur.execute('SELECT * FROM blogPosts').fetchall()
  posts = {}

  for ID, TITLE, BODY in query:
    posts[TITLE] = BODY

  conn.commit()
  conn.close()
  return render_template("index.html", posts = posts)

#Render Page to add Post
@app.route('/addBlogPost')
def add_blog_post():
  return render_template("addBlogPost.html")

#Render/Re-render post confirmation or page to add post
@app.route('/addBlogPost', methods=["POST"])
def create_post():
  title = str(request.form.get("Post Title"))
  content = str(request.form.get("Post Content"))
  
  titleLen = len(title)
  contentLen = len(content)

  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  cur.execute('INSERT INTO blogPosts (TITLE, BODY) VALUES (?, ?)', (title, content))
  conn.commit()
  conn.close()

  error = "Please enter a post title under 300 characters and post content under 1000 characters"

  if title != "None" and content != "None":
    if titleLen > 0 and titleLen < 300 and contentLen > 0 and contentLen < 1000:
      return render_template("postAdded.html", title = title, content = content)
    else:
      return render_template("addBlogPost.html", error = error)

  return render_template("addBlogPost.html", error = error)


app.run(host='0.0.0.0', port=8080)