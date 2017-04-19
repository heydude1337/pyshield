# -*- coding: utf-8 -*-
tbl = result[1]
tbl = tbl.round({'Dose [mSv]': 2, 'Dose corrected for occupancy [mSv]': 2})


tbl['point name'] = tbl.index

tbl.sort(columns = 'point name')
title = 'Pyshield Report'
file_name = 'report.pdf'
from reportlab.lib import colors
from reportlab.lib.pagesizes import  A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.pdfgen import canvas
doc = SimpleDocTemplate("simple_table.pdf", pagesize=A4)
elements = []

#c = canvas.canvas(file_name, pagesize = A4)

#c = c.drawString(100, 100, title)


list_tbl = [tbl.columns[:,].values.astype(str).tolist()] + tbl.values.tolist()

pdf_tbl = Table(list_tbl)

elements.append(pdf_tbl)

doc.build(elements)
