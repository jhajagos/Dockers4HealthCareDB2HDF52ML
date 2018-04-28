#!/bin/bash

cd /root/Git/CommonDataModelMapper/omop_cdm/concept_server/

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=concept_server.py
flask  run --host=0.0.0.0