from tabulate import tabulate, TableFormat, Line

thick_line = TableFormat(
    lineabove=Line("╔", "═", "╤", "╗"),
    linebelowheader=Line("╟", "─", "┼", "╢"),
    linebetweenrows=None,
    linebelow=Line("╚", "═", "╧", "╝"),
    headerrow="║ {header} ║",
    datarow="║ {data} ║",
    padding=1,  # Adds padding to each cell
)