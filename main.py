from flask import Flask, render_template, request

app = Flask('app')

#Render Home Page
@app.route('/')
def start_page():
  return render_template("index.html")

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
  print(title)
  print(content)
  error = "Please enter a post title under 300 characters and post content under 1000 characters"

  if title != "None" and content != "None":
    if titleLen > 0 and titleLen < 300 and contentLen > 0 and contentLen < 1000:
      return render_template("postAdded.html", title = title, content = content)

  return render_template("addBlogPost.html", error = error)


app.run(host='0.0.0.0', port=8080)