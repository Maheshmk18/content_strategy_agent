import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Content Strategy Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar configuration
st.sidebar.title(" Configuration")
API_URL = st.sidebar.text_input("API URL", value="http://localhost:8000/api", key="api_url")


# Initialize session state
if "current_month" not in st.session_state:
    st.session_state.current_month = datetime.now().strftime("%B %Y")
if "plan_id" not in st.session_state:
    st.session_state.plan_id = None
if "calendar_data" not in st.session_state:
    st.session_state.calendar_data = None
if "plan_status" not in st.session_state:
    st.session_state.plan_status = None
    

def health_check() -> bool:
    
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_URL.replace('/api', '')}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def generate_plan(month: str) -> dict:
    
    """Call the generate-plan endpoint."""
    try:
        response = requests.post(
            f"{API_URL}/generate-plan",
            json={"month": month},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating plan: {str(e)}")
        return None

def get_calendar(plan_id: str) -> dict:
    
    """Fetch the calendar for a plan."""
    try:
        response = requests.get(
            f"{API_URL}/calendar/{plan_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f" Error fetching calendar: {str(e)}")
        return None

def get_plan_status(plan_id: str) -> dict:
    """Get the status of a plan."""
    try:
        response = requests.get(
            f"{API_URL}/status/{plan_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f" Error fetching status: {str(e)}")
        return None

def approve_plan(plan_id: str) -> bool:
    
    """Approve a plan."""
    try:
        response = requests.post(
            f"{API_URL}/approve/{plan_id}",
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f" Error approving plan: {str(e)}")
        return False

# Main app
st.title("Content Strategy Agent")
st.markdown("Generate, review, and manage your 30-day content calendar")

# Check API connection
if not health_check():
    st.error("Cannot connect to API. Make sure the FastAPI server is running at " + API_URL.replace('/api', ''))
    st.info("Run: `uvicorn api.main:app --reload`")
    st.stop()

st.success("Connected to API")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Generate Plan", "View Calendar", "Plan History"])

with tab1:
    st.subheader("Generate a New Content Plan")

    col1, col2 = st.columns([2, 1])

    with col1:
        month_input = st.text_input(
            "Enter Month (e.g., June 2025)",
            value=st.session_state.current_month,
            key="month_input"
        )

    with col2:
        st.write("")  # Spacing
        generate_btn = st.button("Generate Plan", use_container_width=True, key="generate_btn")

    if generate_btn:
        with st.spinner("Generating your content plan..."):
            result = generate_plan(month_input)

            if result:
                st.session_state.plan_id = result.get("plan_id")
                st.session_state.current_month = month_input

                # Display results
                st.success("Plan generated successfully!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Plan ID", result.get("plan_id", "N/A")[:8] + "...")
                with col2:
                    st.metric("Status", result.get("status", "N/A").upper())
                with col3:
                    st.metric("Calendar Days", result.get("calendar_days", "N/A"))

                # Email notification
                if result.get("email_sent"):
                    st.info(f"📧 Calendar delivered via Email")

                # Auto-fetch calendar
                st.session_state.calendar_data = get_calendar(st.session_state.plan_id)

                st.balloons()

with tab2:
    st.subheader("30-Day Content Calendar")

    if st.session_state.plan_id:
        st.info(f"Plan ID: `{st.session_state.plan_id}`")

        # Fetch latest calendar if not in session
        if st.session_state.calendar_data is None:
            st.session_state.calendar_data = get_calendar(st.session_state.plan_id)

        if st.session_state.calendar_data and "calendar" in st.session_state.calendar_data:
            calendar = st.session_state.calendar_data["calendar"]
            quality_score = st.session_state.calendar_data.get("quality_score", "N/A")

            # Show quality score
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.metric("Quality Score", f"{quality_score}/10")
            with col2:
                approve_btn = st.button("Approve Plan", key="approve_btn", type="primary")
                if approve_btn:
                    if approve_plan(st.session_state.plan_id):
                        st.success(" Plan approved!")
                        st.session_state.plan_status = "approved"

            # Display calendar as table
            st.markdown("### Calendar Preview")

            # Convert to DataFrame for better display
            df = pd.DataFrame(calendar)

            # Format the dataframe
            display_df = df[["day", "date", "platform", "content_type", "topic"]].copy()

            # Use colored columns based on platform
            def color_platform(val):
                if val == "LinkedIn":
                    return "background-color: #0A66C2"
                elif val == "Instagram":
                    return "background-color: #E4405F"
                elif val == "YouTube":
                    return "background-color: #FF0000"
                return ""

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )

            # Expandable details
            with st.expander("📖 View Full Details"):
                for day in calendar:
                    with st.container(border=True):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.subheader(f"Day {day['day']}")
                            st.caption(day['date'])
                            # Platform badge
                            platform_colors = {
                                "LinkedIn": "#0A66C2",
                                "Instagram": "#E4405F",
                                "YouTube": "#FF0000"
                            }
                            color = platform_colors.get(day['platform'], "#666666")
                            st.markdown(f"<div style='background-color: {color}; color: white; padding: 5px 10px; border-radius: 4px; text-align: center; font-weight: bold;'>{day['platform']}</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"**{day['topic']}**")
                            st.markdown(f"*Content Type: {day['content_type']}*")
                            st.markdown(f"📝 {day['notes']}")
        else:
            st.warning("No calendar data available. Generate a plan first.")
    else:
        st.info("Generate a plan in the **Generate Plan** tab to see the calendar here.")

with tab3:
    st.subheader("Plan History & Status")

    if st.session_state.plan_id:
        plan_id_input = st.text_input(
            "Enter Plan ID to check status:",
            value=st.session_state.plan_id,
            key="status_plan_id"
        )

        if st.button("Check Status", key="check_status_btn"):
            status = get_plan_status(plan_id_input)
            if status:
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Plan ID**: {status.get('plan_id')}")
                    st.info(f"**Status**: {status.get('status', 'N/A').upper()}")
                with col2:
                    if status.get('created_at'):
                        st.info(f"**Created**: {status.get('created_at')}")
                    if status.get('approved_at'):
                        st.info(f"**Approved**: {status.get('approved_at')}")
    else:
        st.info("Generate a plan first to track its status.")


# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
    <p>Content Strategy Agent | Powered by LangChain & Claude</p>
</div>
""", unsafe_allow_html=True)
