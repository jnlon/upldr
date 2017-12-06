# upldr
Simple CGI script for uploading and deleting files on your http server. Made
because I was tired of managing files in my webroot with ssh/scp. Uploaded
files are stored in `store/` in the same directory as the script itself.

## Sample nginx config

For this to work you need:

1. `fcgiwrap` installed and running as the same user as your nginx server. Here it's listening on port 8890

2. Create an .htpasswd file for basic auth ([guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-password-authentication-with-nginx-on-ubuntu-14-04))

3. Configure and enable https, otherwise basic auth is useless ([guide](http://nginx.org/en/docs/http/configuring_https_servers.html))

```
server {

    # Be sure to enable SSL!
    listen       443 ssl;
    ...
 
    # Put upldr.py in files/ in your webroot
    location /files/ {

      # Enable basic auth so only you can upload and delete
      auth_basic "Upldr files";
      auth_basic_user_file $document_root/files/.htpasswd; 

      gzip off;
      fastcgi_pass 127.0.0.1:8890;

      # Set important CGI variables
      fastcgi_param  QUERY_STRING       $query_string;
      fastcgi_param  REQUEST_METHOD     $request_method;
      fastcgi_param  CONTENT_TYPE       $content_type;
      fastcgi_param  CONTENT_LENGTH     $content_length;
      fastcgi_param  REQUEST_URI        $request_uri;
      fastcgi_param  DOCUMENT_URI       $document_uri;
      fastcgi_param  DOCUMENT_ROOT      $document_root;
      fastcgi_param  SCRIPT_NAME        upldr.py;
      fastcgi_param  SCRIPT_FILENAME    $document_root/files/upldr.py;

      # Disable basic auth in store/ so files are public if you know the url
      location /files/store {
        auth_basic off;
        gzip on; 
      }   
    }   
    ...
}
```

