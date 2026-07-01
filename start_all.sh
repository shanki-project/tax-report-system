#!/bin/bash

echo "Starting all 6 microservices..."

export GMAIL_ADDRESS="shankidevadiga@gmail.com"
export GMAIL_APP_PASSWORD="qeao shas wtpn wbfv"

ROOT_DIR=$(pwd)
mkdir -p $ROOT_DIR/logs

python3 $ROOT_DIR/user-service/app.py > $ROOT_DIR/logs/user-service.log 2>&1 &
echo "User Service started (PID $!)"

python3 $ROOT_DIR/report-service/app.py > $ROOT_DIR/logs/report-service.log 2>&1 &
echo "Report Service started (PID $!)"

python3 $ROOT_DIR/rename-service/app.py > $ROOT_DIR/logs/rename-service.log 2>&1 &
echo "Rename Service started (PID $!)"

python3 $ROOT_DIR/db-service/app.py > $ROOT_DIR/logs/db-service.log 2>&1 &
echo "DB Service started (PID $!)"

python3 $ROOT_DIR/notification-service/app.py > $ROOT_DIR/logs/notification-service.log 2>&1 &
echo "Notification Service started (PID $!)"

python3 $ROOT_DIR/download-service/app.py > $ROOT_DIR/logs/download-service.log 2>&1 &
echo "Download Service started (PID $!)"

echo ""
echo "All services started. Logs in $ROOT_DIR/logs/"