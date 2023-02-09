import os

from visidata import vd, Sheet, VisiData, FreqTableSheet, BaseSheet, asyncthread, CellColorizer

vd.options.disp_menu_fmt = '|  VisiData {vd.version} | {vd.motd}'

# HTML("<html>...") and JSON('{"k":"v"...}')
@VisiData.lazy_property
def utf8_parser(vd):
    from lxml import etree
    return etree.HTMLParser(encoding='utf-8')

@VisiData.api
def HTML(vd, s):
    import lxml.html
    return lxml.html.etree.fromstring(s, parser=vd.utf8_parser)

@VisiData.api
def JSON(vd, s):
    import json
    return json.loads(s)


@Sheet.api
@asyncthread
def select_equal_selected(sheet, col):
    selectedVals = set(col.getDisplayValue(row) for row in Progress(sheet.selectedRows))
    sheet.select(sheet.gatherBy(lambda r,c=col,vals=selectedVals: c.getDisplayValue(r) in vals), progress=False)


Sheet.addCommand('', 'addcol-source', 'source.addColumn(copy(cursorCol))', 'add copy of current column to source sheet')  #988  frosencrantz

Sheet.addCommand('', 'clean-names', '''
options.clean_names = True;
for c in visibleCols:
    c.name = c.name
''', 'set options.clean_names on sheet and clean visible column names')

Sheet.addCommand('', 'select-equal-selected', 'select_equal_selected(cursorCol)', 'select rows with values in current column in already selected rows')



@VisiData.api
def ansi(*args):
    os.write(1, b'\x1b'+b''.join([x.encode('utf-8') for x in args]))


@VisiData.api
def set_titlebar(vd,title):
    ansi(']2;', title, '\x07')


vd.option('color_current_cell', '', 'color of current cell, if different from color_current_row+color_current_col')
Sheet.colorizers += [
    CellColorizer(3, 'color_current_cell', lambda s,c,r,v: c is s.cursorCol and r is s.cursorRow)
]