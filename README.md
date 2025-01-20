# Activity Tracker with Azure Integration

## Overview
This project tracks user activities (mouse movements, system usage, and active applications) on both **Linux** and **Windows** platforms. It sends logs to **Azure Log Analytics** for real-time monitoring and tamper detection. Designed for cybersecurity and productivity analysis, this tool ensures seamless integration and insightful analytics.

## Features
- Cross-platform support: Linux and Windows
- Tracks mouse movements, system usage, and active application
- Sends logs to Azure Log Analytics workspace
- Identifies tampering and anomalies using AI-based analysis
- Provides visualization and alerts in Azure Monitor
- Purge outdated logs for efficient data management

## Technologies Used
- Python
- Bash
- Azure Log Analytics
- JavaScript/HTML (for visualization)

## Prerequisites
- Python 3.x
- Azure CLI
- Access to Azure Log Analytics workspace
- Required Python modules (see `requirements.txt`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/activity-tracker.git
   cd activity-tracker

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

3. Set up Azure workspace:
- Note down your Workspace ID and Primary Key.
- Add them to the respective scripts.

## Usage

- Linux
Run the activity_tracker.sh script:

```bash
chmod +x src/activity_tracker.sh
./src/activity_tracker.sh
```

Windows
Run the main.py script:

```bash
python src/main.py
```
Contributing
Feel free to contribute! Fork this repository and submit a pull request.
