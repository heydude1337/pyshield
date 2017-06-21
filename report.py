# -*- coding: utf-8 -*-
from pyshield import CONST
from reportlab.lib import colors
from reportlab.lib.pagesizes import  A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Image, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.lib.utils import ImageReader
from io import BytesIO
import re


def naturallysorted(L, reverse=False):
  """ Similar functionality to sorted() except it does a natural text sort
  which is what humans expect when they see a filename list.
  """
  convert = lambda text: ("", int(text)) if text.isdigit() else (text, 0)
  alphanum = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  return sorted(L, key=alphanum, reverse=reverse)

def pd_to_list(pd_frame):
  lst = [pd_frame.columns[:,].values.astype(str).tolist()] + pd_frame.values.tolist()
  return lst


def make_report(file_name, calc_results, title = 'PyShield Report'):
  mpl_figs = calc_results[CONST.FIGURE]
  tbl = calc_results[CONST.SUM_TABLE]
  styles = getSampleStyleSheet()
  title = Paragraph(title, styles["Heading1"])

  # additional editing of the results
  tbl = tbl.round({'Dose [mSv]': 2, 'Dose corrected for occupancy [mSv]': 2})
  # convert to something reportlab can work with

  doc = SimpleDocTemplate(file_name, pagesize=A4)

  # convert mpl figure to something reportlab can work with
  lst_tbl = pd_to_list(tbl)
  pdf_tbl = Table(lst_tbl)
  pdf_tbl.setStyle(TableStyle(tbl_style(lst_tbl)))

  elements = [title,pdf_tbl, PageBreak()]
  if not(hasattr(mpl_figs, '__iter__')):
    mpl_figs = (fig,)
  for fig in mpl_figs.values():
    image = image_from_mpl_fig(fig)
    elements += [image, PageBreak()]

  doc.build(elements)

def image_from_mpl_fig(mpl_fig):
  image_data = BytesIO()
  mpl_fig.savefig(image_data, format = 'png', dpi = 200)
  image_data.seek(0)
  image = Image(image_data)
  image._restrictSize(*A4)
  return image


def tbl_style(tbl):
    style = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
             ('BOX', (0,0), (-1,-1), 0.25, colors.black)]


    for i, row in enumerate(tbl):
      if i > 0: # ignore headers
        if row[-1] > 0.3:
          style.append(('BACKGROUND', (0,i), (-1, i), 'red'))
        elif row[-1] > 0.1:
          style.append(('BACKGROUND', (0,i), (-1, i), 'orange'))
    return style