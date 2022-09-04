import io
from importlib.resources import open_binary

import docx

from app import resorces


async def get_file(starting_point: str, end_point: str, date: str) -> io.BytesIO:
    document = open_binary(resorces, 'dad_info.docx')
    output = io.BytesIO()
    output.name = 'file_dad.docx'
    doc = docx.Document(document)
    doc.paragraphs[-2].text = f'Путевой: б/н        от {date}'
    doc.paragraphs[-1].text = 'Маршрут                 '
    doc.paragraphs[-1].add_run(f'{starting_point.title()}-{end_point.title()}').bold = True
    doc.save(output)
    return output