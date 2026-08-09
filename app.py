import streamlit as st
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agents import (
    incident_agent,
    category_agent,
    priority_agent,
    knowledge_agent,
    decision_agent
)

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Agentic AI Service Desk",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

.main-title{
    font-size:50px;
    color:#0E76A8;
    font-weight:bold;
    text-align:center;
}

.sub-title{
    font-size:24px;
    text-align:center;
    color:gray;
    margin-bottom:25px;
}

.stTextArea textarea{
    font-size:20px !important;
}

.stButton>button{
    width:100%;
    height:60px;
    font-size:22px;
    font-weight:bold;
    border-radius:10px;
}

.result-card{
    background:#F5F7FA;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

.card-title{
    font-size:22px;
    font-weight:bold;
    color:#0E76A8;
}

.card-value{
    font-size:24px;
    color:#222;
}

.resolution-box{
    background:#E8F4FD;
    padding:20px;
    border-radius:12px;
    font-size:20px;
    color:black;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("🤖 Agentic AI")

st.sidebar.success("Placement Ready Project")

st.sidebar.markdown("""
### Features

✅ Incident Classification

✅ Priority Prediction

✅ Knowledge Base Search

✅ RAG

✅ Agentic AI Workflow

✅ Assignment Prediction

✅ Resolution Recommendation

""")

# ----------------------------
# Header
# ----------------------------
st.markdown(
    "<div class='main-title'>🤖 Agentic AI Service Desk</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>AI Powered IT Incident Management System</div>",
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# Input
# ----------------------------
incident = st.text_area(
    "Describe your IT Incident",
    placeholder="Example: VPN is not connecting to office network...",
    height=180
)

# ----------------------------
# Analyze Button
# ----------------------------
if st.button("🚀 Analyze Incident"):

    if incident.strip() == "":
        st.error("Please enter an incident description.")
        st.stop()

    state = {
        "incident": incident,
        "category": "",
        "priority": "",
        "resolution": "",
        "assignment_group": ""
    }

    with st.spinner("🤖 AI Agents are analyzing your incident..."):

        state = incident_agent(state)
        state = category_agent(state)
        state = priority_agent(state)
        state = knowledge_agent(state)
        state = decision_agent(state)

    st.success("Analysis Completed Successfully!")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="result-card">
        <div class="card-title">📂 Category</div>
        <div class="card-value">{state["category"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="result-card">
        <div class="card-title">🔥 Priority</div>
        <div class="card-value">{state["priority"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="result-card">
        <div class="card-title">👨‍💻 Assignment Group</div>
        <div class="card-value">{state["assignment_group"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("🛠 Suggested Resolution")

    st.markdown(f"""
    <div class="resolution-box">
    {state["resolution"]}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📋 Incident Summary")

    st.write("### Incident")
    st.write(state["incident"])

    st.write("### Predicted Category")
    st.success(state["category"])

    st.write("### Predicted Priority")
    st.warning(state["priority"])

    st.write("### Assignment Group")
    st.info(state["assignment_group"])

    st.write("### Suggested Resolution")
    st.success(state["resolution"])

    st.divider()

    if st.button("🎫 Create ServiceNow Ticket"):

        st.balloons()

        st.success("ServiceNow Ticket Created Successfully! (Demo)")

# ----------------------------
# Footer
# ----------------------------
st.divider()

st.markdown(
    "<center><h4>Built with ❤️ using Streamlit | LangGraph | Machine Learning | FAISS | Sentence Transformers</h4></center>",
    unsafe_allow_html=True
)