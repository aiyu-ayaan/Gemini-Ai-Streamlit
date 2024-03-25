import subprocess

import streamlit as st


class Export:
    @staticmethod
    def export_to_pdf(content: str, container: st.container = None, name: str = 'output.pdf'):
        with open('./output/mktopdf.md', 'w', encoding='utf-8') as f:
            f.write(content)
        command = ["mdpdf", "-o", "./output/output.pdf", "./output/mktopdf.md"]
        try:
            subprocess.run(command, check=True)
            if container is not None:
                container.success("PDF created successfully")
                with open('./output/output.pdf', 'rb') as f:
                    container.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=name,
                        mime='application/pdf'
                    )
        except subprocess.CalledProcessError as e:
            if container is not None:
                container.error("An error occurred while creating PDF")
                container.error(e)
