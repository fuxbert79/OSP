#!/bin/bash
# Restore lookup data after container restart
sleep 10  # Warte bis Container läuft
docker exec pipelines mkdir -p /opt/osp/lookups
docker cp /opt/osp/lookups/kontakt_wkz_mapping.json pipelines:/opt/osp/lookups/
docker restart pipelines
echo "$(date): Lookup restored" >> /var/log/osp-lookup.log
