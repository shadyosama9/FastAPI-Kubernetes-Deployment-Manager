from fastapi import FastAPI, HTTPException
from kubernetes import client, config
from dotenv import load_dotenv
import httpx
import os

load_dotenv()
app = FastAPI()
PROMETHEUS_URL = "http://192.168.59.108:31220" # todo : Move to a .env file 
config.load_incluster_config()

@app.post("/createdeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name, labels={"app": deployment_name}),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"app": deployment_name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name="nginx-app",
                        image="nginx:latest",
                        ports=[client.V1ContainerPort(container_port=80)]
                    )
                ])
            )
        )
    )

    k8s_apps_v1 = client.AppsV1Api()
    try:
        k8s_apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment
        )
        return {"message": f"Deployment {deployment_name} created successfully."}
    except client.exceptions.ApiException as e:
        raise HTTPException(status_code=e.status, detail=e.body)



@app.get("/getpromdetails")
async def get_prom_details():
    try:
        async with httpx.AsyncClient() as client:
            query = 'kube_pod_info'
            response = await client.get(f"{os.getenv("PROMETHEUS_URL")}/api/v1/query?query={query}")
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and 'result' in data['data']:
                return data['data']['result']
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch pod details")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
