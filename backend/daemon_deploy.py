# daemon_deploy.py
import asyncio
from agentscope_runtime.engine.deployers.local_deployer import LocalDeployManager
from agent_app import app  # Import the configured app


# Deploy in daemon mode
async def main():
    await app.deploy(LocalDeployManager())


if __name__ == "__main__":
    asyncio.run(main())
    input("Press Enter to stop the server...")
