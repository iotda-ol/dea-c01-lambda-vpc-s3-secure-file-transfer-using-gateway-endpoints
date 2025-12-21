#!/bin/bash
# Start local SFTP server using Docker

echo "Starting local SFTP server..."

# Pull SFTP Docker image
docker pull atmoz/sftp

# Create upload directory
mkdir -p /tmp/sftp-data/upload

# Run SFTP server
docker run -d \
    --name test-sftp-server \
    -p 2222:22 \
    -v /tmp/sftp-data:/home/testuser/upload \
    atmoz/sftp \
    testuser:testpass:1001:100:upload

echo "SFTP server started on port 2222"
echo "Username: testuser"
echo "Password: testpass"
echo "Upload directory: /home/testuser/upload"
echo ""
echo "To stop: docker stop test-sftp-server"
echo "To remove: docker rm test-sftp-server"
