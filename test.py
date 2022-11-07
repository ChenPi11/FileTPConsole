from rich.progress import Progress
import time
import rich.text
import rich.columns
import random
from filetp_color import *
#rich.columns.Columns()
with Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    TimeElapsedColumn(),
    console=console,
    transient=False,
) as progress:

    task1 = progress.add_task("[red]Downloading", total=1000)
    task2 = progress.add_task("[green]Processing", total=1000)
    task3 = progress.add_task("[yellow]Thinking", total=None)

    while not progress.finished:
        #progress.update(task1, advance=0.5)
        progress.update(task1, completed=500,total=1000)
        progress.update(task2, advance=0.3)
        time.sleep(0.01)
        if random.randint(0, 100) < 1:
            progress.log("1")