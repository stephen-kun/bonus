#!/bin/sh

killall uwsgi

sleep 1

uwsgi -x django.xml
