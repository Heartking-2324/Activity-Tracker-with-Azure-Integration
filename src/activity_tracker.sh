#!/bin/bash

# Azure Details
WORKSPACE_NAME="activity-tracker-workspace"
SUBSCRIPTION_ID="your-subscription-id"  # Replace with your Subscription ID
RESOURCE_GROUP="your-resource-group"    # Replace with your Resource Group name
MANUAL_TOKEN="your-manual-token"        # Replace with your manually retrieved token

# Interval for sending data to Azure (in seconds)
LOG_INTERVAL=15

# Function to send mouse tracking logs to Azure
send_mouse_logs_to_azure() {
    local movement_count="$1"
    local distinct_positions="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local logs=$(cat <<EOF
[{
    "timestamp": "$timestamp",
    "movement_count": $movement_count,
    "distinct_positions": $distinct_positions
}]
EOF
)
    curl -s -X POST "https://${WORKSPACE_NAME}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01" \
        -H "Authorization: Bearer $MANUAL_TOKEN" \
        -H "Content-Type: application/json" \
        -H "Log-Type: MouseActivityLogs" \
        -d "$logs"
}

# Function to purge old logs in Azure
purge_old_logs() {
    curl -s -X POST "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/${WORKSPACE_NAME}/purge?api-version=2015-03-20" \
        -H "Authorization: Bearer $MANUAL_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "table": "ActivityLogs_CL",
            "filters": [
                {
                    "column": "timestamp_t",
                    "operator": "<",
                    "value": "'"$(date -u --date='1 day ago' +'%Y-%m-%dT%H:%M:%SZ')"'"
                }
            ]
        }'
}

# Function to track mouse activity and send logs to Azure
track_mouse_activity() {
    local last_x=0
    local last_y=0
    local movement_count=0
    local distinct_positions=()

    echo "Starting mouse activity tracking and data sending to Azure..."
    while true; do
        # Get current mouse position
        read x y < <(xdotool getmouselocation --shell | grep -E 'X=|Y=' | awk -F= '{print $2}')
        
        # Check if the position has changed
        if [[ "$x" != "$last_x" || "$y" != "$last_y" ]]; then
            movement_count=$((movement_count + 1))
            distinct_positions+=("$x,$y")
            last_x=$x
            last_y=$y
        fi

        # Every LOG_INTERVAL seconds, send logs to Azure
        if (( $(date +%s) % LOG_INTERVAL == 0 )); then
            distinct_count=$(echo "${distinct_positions[@]}" | tr ' ' '\n' | sort | uniq | wc -l)
            send_mouse_logs_to_azure "$movement_count" "$distinct_count"
            movement_count=0
            distinct_positions=()
        fi

        # Sleep for a short duration to reduce CPU usage
        sleep 0.1
    done
}

# Main script logic
{
    # Start mouse tracking in the background
    track_mouse_activity &

    # Run purging every 24 hours in the background
    while true; do
        purge_old_logs
        sleep 86400
    done
} &
wait
