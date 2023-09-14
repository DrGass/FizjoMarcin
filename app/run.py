import uvicorn
from env import get_env

env = get_env()

if __name__ == '__main__':
    reload = True if env.environment == 'development' else False
    uvicorn.run(
        "main:create_app",
        host=env.host,
        port=env.port,
        reload=reload,
    )
