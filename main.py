#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Blogs(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("mainpage.html")
        blogs_query = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC LIMIT 5")
        render_content = t.render(blogs_query = blogs_query)
        self.response.write(render_content)

class NewPost(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("newpost.html")
        render_content = t.render()
        self.response.write(render_content)
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if (not title) or (title.strip() == "") or (not content) or (content.strip() == ""):
            error = "We need both a title and some content!"
            t = jinja_env.get_template("newpost.html")
            render_content = t.render(error=error, title=title, content=content)
            self.response.write(render_content)
        else:
            blog = Blogs(title = title, content = content)
            blog.put()
            self.redirect("/")
# class BlogDetail(Handler):
# 	    def get(self, blog_id):
# 	        blog = Blogs.get_by_id(int(blog_id))
# 	        if not blog:
# 	            self.error(404)
#
#
# 	        t = jinja_env.get_template('blog_detail.html')
# 	        content = t.render(blog=blog)
#
#
# 	        self.response.write(content)
# webapp2.Route('/<blog_id:\d+>', BlogDetail)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost)    
], debug=True)
