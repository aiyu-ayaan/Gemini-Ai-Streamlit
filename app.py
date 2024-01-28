import streamlit as st

from database.Session import SessionDatabase, Messages, Role
from utils.Utils import formate_time, States

session_db = SessionDatabase()
recent_session = session_db.create_new_session() if States.CURRENT_SESSION not in st.session_state or st.session_state[
    States.CURRENT_SESSION] is None else st.session_state[
    States.CURRENT_SESSION]

st.set_page_config(page_title='Tutor Talk', page_icon=':shark:', layout='wide')

main_container = st.container()
for session in session_db.get_sessions():
    print(session.session_id)


def populate_messages(current_session=None):
    if current_session is None:
        state = st.session_state[States.CURRENT_SESSION] = recent_session
    else:
        state = st.session_state[States.CURRENT_SESSION]
    for me in state.get_messages():
        message, role, created_at = me.get_message()

        if message == '' or message is None:
            continue

        if role == Role.BOT:
            with main_container:
                st.subheader('Bot 🤖 : ')
                st.markdown(body=message)
        else:
            with main_container:
                st.subheader('You 👤 : ')
                st.markdown(body=message)


def is_expandable():
    st.session_state[States.IS_CHAT_HISTORY_EXPANDABLE] = len(session_db.get_sessions()) > 1


def create_new_session():
    st.session_state[States.CURRENT_SESSION] = session_db.create_new_session()
    is_expandable()


def create_new_session_enabled():
    st.session_state[States.IS_CREATE_NEW_SESSION_ENABLED] = len(recent_session.get_messages()) > 0


# Sidebar
with st.sidebar:
    is_expandable()
    create_new_session_enabled()
    st.button('Create New Chat', on_click=create_new_session,
              disabled=not st.session_state[States.IS_CREATE_NEW_SESSION_ENABLED])
    with st.expander(expanded=st.session_state[States.IS_CHAT_HISTORY_EXPANDABLE], label='Chat History'):
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
        populate_messages()

#  if length > 1:
#         st.error('Please ask one question at a time.')
#     else:
#         st.success('Question received.')
#         st.balloons()
