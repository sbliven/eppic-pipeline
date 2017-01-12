#!/usr/bin/env bash
#workon luigi
exec luigid --background \
  --pidfile /data/spencer/eppic/luigid/luigid.pid \
  --logdir /data/spencer/eppic/luigid/log/ \
  --port 8090
