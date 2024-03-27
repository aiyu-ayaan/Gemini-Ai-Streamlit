import os
import subprocess

import streamlit as st


class Export:
    """
    Export is a class that contains methods to export content to different formats.
    Initially, it supports exporting content to PDF.
    """

    @staticmethod
    def export_to_pdf(content: str, container: st.container = None, name: str = 'output.pdf'):
        """
        Exports the given content to PDF.
        :param content: Markdown content to export.
        :param container: Parent container to display the download button.
        :param name: Name of the PDF file.
        """
        with open('./src/output/mktopdf.md', 'w', encoding='utf-8') as f:
            f.write(content)
        command = ["mdpdf", "-o", "./src/output/output.pdf", "./src/output/mktopdf.md"]
        try:
            subprocess.run(command, check=True)
            if container is not None:
                container.success("PDF created successfully")
                with open('./src/output/output.pdf', 'rb') as f:
                    container.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=name,
                        mime='application/pdf'
                    )
                os.remove('./src/output/mktopdf.md')
                os.remove('./src/output/output.pdf')
        except subprocess.CalledProcessError as e:
            if container is not None:
                container.error("An error occurred while creating PDF")
                container.error(e)
