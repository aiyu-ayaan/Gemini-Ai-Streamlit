import asyncio

import streamlit as st

from database.Emoji import Emoji
from database.Repository import get_value_from_state, State, create_or_update_session, ChatRepositoryImp
from database.Session import Role, Message
from gemini.Gemini import Gemini
from output.MarkdownToPdf import Export
from utils.Utils import Links

emoji = Emoji().get_random_emoji()
st.set_page_config(page_title='Tutor Talk', page_icon=f'{emoji}', layout='wide')

hide_streamlit_style = '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-1y0tads {padding-top: 0rem;}
.stDeployButton {
            visibility: hidden;
        }
[data-testid="stStatusWidget"] {
    visibility: hidden;
}
</style>

'''

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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

export: Export = create_or_update_session(
    State.EXPORT.value,
    init_value=Export()
)


def about_section():
    with st.expander("About", expanded=True) as e:
        st.title(f'{emoji} Chatbot')
        st.write('Welcome to Tutor Talk')
        st.button('➕ New Chat', key='new-chat', on_click=database.create_new_session, use_container_width=True,
                  disabled=len(database.get_current().get_messages()) == 0
                  )
        st.button('Export to PDF', key='export-pdf', use_container_width=True,
                  on_click=export.export_to_pdf,
                  args=[database.get_current().convert_to_markdown(), main_container,
                        database.get_current().get_session_name() + '.pdf'],
                  disabled=len(database.get_current().get_messages()) == 0
                  )


def message_container(message: Message):
    if message.get_role() == Role.MODEL:
        with st.chat_message('AI'):
            st.markdown(message.get_content(), unsafe_allow_html=True)
    else:
        with st.chat_message('User'):
            st.markdown(message.get_content(), unsafe_allow_html=True)
    # else:
    #     st.error('Unknown Role')
    #     st.caption('Message set to empty due to unknown role.')
    #     current_session = database.get_current()
    #     current_session.update_message([])


def populate_messages(session_id: int):
    database.get_current_session(session_id)
    gemini.start_new_chat(database.get_current().get_messages())
    # with main_container:
    #     for i in database.get_current().get_messages():
    #         message_container(i)


def his_section():
    with st.expander('History', expanded=True):
        st.subheader('All history')
        for session in reversed(get_value_from_state(State.SESSION_LIST_STATE.value)):
            st.button(session.get_session_name(), key=session.get_session_id,
                      on_click=populate_messages, args=[session.get_session_id()])


def acknowledgements_sec():
    with st.expander('Acknowledgements', expanded=False):
        st.link_button('Source Code', url=Links.GITHUB.value, use_container_width=True)
        with st.container(border=True):
            st.image('src/img/male.png', width=80)
            st.subheader('Ayaan', divider=True)
            st.link_button('Github', url=Links.AYAAN.value, use_container_width=True)
        with st.container():
            st.caption('This project is made using:')
            st.link_button('Streamlit', url=Links.STREAMLIT.value, use_container_width=True)
            st.link_button('Python', url=Links.PYTHON.value, use_container_width=True)
            st.link_button('Gemini Ai', url=Links.GEMINI.value, use_container_width=True)


with side_bar:
    about_section()
    his_section()
    acknowledgements_sec()

prompt = st.chat_input('Ask me anything!')


async def process_message(input_message: str):
    database.add_message(message=input_message, role=Role.USER)
    response = await gemini.send_message(input_message, Role.USER)
    database.add_message(response.get_content(), Role.MODEL)
    st.rerun()


with main_container:
    st.title(f'{emoji} Chatbot')
    st.caption('An chatbot based on Gemini Ai.')
    for i in database.get_current().get_messages():
        message_container(i)
    if prompt:
        with st.spinner('Thinking...'):
            asyncio.run(process_message(prompt))
