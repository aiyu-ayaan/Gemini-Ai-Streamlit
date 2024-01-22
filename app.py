import streamlit as st

from database.Session import SessionDatabase, Messages, Role
from utils.Utils import formate_time

session_db = SessionDatabase()
recent_session = session_db.get_recent_session()

st.set_page_config(page_title='Tutor Talk', page_icon=':shark:', layout='wide')

main_container = st.container()


def populate_messages(current_session):
    state = st.session_state['current_session'] = current_session

    if st.session_state['current_session'] is None:
        st.error('Please create a new chat session.')
        return
    for me in state.get_messages():
        message, role, created_at = me.get_message()
        if message == '' or message is None:
            continue
        if role == Role.BOT:
            main_container.subheader('Bot 🤖 : ')
            main_container.markdown(body=message)
        else:
            main_container.subheader('You 👤 : ')
            main_container.markdown(body=message)


def create_new_session():
    global recent_session  # This is a global variable
    recent_session = session_db.create_new_session()


def create_new_session_enabled():
    st.session_state['isEnable'] = len(recent_session.get_messages()) > 0


# Sidebar
with st.sidebar:
    create_new_session_enabled()
    st.button('Create New Chat', on_click=create_new_session, disabled=not st.session_state['isEnable'])
    with st.expander(expanded=True, label='Chat History'):
        for session in reversed(session_db.get_sessions()):
            st.button(f'Session ID: {formate_time(session.created_at)}', id(session.session_id),
                      on_click=populate_messages, args=(session,))

# Main Container
prompt = st.chat_input('Ask me anything!')

with main_container:
    recent_session.add_message(Messages(message=prompt, role=Role.USER))
    main_container.title('💬 Chatbot')
    main_container.caption('An chatbot based on Gemini Ai.')
    if prompt:
        create_new_session_enabled()
        populate_messages(recent_session)

#  if length > 1:
#         st.error('Please ask one question at a time.')
#     else:
#         st.success('Question received.')
#         st.balloons()
