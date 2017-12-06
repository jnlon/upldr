#!/usr/bin/env python3

import cgi
import os

def upload_form_html():
  return """
  <form action="/files/" method="post" enctype="multipart/form-data" >
    <input type="file" id="file" name="file">
    <input type="submit" value="Upload" name="submit">
  </form> """

def home_page_link_html():
  return '<p><a href="/files/">Go back</a></p>'

def files_html():

  files = os.listdir('store/')
  fmt = """
  <li> 
    <form action="/files/" style="display:inline;">
      <button type="submit" name="delete" value="{0}">delete</button>
    </form>
    <a href="store/{0}">{0}</a> 
  </li>
  """
  files_list_html = '\n'.join([fmt.format(file) for file in files])

  return """
    <h2> Files ({}) </h2>
    <ul> {} </ul>
  """.format(len(files), files_list_html)

def get(form):
  if 'delete' in form: # ?delete=<filename>
    filename = os.path.basename(form['delete'].value)
    filename = os.path.join('store', filename)

    # Are we deleting an actual valid file?
    if not os.path.isfile(filename):
      print("Invalid path '{}'".format(filename))
      print(home_page_link_html())
      return

    print("Deleting '{}'...<br>".format(filename))
    os.remove(filename)
    print("Done")
    print(home_page_link_html())
  else:
    print(upload_form_html())
    print(files_html())

def post(form):
  filename = form['file'].filename
  if filename == '':
    print("No file submitted")
    print(home_page_link_html())
    return

  outname = os.path.join("store", os.path.basename(filename))
  print('Saving to {}...<br>'.format(outname))
  with open(outname, 'wb') as outfile:
    outfile.write(form['file'].value)
  print('Done writing {} bytes\n'.format(len(form['file'].value)))
  print(home_page_link_html())

def main():
  form = cgi.FieldStorage()
  print('Content-Type: text/html\n')
  method = os.getenv("REQUEST_METHOD")

  os.makedirs("store", exist_ok=True)

  print('<html>\n <body>')
  if method == "GET":
    get(form)
  if method == "POST":
    post(form)
  print('</body> \n</html>')

main()
