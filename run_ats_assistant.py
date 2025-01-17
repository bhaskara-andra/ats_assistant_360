import os
 
current_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_folder)
streamlit_command = f"python -m streamlit run ats_compliance_tool_v1.py"
os.system(streamlit_command)