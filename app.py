import streamlit as st
import sys
import os

# ---------------------------------------------------------
# Add src folder to Python path
# ---------------------------------------------------------

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# ---------------------------------------------------------
# Import your agents
# ---------------------------------------------------------

from agents import (
    incident_agent,
    category_agent,
    priority_agent,
    knowledge_agent,
    decision_agent
)

# ServiceNow API
from servicenow import create_incident


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Service Desk Agent",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS - MAKE TEXT BIGGER
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 20px;
        margin-bottom: 30px;
    }

    /* Section headings */
    h2 {
        font-size: 30px !important;
    }

    h3 {
        font-size: 24px !important;
    }

    /* Normal text */
    p, label, .stMarkdown {
        font-size: 18px !important;
    }

    /* Text area */
    textarea {
        font-size: 18px !important;
    }

    /* Buttons */
    .stButton > button {
        font-size: 19px !important;
        font-weight: bold !important;
        padding: 12px 25px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Service Desk Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent incident classification, priority prediction, '
    'knowledge retrieval and ServiceNow ticket creation'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# INCIDENT INPUT
# ---------------------------------------------------------

st.subheader("📝 Describe Your IT Issue")

incident = st.text_area(
    "Enter your incident:",
    placeholder="Example: VPN is not connecting to the office network",
    height=150
)


# ---------------------------------------------------------
# ANALYZE INCIDENT BUTTON
# ---------------------------------------------------------

if st.button("🔍 Analyze Incident", use_container_width=True):

    if not incident.strip():

        st.warning("Please enter an incident first.")

    else:

        # ---------------------------------------------
        # Initial state
        # ---------------------------------------------

        state = {
            "incident": incident,
            "category": "",
            "priority": "",
            "resolution": "",
            "assignment_group": ""
        }

        # ---------------------------------------------
        # Run agents
        # ---------------------------------------------

        with st.spinner("AI agents are analyzing the incident..."):

            state = incident_agent(state)

            state = category_agent(state)

            state = priority_agent(state)

            state = knowledge_agent(state)

            state = decision_agent(state)

        # ---------------------------------------------
        # Store result in session state
        # ---------------------------------------------

        st.session_state["incident_result"] = state


# ---------------------------------------------------------
# DISPLAY RESULT
# ---------------------------------------------------------

if "incident_result" in st.session_state:

    result = st.session_state["incident_result"]

    st.divider()

    st.header("🤖 AI Analysis")


    # -------------------------------------------------
    # Incident
    # -------------------------------------------------

    st.subheader("Incident")

    st.info(result["incident"])


    # -------------------------------------------------
    # Classification / Priority
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📂 Category")

        st.success(result["category"])


    with col2:

        st.subheader("🚨 Priority")

        st.warning(result["priority"])


    # -------------------------------------------------
    # Assignment Group
    # -------------------------------------------------

    st.subheader("👥 Assignment Group")

    st.info(result["assignment_group"])


    # -------------------------------------------------
    # Resolution
    # -------------------------------------------------

    st.subheader("💡 Recommended Resolution")

    st.success(result["resolution"])


    # -------------------------------------------------
    # CREATE SERVICENOW TICKET
    # -------------------------------------------------

    st.divider()

    st.header("🎫 ServiceNow")


    if st.button(
        "🚀 Create ServiceNow Ticket",
        use_container_width=True
    ):

        with st.spinner("Creating ServiceNow incident..."):

            ticket = create_incident(

                short_description=result["incident"],

                description=(
                    f"Incident: {result['incident']}\n\n"
                    f"Category: {result['category']}\n"
                    f"Priority: {result['priority']}\n\n"
                    f"Recommended Resolution:\n"
                    f"{result['resolution']}"
                ),

                category=result["category"],

                priority=result["priority"],

                assignment_group=result["assignment_group"]
            )


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        if ticket["success"]:

            st.success(
                "✅ ServiceNow ticket created successfully!"
            )

            st.subheader("🎫 Incident Number")

            st.code(
                ticket["number"],
                language=None
            )

            st.write(
                "The incident has been successfully created "
                "in your ServiceNow PDI."
            )


        # -------------------------------------------------
        # FAILURE
        # -------------------------------------------------

        else:

            st.error(
                "❌ Failed to create ServiceNow ticket."
            )

            st.error(
                f"Status Code: {ticket.get('status_code', 'Unknown')}"
            )

            st.code(
                ticket.get("message", "Unknown error"),
                language=None
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI Service Desk Agent • Machine Learning + RAG + "
    "Agentic Workflow + ServiceNow REST API"
)