from tabulate import tabulate, TableFormat, Line, DataRow

thick_line = TableFormat(
    lineabove=Line("╔", "═", "╤", "╗"),
    linebelowheader=Line("╟", "─", "┼", "╢"),
    linebetweenrows=None,
    linebelow=Line("╚", "═", "╧", "╝"),
    headerrow=DataRow("║", "│", "║"),
    datarow=DataRow("║", "│", "║"),
    padding=1,
    with_header_hide=None
)