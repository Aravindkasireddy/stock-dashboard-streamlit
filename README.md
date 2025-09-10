📈 Stock Price Dashboard (Streamlit + AWS EC2)

An interactive Stock Price Dashboard built with Streamlit
.
This app allows users to fetch, visualize, and analyze stock market data with live charts. It runs locally or can be deployed on AWS EC2 with Nginx reverse proxy.

🚀 Features

🔍 Search for stock tickers (AAPL, TSLA, MSFT, etc.)

📊 Interactive table view with historical stock data

📈 Line chart of closing prices over time

💾 Download stock data as CSV

🔄 Yahoo Finance as the primary data source, Alpha Vantage fallback to handle rate limits

☁️ Deployment-ready for AWS EC2

🛠️ Installation (Run Locally)

Clone this repo

git clone https://github.com/<your-username>/stock-dashboard-streamlit.git
cd stock-dashboard-streamlit


Create virtual environment

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Run the app

streamlit run app.py


Open in browser:

http://localhost:8501

📦 Requirements

Dependencies are listed in requirements.txt:

streamlit
yfinance
pandas
matplotlib
requests


Install them with:

pip install -r requirements.txt

☁️ Deployment on AWS EC2
1. Launch EC2 Instance

AMI: Ubuntu 22.04 or 24.04

Open ports: 22 (SSH), 80 (HTTP), 8501 (optional)

2. Connect to EC2
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

3. Setup Environment
sudo apt update && sudo apt install python3-venv nginx -y
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

4. Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

5. Configure Nginx Reverse Proxy

Create /etc/nginx/sites-available/streamlit:

server {
    listen 80;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


Enable it:

sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

6. Access Your App

👉 http://<EC2_PUBLIC_IP>

📸 Screenshots

Add your screenshots here for better visibility (e.g., stock chart and table).

📜 License

This project is licensed under the MIT License.
