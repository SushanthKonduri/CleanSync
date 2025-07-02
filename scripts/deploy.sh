#!/bin/bash

# CleanSync Deployment Script
# This script handles the deployment of the CleanSync application

set -e

# Configuration
DOCKER_IMAGE="cleansync-app"
DOCKER_TAG="${BUILD_NUMBER:-latest}"
CONTAINER_NAME="cleansync-container"
PORT="5000"

echo "Starting CleanSync deployment..."

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log "ERROR: Docker is not running or not accessible"
        exit 1
    fi
    log "Docker is running"
}

# Function to build Docker image
build_image() {
    log "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
    docker build -t "${DOCKER_IMAGE}:${DOCKER_TAG}" .
    docker tag "${DOCKER_IMAGE}:${DOCKER_TAG}" "${DOCKER_IMAGE}:latest"
    log "Docker image built successfully"
}

# Function to stop and remove existing container
cleanup_container() {
    log "Cleaning up existing container..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
    log "Container cleanup completed"
}

# Function to run new container
run_container() {
    log "Starting new container: ${CONTAINER_NAME}"
    docker run -d \
        --name "${CONTAINER_NAME}" \
        -p "${PORT}:5000" \
        -v "$(pwd)/uploads:/app/uploads" \
        -v "$(pwd)/logs:/app/logs" \
        --restart unless-stopped \
        "${DOCKER_IMAGE}:${DOCKER_TAG}"
    
    log "Container started successfully"
}

# Function to health check
health_check() {
    log "Performing health check..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "http://localhost:${PORT}/" > /dev/null 2>&1; then
            log "Health check passed! Application is running"
            return 0
        fi
        
        log "Health check attempt ${attempt}/${max_attempts} failed, retrying in 5 seconds..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    log "ERROR: Health check failed after ${max_attempts} attempts"
    return 1
}

# Function to show container status
show_status() {
    log "Container status:"
    docker ps -a --filter "name=${CONTAINER_NAME}"
    
    log "Container logs (last 20 lines):"
    docker logs --tail 20 "${CONTAINER_NAME}" 2>/dev/null || true
}

# Function to rollback
rollback() {
    log "ERROR: Deployment failed, rolling back..."
    cleanup_container
    
    # Try to run the previous version
    if docker images | grep -q "${DOCKER_IMAGE}"; then
        log "Attempting to run previous version..."
        run_container
        if health_check; then
            log "Rollback successful"
        else
            log "ERROR: Rollback failed"
            exit 1
        fi
    else
        log "ERROR: No previous version available for rollback"
        exit 1
    fi
}

# Main deployment process
main() {
    log "Starting CleanSync deployment process..."
    
    # Check prerequisites
    check_docker
    
    # Build new image
    build_image
    
    # Cleanup existing container
    cleanup_container
    
    # Run new container
    run_container
    
    # Health check
    if health_check; then
        log "Deployment completed successfully!"
        show_status
    else
        log "ERROR: Deployment failed"
        rollback
    fi
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "build")
        check_docker
        build_image
        ;;
    "stop")
        cleanup_container
        ;;
    "status")
        show_status
        ;;
    "logs")
        docker logs -f "${CONTAINER_NAME}" 2>/dev/null || log "Container not found"
        ;;
    *)
        echo "Usage: $0 {deploy|build|stop|status|logs}"
        echo "  deploy  - Full deployment (default)"
        echo "  build   - Build Docker image only"
        echo "  stop    - Stop and remove container"
        echo "  status  - Show container status"
        echo "  logs    - Show container logs"
        exit 1
        ;;
esac 