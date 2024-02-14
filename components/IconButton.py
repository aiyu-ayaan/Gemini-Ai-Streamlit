from streamlit_extras.stylable_container import stylable_container
import streamlit as st
from streamlit.components.v1 import html
import webbrowser


def icon_button(icon: str = r'\f0c1', on_click=None, args=None, key=None):
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
        unsafe_allow_html=True,
    )
    with stylable_container(
            key="container_with_border",
            css_styles=r'''
                  button div:before {
                      font-family: 'Font Awesome 5 Free';
                      ''' +
                       f'''content: "{icon}";'''
                       + r''' 
                      display: inline-block;
                      padding-right: 3px;
                      vertical-align: middle;
                      font-weight: 900;
                  }
                  ''',
    ):
        st.button("", on_click=on_click, key=key, args=args)


def open_page(url):
    webbrowser.open_new_tab(url)
