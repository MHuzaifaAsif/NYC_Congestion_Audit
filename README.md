# 🚕 NYC Congestion Pricing Audit

A data analytics pipeline and interactive dashboard to audit NYC TLC valid/invalid yellow taxi trips, monitor anomaly rate (ghost trips), and visualize revenue potential relating to congestion pricing. 

## 🚀 Features
- **Data Pipeline (`pipeline.py`)**: Downloads NYC TLC Trip Record data, processes it via Dask, and flags "Ghost Trips" (e.g. Impossible speeds, teleporting vehicles).
- **Interactive Dashboard (`dashboard.py`)**: A Streamlit application built with Plotly featuring a premium dark mode UI to visualize hourly trip patterns, revenue contributions, and anomaly compliance metrics.

## 🛠️ Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NYC_Congestion_Audit.git
   cd NYC_Congestion_Audit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Data Pipeline**:
   *Downloads data & generates the `outputs/` directory.*
   ```bash
   python pipeline.py
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

## ☁️ Deployment (Streamlit Community Cloud)
To deploy this application for free on the web:
1. Push this repository to GitHub, ensuring `.gitignore` allows the `outputs/` folder (where the `.parquet` data resides) to be committed.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
3. Click **New App**, select your repository, set the Main file path to `dashboard.py`, and click **Deploy**.
