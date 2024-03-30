"""
This module is the main entry point for the Streamlit app. It contains the main logic for the Streamlit app.

Note:
    The module imports the necessary classes and functions from the project package.


"""
import asyncio

from Main import *
from database.Repository import ChatRepositoryImp, create_or_update_session
from export.MarkdownToPdf import Export
from gemini.Gemini import Gemini

if __name__ == '__main__':
    # Get a random emoji from the Emoji class
    emoji = Emoji().get_random_emoji()

    # Set the Streamlit app configuration
    st.set_page_config(page_title='Tutor Talk', page_icon=f'{emoji}', layout='wide')

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

    # Render the CSS styles
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Create a main container and sidebar
    main_container = st.container()
    side_bar = st.sidebar

    # Render the sidebar sections
    with side_bar:
        about_section(main_container, database, export)
        his_section(database, gemini)
        acknowledgements_sec()

    # Get the user's prompt
    prompt = st.chat_input('Ask me anything!')

    # Render the main container
    with main_container:
        st.title(f'{emoji} Chatbot')
        st.caption('A chatbot based on Gemini Ai.')

        # Display the chat messages
        for i in database.get_current().get_messages():
            print(i.get_role())
            message_container(i)

        # Process the user's prompt
        if prompt:
            with st.spinner('Thinking...'):
                asyncio.run(process_message(prompt, database, gemini))
