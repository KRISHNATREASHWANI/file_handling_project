"""
File Manager Pro — Streamlit Edition
-------------------------------------
Same Create / Read / Update / Delete file logic, presented as a
clean Streamlit web app.

Run:
    pip install streamlit
    streamlit run file_manager_streamlit.py
"""

from pathlib import Path
from datetime import datetime
import streamlit as st


# ---------------------------------------------------------------------------
# Core file operations (unchanged behavior from the original script)
# ---------------------------------------------------------------------------
def op_create(name, content):
    path = Path(name)
    if path.exists():
        return False, f'"{name}" already exists.'
    path.write_text(content, encoding="utf-8")
    return True, f'"{name}" created successfully.'


def op_read(name):
    path = Path(name)
    if not path.exists():
        return False, f'"{name}" does not exist.'
    return True, path.read_text(encoding="utf-8")


def op_rename(name, new_name):
    path, new_path = Path(name), Path(new_name)
    if not path.exists():
        return False, f'"{name}" does not exist.'
    if new_path.exists():
        return False, f'"{new_name}" already exists.'
    path.rename(new_path)
    return True, f'Renamed "{name}" to "{new_name}".'


def op_append(name, content):
    path = Path(name)
    if not path.exists():
        return False, f'"{name}" does not exist.'
    with open(path, "a", encoding="utf-8") as fs:
        fs.write("\n" + content)
    return True, f'Content appended to "{name}".'


def op_overwrite(name, content):
    path = Path(name)
    if not path.exists():
        return False, f'"{name}" does not exist.'
    path.write_text(content, encoding="utf-8")
    return True, f'"{name}" overwritten successfully.'


def op_delete(name):
    path = Path(name)
    if not path.exists():
        return False, f'"{name}" does not exist.'
    path.unlink()
    return True, f'"{name}" deleted successfully.'


# ---------------------------------------------------------------------------
# Page config + styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="File Manager Pro",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #f4f6fb; }
    section[data-testid="stSidebar"] {
        background-color: #1e2130;
    }
    section[data-testid="stSidebar"] * { color: #d7d9f0 !important; }
    section[data-testid="stSidebar"] .stRadio label { font-size: 15px; padding: 6px 0; }

    div.block-container { padding-top: 2.2rem; max-width: 720px; }

    .card {
        background: #ffffff;
        padding: 28px 32px;
        border-radius: 14px;
        box-shadow: 0 2px 14px rgba(30, 33, 48, 0.06);
        margin-bottom: 18px;
    }
    .card h2 { margin-top: 0; margin-bottom: 2px; }
    .card p.sub { color: #6b7280; margin-top: 0; margin-bottom: 22px; font-size: 14px; }

    div.stButton > button {
        background-color: #5b6cf9;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.55em 1.4em;
        font-weight: 600;
    }
    div.stButton > button:hover { background-color: #4453d6; color: white; }

    .danger-btn button {
        background-color: #d84343 !important;
    }
    .danger-btn button:hover { background-color: #b83636 !important; }

    .log-entry-ok { color: #1f9d55; font-family: monospace; font-size: 13px; }
    .log-entry-err { color: #d84343; font-family: monospace; font-size: 13px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "log" not in st.session_state:
    st.session_state.log = []


def write_log(message, ok=True):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.log.insert(0, (ts, ok, message))
    st.session_state.log = st.session_state.log[:8]


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📁 File Manager")
    st.caption("Pro Edition")
    st.markdown("---")
    page = st.radio(
        "Choose an operation",
        ["📝 Create", "📖 Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )


# ---------------------------------------------------------------------------
# Main panels
# ---------------------------------------------------------------------------
if page == "📝 Create":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Create a New File")
    st.markdown('<p class="sub">Choose a name and starting content.</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt")
    content = st.text_area("Content", height=140, placeholder="Type the starting content...")
    if st.button("Create File"):
        if not name.strip():
            st.warning("Please enter a file name.")
        else:
            ok, msg = op_create(name.strip(), content)
            write_log(msg, ok)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📖 Read":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Read a File")
    st.markdown('<p class="sub">View the contents of an existing file.</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt")
    if st.button("Read File"):
        ok, msg = op_read(name.strip())
        if ok:
            st.text_area("Contents", value=msg, height=180)
            write_log(f'"{name}" loaded.', True)
        else:
            write_log(msg, False)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "✏️ Update":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Update a File")
    st.markdown('<p class="sub">Rename, append to, or overwrite a file.</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt")
    mode = st.radio("Action", ["Rename", "Append", "Overwrite"], horizontal=True)
    value_label = "New file name" if mode == "Rename" else "Content"
    value = st.text_area(value_label, height=100) if mode != "Rename" else st.text_input(value_label)
    if st.button("Apply Update"):
        if mode == "Rename":
            ok, msg = op_rename(name.strip(), value.strip())
        elif mode == "Append":
            ok, msg = op_append(name.strip(), value)
        else:
            ok, msg = op_overwrite(name.strip(), value)
        write_log(msg, ok)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🗑️ Delete":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Delete a File")
    st.markdown('<p class="sub">This action cannot be undone.</p>', unsafe_allow_html=True)
    name = st.text_input("File name", placeholder="notes.txt")
    confirm = st.checkbox("I understand this cannot be undone")
    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    if st.button("Delete File", disabled=not confirm):
        ok, msg = op_delete(name.strip())
        write_log(msg, ok)
    st.markdown("</div></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Activity log
# ---------------------------------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("##### Activity Log")
if not st.session_state.log:
    st.caption("No actions yet.")
else:
    for ts, ok, msg in st.session_state.log:
        icon = "✔" if ok else "✘"
        cls = "log-entry-ok" if ok else "log-entry-err"
        st.markdown(f'<div class="{cls}">[{ts}] {icon} {msg}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)