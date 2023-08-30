# FizjoMarcin
 
Simple FastAPI website, training for work and in future website for my brother.

In order to make the docker work i needed to add this PYTHON PATH variable to Dockerfile because otherwise there was no option for it to work.

And in order to make uvicorn start on docker i needed to manually insert ip adress from etc/hosts because it couldn't translate hostname into ip. so in file database.py the "localhost" variable needs to be changed to "127.0.0.2"