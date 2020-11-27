#!/usr/bin/env sh

set -u

nginx_config_file="/etc/nginx/conf.d/default.conf"
template_file="/tmp/nginx.conf"

# need to copy the template into the container, because you otherwise get
# an error trying to replace the contents with sed, since `-i` replaces the file
# instead of editing it in place. We could probably just pipe the sed output to 
# the config file and avoid this copy step, but whatever
cp ${template_file} ${nginx_config_file}

if [ "${NGINX_BASIC_ENABLED:-true}" != "true" ]; then
    echo "NGINX basic auth is disabled. Skipping setup..."
    exit 0
fi

if [ -z "${NGINX_BASIC_USER}" ]; then
    echo "'NGINX_BASIC_USER' env var not set"
    exit 1
fi

if [ -z "${NGINX_BASIC_PASS}" ]; then
    echo "'NGINX_BASIC_PASS' env var not set"
    exit 1
fi

which htpasswd
is_htpasswd_installed=$?

if [ ${is_htpasswd_installed} -gt 0 ]; then
    echo "htpasswd not installed"
    exit 1
fi

passwd_file="/etc/nginx/.htpasswd"
touch ${passwd_file} 
htpasswd -b -C 17 ${passwd_file} ${NGINX_BASIC_USER} ${NGINX_BASIC_PASS}

sed -i \
    's/#REPLACE_FOR_BASIC_AUTH/auth_basic "dev"; auth_basic_user_file \/etc\/nginx\/\.htpasswd;/g' \
    ${nginx_config_file}

echo "Config"
echo "---------"
nginx -T
echo "---------"

grep "auth_basic" ${nginx_config_file}
if [ $? -gt 0 ]; then
  echo "Basic auth setup failed"
  exit 1
fi

echo "done"
