#!/usr/bin/env python3

import cgi
import os
from urllib.parse import urlsplit

def upload_form_html():
  return """
  <form action="{0}" method="post" enctype="multipart/form-data" >
    <input type="file" id="file" name="file">
    <input type="submit" value="Upload" name="submit">
  </form> """.format(os.getenv("REQUEST_URI"))

def home_page_link_html():
  endpoint = os.getenv("REQUEST_URI")
  return '<p><a href="{0}">Go back</a></p>'.format(urlsplit(endpoint).path)

def files_html():
  files = os.listdir('store/')
  endpoint = os.getenv("REQUEST_URI")
  fmt = """
  <li> 
    <form action="{0}" style="display:inline;">
      <button type="submit" name="delete" value="{1}">delete</button>
    </form>
    <a href="store/{1}">{1}</a> 
  </li>
  """
  files_list_html = '\n'.join([fmt.format(endpoint, file) for file in files])

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
  print('Uploading ...<br>'.format(outname))

  with open(outname, 'wb') as outfile:
    outfile.write(form['file'].value)

  print('Saved {0} bytes to <a href="{1}">{1}</a> \n'.format(
    len(form['file'].value),
    outname
  ))

  print(home_page_link_html())

def main():
  form = cgi.FieldStorage()
  print('Content-Type: text/html\n')

  method = os.getenv('REQUEST_METHOD')

  os.makedirs("store", exist_ok=True)

  print('<html>\n <body>')
  if method == "GET":
    get(form)
  if method == "POST":
    post(form)
  print('</body> \n</html>')

main()
