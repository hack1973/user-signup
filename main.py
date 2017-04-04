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
import re
page_header = """</DOCTYPE html>
            <html>
                <head>
                    <title>User Signup
                    </title>
                    <style type="text/css">
                        .error {
                            color: red;
                        }
                    </style>
                </head>
                <body>
                    <h1>Signup
                    </h1>
"""

page_footer = """</body>
            </html>
"""

page_body = """  <form method="post">
                        <table>
                            <tr>
                                <td class="label">
                                    Username
                                </td>
                                <td>
                                    <input type="text" name="username" value="{username}">
                                </td>
                                <td class="error">
                                    {error_username}
                                </td>
                            </tr>
                            <tr>
                                <td class="label">
                                    Password
                                </td>
                                <td>
                                    <input type="password" name="password" value="">
                                </td>
                                <td class="error">
                                    {error_password}
                                </td>
                            </tr>
                            <tr>
                                <td class="label">
                                    Verify Password
                                </td>
                                <td>
                                    <input type="password" name="verify" value="">
                                    <span class="error"></span>
                                </td>
                                <td class="error">
                                    {error_verify}
                                </td>
                            </tr>
                            <tr>
                                <td class="label">
                                    Email (Optional)
                                </td>
                                <td>
                                    <input type="text" name="email" value="{email}">
                                    <span class="error"></span>
                                </td>
                                <td class="error">
                                    {error_email}
                                </td>
                            </tr>
                        </table>
                        <input type= "submit">
                    </form>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PW_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):
    def get(self):
        username = ""
        error_username = ""
        error_password = ""
        error_verify = ""
        email = ""
        error_email = ""

        new_body = page_body.format(username = username, error_username = error_username, error_password = error_password, error_verify = error_verify, email = email, error_email = error_email)
        content = page_header + new_body + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        #if password == "":
        #    self.redirect("/?error=Please enter a password!")

        if username == "":
            #self.redirect("/?error=Please enter a Username!")
            error_username = "Please enter a Username!"
            have_error = True

        elif not valid_username(username):
            error_username = "That's not a valid username!"
            have_error = True

        if not valid_password(password):
            error_password = "That was not a valid password!"
            have_error = True

        elif password != verify:
            error_verify = "The passwords didn't match!"
            have_error = True

        if not valid_email(email):
            error_email = "That's not a valid email!"
            have_error = True

        if have_error:
            #self.redirect('/', **params)
            new_body = page_body.format(username = username, error_username = error_username, error_password = error_password, error_verify = error_verify, email = email, error_email = error_email)
            content = page_header + new_body + page_footer
            self.response.write(content)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):

        username = self.request.get('username')

        #if valid_username == username:
        #    self.redirect('/welcome')
        #else:
        #    self.redirect('/')

        response = "Welcome, " + username + "!"
        response_header = "<h1>" + response + "</h1>"
        self.response.write(response_header)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
