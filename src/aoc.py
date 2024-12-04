import contextlib
from collections.abc import Callable
from cProfile import Profile
from enum import Enum
from importlib import import_module
from pathlib import Path
from pstats import Stats
from statistics import mean
from time import time
from typing import Any

import typer
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from utils import read_input

app = typer.Typer()


class DayType(str, Enum):
    # [[[cog
    # import cog
    # from pathlib import Path
    # for day in sorted([p.name.replace(".py", "") for p in list(Path("./src").glob("day_*.py"))]):
    #    cog.outl(f'{day.upper()} = "{day}"')
    # ]]]
    DAY_01 = "day_01"
    DAY_02 = "day_02"
    DAY_03 = "day_03"
    DAY_04 = "day_04"
    # [[[end]]] (checksum: 140cd596aea2fec3798dca87fec2ec1d)


class SortType(str, Enum):
    CALLS = "calls"
    CUMULATIVE = "cumulative"
    FILENAME = "filename"
    LINE = "line"
    NAME = "name"
    NFL = "nfl"
    PCALLS = "pcalls"
    STDNAME = "stdname"
    TIME = "time"


class PartType(str, Enum):
    PART_1 = "part_1"
    PART_2 = "part_2"


def time_it(day: str, iterations: int = 1, progress: Callable[..., Any] = lambda: None) -> tuple[float, float]:
    module = import_module(day)
    input_str = read_input(day)

    times: dict[int, list[float]] = {}

    for i in [1, 2]:
        times[i] = []
        for _ in range(iterations):
            start = time()
            with contextlib.suppress(Exception):
                getattr(module, f"part_{i}")(input_str)
            times[i].append(time() - start)
            progress()

    return mean(times[1]), mean(times[2])


@app.command()
def benchmark(iterations: int = 10, days: list[str] = []) -> None:
    table = Table(title=f"AOC 2023 - Timings\n({iterations:,} iterations)")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")

    if not days:
        _days = [p.name.replace(".py", "") for p in list(Path("./src").glob("day_*.py"))]
    else:
        _days = [str(d) for d in days]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(_days) * 2) * iterations)
        for day in sorted(_days):
            p1, p2 = time_it(day, iterations, lambda: progress.update(task, advance=1))

            _, d = day.split("_")
            table.add_row(f"{int(d)}", f"{p1:.4f}s", f"{p2:.4f}s")

    with Console() as console:
        console.print(table)


@app.command()
def profile(day: DayType, part: PartType, sort: SortType = SortType.CALLS) -> None:
    module = import_module(day)
    input_str = read_input(day)

    with Profile() as profile:
        getattr(module, part)(input_str)
        Stats(profile).strip_dirs().sort_stats(sort).print_stats()


def run_day(day: str, progress: Callable[..., Any] = lambda: None) -> tuple[float, float]:
    module = import_module(day)
    input_str = read_input(day)

    part_1 = 0
    part_2 = 0
    with contextlib.suppress(Exception):
        part_1 = module.part_1(input_str)
        progress()

        part_2 = module.part_2(input_str)
        progress()

    return part_1, part_2


def day_from_name(file_name: str) -> int:
    return int(file_name.replace(".py", "").replace("day_", ""))


@app.command()
def answers(days: list[int] = []) -> None:
    table = Table(title="Advent of Code 2023 - Answers")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="left")
    table.add_column("Part 2", justify="left")

    if not days:
        days = [day_from_name(p.name) for p in list(Path("./src").glob("day_*.py"))]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(days) * 2))
        for d in sorted(days):
            p1, p2 = run_day(f"day_{d:02}", lambda: progress.update(task, advance=1))

            table.add_row(f"{int(d)}", f"{p1}", f"{p2}")

    with Console() as console:
        console.print(table)


if __name__ == "__main__":
    app()
