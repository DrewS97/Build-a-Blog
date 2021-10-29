from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask('app')

#Set up DB
DATABASE = 'blogPosts.db'

#Use database without values
def sql(cmd):
  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  query = cur.execute(cmd).fetchall()
  conn.commit()
  conn.close()
  return query

#Use database with values
def sqlVal(cmd, vals=None):
  conn = sqlite3.connect(DATABASE)
  cur = conn.cursor()
  query = cur.execute(cmd, vals).fetchall()
  conn.commit()
  conn.close()
  return query

#Render Home Page With All Posts Or Indiviual When Clicked
@app.route('/')
def start_page():
  query = sql('SELECT * FROM blogPosts')
  id = request.args.get('ID')
  if id != None:
    #Grab values
    title = sqlVal('SELECT TITLE FROM blogPosts WHERE ID=?', (id,))
    body = sqlVal('SELECT BODY FROM blogPosts WHERE ID=?', (id,))
    return render_template('individualBlog.html', TITLE = title, BODY = body)
  return render_template("index.html", query = query)

#Render Page to add Post
@app.route('/addBlogPost')
def add_blog_post():
  return render_template("addBlogPost.html")

#Render/Re-render post confirmation or page to add post
@app.route('/addBlogPost', methods=["POST"])
def create_post():
  #Input info
  title = str(request.form.get("Post Title"))
  content = str(request.form.get("Post Content"))
  titleLen = len(title)
  contentLen = len(content)

  error = "Please enter a post title under 300 characters and post content under 1000 characters"

  if title != "None" and content != "None":
    if titleLen > 0 and titleLen < 300 and contentLen > 0 and contentLen < 1000:
      #Insert into DB
      sqlVal('INSERT INTO blogPosts (TITLE, BODY) VALUES (?, ?)', (title, content))
      return render_template("postAdded.html", title = title, content = content)
    else:
      return render_template("addBlogPost.html", error = error)

  return render_template("addBlogPost.html", error = error)


app.run(host='0.0.0.0', port=8080)