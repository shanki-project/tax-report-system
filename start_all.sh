#!/bin/bash

echo "Starting all 6 microservices..."

# Set Gmail credentials
export GMAIL_ADDRESS="shankidevadiga@gmail.com"
export GMAIL_APP_PASSWORD="qeao shas wtpn wbfv"

# Start each service in background, log to its own file
cd user-service && python3 app.py > ../logs/user-service.log 2>&1 &
echo "User Service started (PID $!)"
cd ..

cd report-service && python3 app.py > ../logs/report-service.log 2>&1 &
echo "Report Service started (PID $!)"
cd ..

cd rename-service && python3 app.py > ../logs/rename-service.log 2>&1 &
echo "Rename Service started (PID $!)"
cd ..

cd db-service && python3 app.py > ../logs/db-service.log 2>&1 &
echo "DB Service started (PID $!)"
cd ..

cd notification-service && python3 app.py > ../logs/notification-service.log 2>&1 &
echo "Notification Service started (PID $!)"
cd ..

cd download-service && python3 app.py > ../logs/download-service.log 2>&1 &
echo "Download Service started (PID $!)"
cd ..

echo ""
echo "All services running. Logs in ./logs/"
echo "To stop all: bash stop_all.sh"