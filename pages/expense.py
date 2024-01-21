import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


st.title('Logged IN')
st.write(st.session_state['person_url'])
st.write("Hi", st.session_state['userid'])