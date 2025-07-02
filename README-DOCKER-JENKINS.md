# CleanSync - Docker & Jenkins CI/CD Project

## Project Overview

CleanSync is an automated data cleaning and preprocessing tool that has been containerized using Docker and integrated with Jenkins for continuous integration and deployment (CI/CD). This project demonstrates modern DevOps practices including containerization, automated testing, and deployment pipelines.

## 🐳 Docker Setup

### Prerequisites
- Docker Desktop installed and running
- Docker Compose (usually comes with Docker Desktop)

### Quick Start with Docker

1. **Build and run using Docker Compose:**
   ```bash
   cd CleanSync-main
   docker-compose up --build
   ```

2. **Or build and run manually:**
   ```bash
   # Build the Docker image
   docker build -t cleansync-app .
   
   # Run the container
   docker run -d -p 5000:5000 --name cleansync-container cleansync-app
   ```

3. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Upload a CSV file and test the data cleaning features

### Docker Commands

```bash
# Build image
docker build -t cleansync-app .

# Run container
docker run -d -p 5000:5000 --name cleansync-container cleansync-app

# View logs
docker logs cleansync-container

# Stop container
docker stop cleansync-container

# Remove container
docker rm cleansync-container

# View running containers
docker ps

# View all containers
docker ps -a
```

## 🔄 Jenkins CI/CD Pipeline

### Prerequisites
- Jenkins server installed and running
- Docker installed on Jenkins server
- Git repository configured

### Jenkins Pipeline Features

The Jenkins pipeline includes the following stages:

1. **Checkout** - Pulls code from repository
2. **Install Dependencies** - Installs Python packages
3. **Code Quality Check** - Runs flake8 and pylint
4. **Unit Tests** - Runs pytest with coverage
5. **Integration Tests** - Tests the application functionality
6. **Build Docker Image** - Creates Docker image
7. **Docker Security Scan** - Scans for vulnerabilities
8. **Deploy to Test Environment** - Deploys to test environment
9. **Performance Test** - Runs basic performance tests

### Setting up Jenkins Pipeline

1. **Create a new Jenkins job:**
   - Go to Jenkins dashboard
   - Click "New Item"
   - Select "Pipeline"
   - Name it "CleanSync-Pipeline"

2. **Configure the pipeline:**
   - In the pipeline configuration, select "Pipeline script from SCM"
   - Choose your SCM (Git)
   - Enter your repository URL
   - Set branch to `*/main` or your default branch
   - Set script path to `Jenkinsfile`

3. **Install required Jenkins plugins:**
   - HTML Publisher Plugin
   - Email Extension Plugin
   - Docker Pipeline Plugin

4. **Configure email notifications:**
   - Go to Jenkins > Manage Jenkins > Configure System
   - Set up SMTP settings for email notifications

### Pipeline Configuration

The pipeline automatically:
- Builds the Docker image
- Runs tests and quality checks
- Deploys to test environment
- Sends email notifications on success/failure
- Generates test coverage reports

## 📁 Project Structure

```
CleanSync-main/
├── app.py                 # Flask web application
├── CleanSync/            # Core CleanSync package
│   ├── __init__.py
│   ├── autoclean.py      # Main CleanSync class
│   ├── modules.py        # Supporting modules
│   └── test_autoclean.py # Unit tests
├── templates/            # HTML templates
├── static/              # CSS, JS, and static files
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── Jenkinsfile          # Jenkins pipeline
├── .dockerignore        # Docker ignore file
├── requirements.txt     # Python dependencies
├── scripts/
│   └── deploy.sh        # Deployment script
├── sample_data.csv      # Sample data for testing
└── README-DOCKER-JENKINS.md # This file
```

## 🚀 Deployment Scripts

### Automated Deployment

Use the deployment script for automated deployments:

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Deploy the application
./scripts/deploy.sh

# Build only
./scripts/deploy.sh build

# Stop application
./scripts/deploy.sh stop

# Check status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs
```

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
# Development
FLASK_ENV=development
FLASK_DEBUG=1

# Production
FLASK_ENV=production
FLASK_DEBUG=0
```

### Docker Compose Environment

Edit `docker-compose.yml` to modify:
- Port mappings
- Volume mounts
- Environment variables
- Health checks

## 🧪 Testing

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov flake8 pylint

# Run unit tests
python -m pytest CleanSync/test_autoclean.py -v

# Run with coverage
python -m pytest CleanSync/test_autoclean.py -v --cov=CleanSync --cov-report=html

# Run code quality checks
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pylint CleanSync/
```

### Integration Tests

```bash
# Test the example script
python example.py

# Test the CLI tool
python clean_my_data.py sample_data.csv
```

## 📊 Monitoring and Logging

### Application Logs

```bash
# View container logs
docker logs cleansync-container

# Follow logs in real-time
docker logs -f cleansync-container

# View logs from deployment script
./scripts/deploy.sh logs
```

### Health Checks

The application includes health checks:
- Docker health check in Dockerfile
- Application health endpoint at `/`
- Automated health checks in deployment script

## 🔒 Security

### Docker Security

- Non-root user in container
- Minimal base image (python:3.10-slim)
- Security scanning with Trivy
- Regular base image updates

### Best Practices

- Use specific version tags for dependencies
- Scan images for vulnerabilities
- Keep base images updated
- Use multi-stage builds for production

## 📈 Performance

### Optimization

- Multi-stage Docker builds
- Layer caching optimization
- Minimal dependencies
- Efficient Python package installation

### Monitoring

- Health check endpoints
- Performance testing in pipeline
- Resource usage monitoring
- Log aggregation

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using port 5000
   netstat -tulpn | grep :5000
   
   # Stop existing container
   docker stop cleansync-container
   ```

2. **Docker build fails:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -t cleansync-app .
   ```

3. **Jenkins pipeline fails:**
   - Check Jenkins logs
   - Verify Docker is running on Jenkins server
   - Ensure all required plugins are installed

### Debug Commands

```bash
# Check container status
docker ps -a

# Inspect container
docker inspect cleansync-container

# Execute commands in container
docker exec -it cleansync-container /bin/bash

# View container resource usage
docker stats cleansync-container
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Testing with pytest](https://docs.pytest.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note:** This project demonstrates modern DevOps practices and can be used as a template for other Python web applications that need containerization and CI/CD automation. 