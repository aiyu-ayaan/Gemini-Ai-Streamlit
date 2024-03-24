import streamlit as st

from components.IconButton import icon_button, open_page
from database.Repository import get_value_from_state, State, create_or_update_session, ChatRepositoryImp
from database.Session import Role, Message
from gemini.Gemini import Gemini

st.set_page_config(page_title='Tutor Talk', page_icon='🤖:', layout='wide')

main_container = st.container()
side_bar = st.sidebar
database: ChatRepositoryImp = create_or_update_session(
    State.CHAT_REPOSITORY.value,
    init_value=ChatRepositoryImp()
)

gemini: Gemini = create_or_update_session(
    State.GEMINI.value,
    init_value=Gemini()
)


def about_section():
    with st.expander("About", expanded=True):
        st.title('🤖 Chatbot')
        st.write('Welcome to Tutor Talk')
        st.caption('by Ayaan')
        icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com'], key='app-code')
        st.button('➕ New Chat', key='new-chat', on_click=database.create_new_session)


# def dev_section():
#     with st.expander('Know about developer'):
#         # col1 = st.columns(1)
#         # with col1:
#         #     with st.container(border=True):
#         #         st.image('img/female.png', width=80)
#         #         st.subheader('Shakya')
#         #         st.write('Role: Gussa Karna')
#         #         icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com/'], key='shakya')
#         # with col1:
#         with st.container(border=True):
#             st.image('img/male.png', width=80)
#             st.subheader('Ayaan')
#             st.write('Role: Gussa jhelna')
#             icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com/aiyu-ayaan'], key='ayaan')


def populate_messages(session_id: int):
    database.get_current_session(session_id)
    gemini.start_new_chat(database.get_current().get_messages())


def his_section():
    with st.expander('History', expanded=True):
        st.subheader('All history')
        for session in reversed(get_value_from_state(State.SESSION_LIST_STATE.value)):
            st.button(session.get_session_name(), key=session.get_session_id,
                      on_click=populate_messages, args=[session.get_session_id()])


with side_bar:
    about_section()
    # dev_section()
    his_section()


def message_container(message: Message):
    if message.get_role() == Role.MODEL:
        with st.container():
            st.caption('Model 🤖')
            st.markdown(message.get_content(), unsafe_allow_html=True)
    else:
        with st.container():
            st.caption('User 👨‍💻')
            st.markdown(message.get_content(), unsafe_allow_html=True)


prompt = st.chat_input('Ask me anything!')
with main_container:
    st.title('🤖 Chatbot')
    st.caption('An chatbot based on Gemini Ai.')
    if prompt:
        database.add_message(message=prompt, role=Role.USER)
        response = gemini.send_message(prompt, Role.USER)
        database.add_message(response.get_content(), Role.MODEL)
    for i in database.get_current().get_messages():
        message_container(i)
