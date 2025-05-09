import streamlit as st
import os
import requests
import time

# Set up the Streamlit app
st.title("AI Research Report Generator")

# Input fields
topic = st.text_input("Topic", value="AI")
year = st.text_input("Year", value="2025")
tasks = st.multiselect(
    "Select Tasks",
    options=[
        "task-research", "task-data", "task-report", "task-ethics",
        "task-master", "task-presentation", "task-dashboard"
    ],
    default=["task-research", "task-data", "task-report", "task-ethics", "task-master", "task-presentation", "task-dashboard"]
)

# Button to generate the report
if st.button("Generate Report"):
    with st.spinner("Generating report..."):
        # Make API call to Flask backend
        payload = {
            "topic": topic,
            "year": year,
            "tasks": tasks
        }
        response = requests.post("http://localhost:5000/api/generate", json=payload)

        if response.status_code == 200:
            data = response.json()
            files = data.get("files", [])
            if files and files[0]["name"] == "master_report.md":
                # Display the Markdown content
                st.markdown("### Generated Master Report")
                st.markdown(files[0]["content"])

                # Provide a download link
                with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "master_report.md"), "r") as f:
                    st.download_button(
                        label="Download Master Report (Markdown)",
                        data=f.read(),
                        file_name="master_report.md",
                        mime="text/markdown"
                    )
            else:
                st.error("No master report generated. Check logs for details.")
        else:
            st.error(f"Error generating report: {response.json().get('error', 'Unknown error')}")

# Progress updates
st.markdown("### Progress Updates")
progress_container = st.empty()

# Poll the /api/progress endpoint
def stream_progress():
    with requests.get("http://localhost:5000/api/progress", stream=True) as response:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    data = json.loads(decoded_line[5:])
                    progress_container.text(data["message"])
                    if "All tasks completed" in data["message"]:
                        break

if st.button("Start Progress Monitoring"):
    stream_progress()