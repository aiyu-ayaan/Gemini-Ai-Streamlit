import copy
import threading

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

from database.Emoji import Emoji
from database.Repository import get_value_from_state, State, ChatRepositoryImp
from database.Session import Role, Message, convert_to_markdown
from database.utils import Links
from export.MarkdownToPdf import Export
from gemini import Gemini

emoji = Emoji().get_random_emoji()


def about_section(container: st.container, database: ChatRepositoryImp, export: Export):
    """Function to create the about section.
    
    Args:
        container (st.container): Parent Container or where the content will be displayed.
        database (ChatRepositoryImp): Chat Repository object
        export (Export): Export object
    """
    with st.expander("About", expanded=True) as e:
        st.title('Chatbot')
        st.write('Welcome to Tutor Talk')
        st.button('➕ New Chat', key='new-chat', on_click=database.create_new_session, use_container_width=True,
                  disabled=len(database.get_current().get_messages()) == 0
                  )
        st.button('Export to PDF', key='export-pdf', use_container_width=True,
                  on_click=export.export_to_pdf,
                  args=[convert_to_markdown(copy.deepcopy(database.get_current())), container,
                        copy.deepcopy(database.get_current()).get_session_name() + '.pdf'],
                  disabled=len(database.get_current().get_messages()) == 0
                  )


def message_container(message: Message):
    """Function to create a message container.

    Args:
        message (Message): Message object
    """
    if message.get_role() == Role.MODEL:
        with st.chat_message('AI'):
            st.markdown(message.get_content(), unsafe_allow_html=True)
    else:
        with st.chat_message('User'):
            st.markdown(message.get_content(), unsafe_allow_html=True)
    # else:
    #     st.error('Unknown Role')
    #     st.caption('Message set to empty due to an unknown role.')
    #     current_session = database.get_current()
    #     current_session.update_message([])


def populate_messages(session_id: int, database: ChatRepositoryImp, gemini: Gemini):
    """Function to populate the messages.
    
    Args:
        session_id (int): Current session id
        database (ChatRepositoryImp): Database object
        gemini (Gemini): Gemini object
    """
    database.get_current_session(session_id)
    gemini.start_new_chat(database.get_current().get_messages())


def his_section(database: ChatRepositoryImp, gemini: Gemini):
    """Function to create the history section.

    Args:
        database (ChatRepositoryImp): Chat Repository object.
        gemini (Gemini): Gemini object.
    """
    with st.expander('History', expanded=True):
        st.subheader('All history')
        for session in reversed(get_value_from_state(State.SESSION_LIST_STATE.value)):
            st.button(session.get_session_name(), key=session.get_session_id,
                      on_click=populate_messages, args=[session.get_session_id(), database, gemini, ])


def acknowledgements_sec():
    """Acknowledgements section.
    """
    with st.expander('Acknowledgements', expanded=False):
        st.link_button('Source Code', url=Links.GITHUB.value, use_container_width=True)
        with st.container(border=True):
            st.image('src/project/img/male.png', width=80)
            st.subheader('Ayaan', divider=True)
            st.link_button('Github', url=Links.AYAAN.value, use_container_width=True)
        with st.container():
            st.caption('This project is made using:')
            st.link_button('Streamlit', url=Links.STREAMLIT.value, use_container_width=True)
            st.link_button('Python', url=Links.PYTHON.value, use_container_width=True)
            st.link_button('Gemini Ai', url=Links.GEMINI.value, use_container_width=True)
            st.link_button('MdPdf', url=Links.MD_PDF.value, use_container_width=True)


def progress_message_in_other_thread(input_message: str, database: ChatRepositoryImp, gemini: Gemini):
    """ Function to process the message in another thread.

    Args:
        input_message (str): Input from user.
        database (ChatRepositoryImp): Chat Repository object.
        gemini (Gemini): Gemini object.
    """
    response = gemini.send_message(input_message, Role.USER)
    database.add_message(response.get_content(), Role.MODEL)


@st.cache_data()
def thinking(input_message: str, _database: ChatRepositoryImp, _gemini: Gemini):
    """Function to process the message in an async manner.
    
    Args:
        input_message (str): Input from user.
        _database (ChatRepositoryImp): Chat Repository object.
        _gemini (Gemini): Gemini object.
    """

    thread = threading.Thread(target=progress_message_in_other_thread, args=(input_message, _database, _gemini))
    add_script_run_ctx(thread)
    thread.start()
    thread.join()
    st.rerun()
