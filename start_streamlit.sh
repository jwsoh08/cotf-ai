#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install streamlit

cd /var/www/my_streamlit_app
sudo pip3 install -r requirements.txt
sudo python3 -m streamlit run main.py
