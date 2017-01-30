#!/usr/bin/env bash
#workon luigi
exec luigid --background \
  --pidfile /data/luigid/luigid.pid \
  --logdir /data/luigid/log/ \
  --port 8090
