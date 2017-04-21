#!/usr/bin/env bash 

curl "http://localhost:9600/solr/irroc/update/csv?commit=true&f.meta_description.split=true&f.meta_description.separator=,&f.stage_list.split=true&f.stage_list.separator=;&f.task_list.split=true&f.task_list.separator=;&f.stage_list_facet.split=true&f.stage_list_facet.separator=;&f.task_list_facet.split=true&f.task_list_facet.separator=;" --data-binary @$1 -H 'Content-type:text/csv; charset=utf-8'

