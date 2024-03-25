import streamlit as st

from database.Emoji import Emoji
from database.Repository import create_or_update_session, State
from gemini.Gemini import Gemini
from utils.Utils import is_valid_url

emoji = Emoji().get_random_emoji()
st.set_page_config(page_title='Tutor Talk', page_icon=f'{emoji}', layout='wide')

gemini: Gemini = create_or_update_session(
    State.GEMINI.value,
    init_value=Gemini()
)

summary_markdown = create_or_update_session(
    State.SUMMARY_MARKDOWN.value,
    ''
)

side_bar = st.sidebar
main_container = st.container()


def summarize(page_url: str):
    if len(page_url) == 0:
        st.warning('Please enter a valid URL')
        return
    if not is_valid_url(url):
        st.warning('Please enter a valid URL')
        return
    with st.spinner('Summarizing'):
        create_or_update_session(
            State.SUMMARY_MARKDOWN.value,
            updated_value=gemini.summaries(page_url).data
        )


with side_bar:
    url = st.text_input('Enter URL here', key='text')
    st.button('Summarize', key='summarize', on_click=summarize, args=(url,))

with main_container:
    st.title(f'Summarize URL {emoji}')
    st.markdown(summary_markdown)
