#!/bin/bash
SERVICE_DIR="/etc/systemd/system"
ROOT_DIR=`dirname "$0"`

service="$1"
from=`realpath "${ROOT_DIR}/services/${service}.service"`
to="${SERVICE_DIR}/${service}.service"

rm ${to} 2> /dev/null
echo "${from} -> ${to}"
ln -s ${from} ${to}
