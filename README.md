# FastAPI Kubernetes Deployment Manager

A FastAPI application to manage Kubernetes deployments and fetch Prometheus metrics. This application provides RESTful endpoints to create Kubernetes deployments and retrieve pod details from Prometheus.

## Overview

This project demonstrates how to:
- Use FastAPI to create RESTful endpoints.
- Deploy a FastAPI application on Kubernetes.
- Create Kubernetes deployments programmatically using the Kubernetes Python client.
- Fetch and display metrics from Prometheus.

The FastAPI application includes the following endpoints:
- `POST /createdeployment/{deployment_name}`: Create a new Kubernetes deployment with the specified name.
- `GET /getpromdetails`: Fetch and display pod details from Prometheus.

## Prerequisites

- **Docker**: To build and run Docker containers.
- **Kubernetes**: A running Kubernetes cluster.
- **kubectl**: Command-line tool for interacting with the Kubernetes cluster.
- **Prometheus**: A running Prometheus instance accessible from the Kubernetes cluster.
- **Python 3.10**: For running the FastAPI application locally.

## Steps

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/fastapi-k8s-deployment-manager.git
    cd fastapi-k8s-deployment-manager
    ```

2. **Set up environment variables**
    - Create a `.env` file in the root of your project with the following content:
      ```env
      PROMETHEUS_URL=http://<your-prometheus-url>
      ```

3. **Build the Docker image**
    ```bash
    docker build -t fastapi-k8s-deployment-manager .
    ```

4. **Push the Docker image to Docker Hub (optional)**
    ```bash
    docker tag fastapi-k8s-deployment-manager yourusername/fastapi-k8s-deployment-manager
    docker push yourusername/fastapi-k8s-deployment-manager
    ```

5. **Apply Kubernetes configurations**

    - Apply RBAC configuration
      ```bash
      kubectl apply -f k8s/rbac.yaml
      ```

    - Deploy the FastAPI application
      ```bash
      kubectl apply -f k8s/deployment.yaml
      ```

    - Expose the FastAPI application using a service
      ```bash
      kubectl apply -f k8s/service.yaml
      ```

6. **Access the FastAPI application**

    - Get the NodePort of the service
      ```bash
      kubectl get svc fast-api-service
      ```
    - Access the application at `http://<node-ip>:<node-port>`

7. **Use the FastAPI application**

    - Create a new Kubernetes deployment
      ```bash
      curl -X POST http://<node-ip>:<node-port>/createdeployment/{deployment_name}
      ```

    - Fetch pod details from Prometheus
      ```bash
      curl http://<node-ip>:<node-port>/getpromdetails
      ```

## Notes

- Ensure your Prometheus instance is running and accessible from the Kubernetes cluster.
- Customize the Kubernetes deployment and service configurations as needed.

