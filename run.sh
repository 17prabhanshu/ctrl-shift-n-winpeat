#!/bin/bash
# run.sh
pip3 install -r requirements.txt --break-system-packages
streamlit run app/app.py --server.headless true
