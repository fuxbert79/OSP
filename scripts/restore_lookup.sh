#!/bin/bash
# Restore lookup data after container restart
sleep 10  # Warte bis Container läuft
docker exec pipelines mkdir -p /mnt/HC_Volume_104189729/osp/lookups
docker cp /mnt/HC_Volume_104189729/osp/lookups/kontakt_wkz_mapping.json pipelines:/mnt/HC_Volume_104189729/osp/lookups/
docker restart pipelines
echo "$(date): Lookup restored" >> /var/log/osp-lookup.log
