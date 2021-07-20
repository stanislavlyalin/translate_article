# Deploy instructions

Server IP address: `34.70.243.200`

- Create file `translate_article.service` for automatic launch `uWSGI` when
server starts in the `/etc/systemd/system` directory. Content:

```ini
[Unit]
Description=uWSGI instance to serve translate_article server
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/translate_article
ExecStart=uwsgi --ini server.ini

[Install]
WantedBy=multi-user.target
```

- Add `uWSGI` to auto-launch:

```commandline
systemctl enable translate_article
```

- Start `uWSGI`:

```commandline
systemctl start translate_article
```

- Add file `translate_article` in the `/etc/nginx/sites-available` with
content:

```
server {
  listen 80;
  
  location / {
    include uwsgi_params;
    uwsgi_pass unix:/home/translate_article/translate_article.sock;
  }
}
```

- Turn on configuration block (see above) in `Nginx` conf

```commandline
ln -s /etc/nginx/sites-available/translate_article /etc/nginx/sites-enabled
```

- Test `Nginx` configuration

```commandline
nginx -t
```

- Restart `uWSGI` и `Nginx`

```

systemctl restart translate_article
systemctl restart nginx

```
