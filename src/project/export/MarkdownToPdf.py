import os
import subprocess

import streamlit as st


class Export:
    """Export is a class that contains methods to export content to different formats.
    Initially, it supports exporting content to PDF.
    """

    @staticmethod
    def export_to_pdf(content: str, container: st.container = None, name: str = 'export.pdf'):
        """Exports the given content to PDF.
        
        Args:
            content (str): Markdown content to export.
            container (st.container, optional): Parent container to display the download button. Defaults to None.
            name (str, optional): Name of the PDF file. Defaults to 'export.pdf'.
        """
        with open('./src/project/export/mktopdf.md', 'w', encoding='utf-8') as f:
            f.write(content)
        command = ["mdpdf", "-o", "./src/project/export/export.pdf", "./src/project/export/mktopdf.md"]
        try:
            subprocess.run(command, check=True)
            if container is not None:
                container.success("PDF created successfully")
                with open('./src/project/export/export.pdf', 'rb') as f:
                    container.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=name,
                        mime='application/pdf'
                    )
                os.remove('./src/project/export/mktopdf.md')
                os.remove('./src/project/export/export.pdf')
        except subprocess.CalledProcessError as e:
            if container is not None:
                container.error("An error occurred while creating PDF")
                container.error(e)
