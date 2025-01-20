## **Azure Setup Guide**
This section provides step-by-step instructions to set up an **Azure Log Analytics Workspace** for the Activity Tracker project.

### **1. Create an Azure Log Analytics Workspace**
1. Log in to the [Azure Portal](https://portal.azure.com/).
2. In the **Search Bar**, type **Log Analytics Workspace** and select it.
3. Click **+ Create**.
4. Fill in the required details:
   - **Subscription**: Select your subscription.
   - **Resource Group**: Create a new resource group (e.g., `codecraft_punehacker`) or select an existing one.
   - **Workspace Name**: Enter a unique name (e.g., `activity-tracker-workspace`).
   - **Region**: Choose a region close to your location (e.g., `Central India`).
5. Click **Review + Create**, then click **Create**.

---

### **2. Retrieve Workspace Details**
Once the workspace is created, collect the following details:
- **Workspace ID**:
  1. Navigate to your workspace in the Azure portal.
  2. Under **Settings**, select **Agents Management**.
  3. Copy the **Workspace ID**.
- **Primary Key**:
  1. In the same **Agents Management** section, copy the **Primary Key**.

Add these details to your scripts:
```bash
WORKSPACE_ID="Your Workspace ID"
PRIMARY_KEY="Your Primary Key"
```

---

### **3. Configure Diagnostic Settings**
To track logs effectively, enable diagnostic settings:
1. Navigate to your **Log Analytics Workspace**.
2. Under **Monitoring**, select **Diagnostic settings**.
3. Click **+ Add diagnostic setting**.
4. Name your setting (e.g., `activity-tracker-logs`).
5. Select the categories you want to log:
   - **Administrative**
   - **Sign-in logs**
   - **Audit logs**
6. Select **Send to Log Analytics Workspace** and choose your workspace.
7. Click **Save**.

---

### **4. Set Up Log Queries**
You can query the logs using **Azure Monitor**:
1. Go to **Azure Monitor** > **Logs**.
2. Select your workspace from the drop-down.
3. Use the following example query to view logs:
   ```kql
   ActivityLogs_CL
   | where TimeGenerated > ago(1h)
   | summarize Count=count() by bin(TimeGenerated, 15m), application_name_s
   | render barchart
   ```

---

### **5. Configure Alerts (Optional)**
Set up alerts to monitor anomalies or specific activities:
1. Go to **Azure Monitor** > **Alerts**.
2. Click **+ New Alert Rule**.
3. Select your **Log Analytics Workspace** as the resource.
4. Under **Condition**, choose **Custom log search**.
5. Enter a query (e.g., detect tampering or anomalies):
   ```kql
   ActivityLogs_CL
   | where movement_count_d > 1000
   | summarize TotalMovements = sum(movement_count_d)
   ```
6. Define the alert logic and set up **Action Groups** to receive notifications.

---

### **6. Azure CLI Integration**
For automation, ensure you have the **Azure CLI** installed:
1. Install the CLI:
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```
2. Log in to Azure:
   ```bash
   az login
   ```
3. Verify your subscription:
   ```bash
   az account list --output table
   ```

---

### **7. Purge Old Logs**
Use the following script to purge outdated logs:
```bash
curl -s -X POST "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/${WORKSPACE_NAME}/purge?api-version=2015-03-20" \
-H "Authorization: Bearer ${MANUAL_TOKEN}" \
-H "Content-Type: application/json" \
-d '{
    "table": "ActivityLogs_CL",
    "filters": [
        {
            "column": "timestamp_t",
            "operator": "<",
            "value": "2025-01-19T00:00:00Z"
        }
    ]
}'
```

---

### **8. Testing the Integration**
1. Run the activity tracker script:
   - **Linux**: `./activity_tracker.sh`
   - **Windows**: `python main.py`
2. Check logs in **Azure Monitor** > **Logs**.
3. Confirm that data appears in your workspace.

---

### **9. Troubleshooting**
- **Azure CLI Authentication Issue**: Run `az login` and ensure the correct subscription is selected.
- **Logs Not Showing**: Verify that the correct **Workspace ID** and **Primary Key** are set in your script.
- **Slow Log Updates**: Check the `LOG_INTERVAL` value in your script. Reduce it if necessary (e.g., `LOG_INTERVAL=10`).

---
