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

main_content = """  <form method="post">
                        <table>
                            <tr>
                                <td>
                                    <label for="username">Username</label>                                        </td>
                                <td>
                                    <input name="username" type="text" value required>
                                    <span class="error"></span>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="password">Password</label>
                                </td>
                                <td>
                                    <input name="password" type="password" required>
                                    <span class="error"></span>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="verify">Verify Password</label>
                                </td>
                                <td>
                                    <input name="verify" type="password" required>
                                    <span class="error"></span>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="email">Email (Optional)</label>
                                </td>
                                <td>
                                    <input name="email" type="email" value>
                                    <span class="error"></span>
                                </td>
                            </tr>
                        </table>
                        <input type= "submit">
                    </form>
"""
USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PW_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return password and PW_RE.match(password)

#VERIFY_RE = re.compile(r"^.{3,20}$")
#def valid_verify(verify):
#    return VERIFY_RE.match(verify)

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return  not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):
    def get(self):
        content = page_header + main_content + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if username == "":
            self.redirect("/?error=Please enter a Username!")

        if password == "":
            self.redirect("/?error=Please enter a password!")

        params = dict(username = username,
                        email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username!"
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That was not a valid password!"
            have_error = True
        elif password != verify:
            params['error_verify'] = "The passwords didn't match!"
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email!"
            have_error = True

        if have_error:
            self.redirect('/')#, **params)
        else:
            self.redirect('/welcome?=username=', username)

class Welcome(webapp2.RequestHandler):
    def get(self):

        username = self.request.get("username")

        response = "Welcome, " + username + "!"
        response_header = "<h1>" + response + "</h1>"
        self.response.write(response_header)
        #self.response.write(password)
        #self.response.write(verify)
        #self.response.write(email)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
