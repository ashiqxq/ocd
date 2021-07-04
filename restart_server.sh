#!/bin/sh
. env/bin/activate
echo yes | python3 src/manage.py collectstatic
sudo supervisorctl reload
sudo systemctl reload nginx