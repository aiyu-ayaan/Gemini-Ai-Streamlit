import streamlit as st

from components.IconButton import icon_button, open_page
from database.Session import Database, Role, get_session, State, Message

st.set_page_config(page_title='Tutor Talk', page_icon='🤖:', layout='wide')

main_container = st.container()
side_bar = st.sidebar

db = Database()


def about_section():
    with st.expander("About", expanded=True):
        st.title('🤖 Chatbot')
        st.write('Welcome to Tutor Talk')
        icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com'], key='app-code')


def dev_section():
    with st.expander('Know about developer'):
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.image('img/female.png', width=80)
                st.subheader('Shakya')
                st.write('Role: Gussa Karna')
                icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com/'], key='shakya')
        with col2:
            with st.container(border=True):
                st.image('img/male.png', width=80)
                st.subheader('Ayaan')
                st.write('Role: Gussa jhelna')
                icon_button(icon=r'\f35d', on_click=open_page, args=['https://www.github.com/aiyu-ayaan'], key='ayaan')


def his_section():
    with st.expander('History', expanded=True):
        st.subheader('All history')
        with st.container(border=True):
            st.write('No history yet')


with side_bar:
    about_section()
    dev_section()
    his_section()


def message_container(message: Message):
    if message.get_role() == Role.BOT:
        with st.container():
            st.subheader('🤖')
            st.markdown(message.get_content(), unsafe_allow_html=True)
    else:
        with st.container():
            st.subheader('👤')
            st.markdown(message.get_content(), unsafe_allow_html=True)


prompt = st.chat_input('Ask me anything!')
with main_container:
    st.title('🤖 Chatbot')
    st.caption('An chatbot based on Gemini Ai.')
    if prompt:
        db.add_message(prompt, Role.USER)
        for i in get_session(State.MESSAGES.value):
            message_container(i)
