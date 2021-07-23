Build image:
sudo docker build --tag=flask_image_captioner_api . 

Check that built image exists:
sudo docker image ls 

Run built image:
sudo docker run -d -p 5000:5000 flask_image_captioner_api