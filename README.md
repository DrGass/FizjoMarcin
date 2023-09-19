# FizjoMarcin
 
Simple FastAPI website, training for work and in future website for my brother.
## Commands
- uvicorn app.main:app --reload : starting uvicorn server
- black <filename> = formatting files

### Containers:
 
- docker-compose build : build image
- docker-compose down -v : delete containers and volumes
- docker-compose -f ./docker-compose.yml --env-file ./app/.env up : start containers with env file
- docker exec -it fastapi_container bash : going into container terminal

### Testing
- pytest : starting tests
- --lf : last failed
- -vv : show full errors 