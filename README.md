# Calculator App Project

1. Create a GitHub account (carefully select your username because it will be your identity for a long time)
2. ⁠Create and push or fork into your GitHub account a simple Python application 
3. Dockerize the Python App and run it locally 
4. ⁠create a new repo named (first_docker_image) and push all your Dockerfile.
5. ⁠document your process with screenshots using markdown and push to that same repo..



# Step 1
- I created a repository
![alt text](<image/Repo image.png>)

# Step 2
- I pushed a python app(calculator.py) to my github
![alt text](<image/calc code.png>)

# Step 3
- I visited https://hub.docker.com/ python to get the python image I need for this project

- I dockerized the python app(calculator.py) and ran it locally
![alt text](<image/docker build.png>)
![alt text](<image/Repo image.png>)

- To run this command locall I turned on docker desktop

- Then build the dockerfile using the below command:
```
docker build -t web-calculator 
```

# Step 4
- I ran the command to get the url for the python app
```
docker run --rm -p 5000:5000 web-calculator
```

![alt text](<image/web upload.png>)

- I opened the url provided and got this result

![alt text](<image/calc 1.png>)
