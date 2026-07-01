#!/bin/bash

echo "Stopping all microservices..."
pkill -f "python3 app.py"
echo "All services stopped."