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
    DAY_05 = "day_05"
    DAY_06 = "day_06"
    DAY_07 = "day_07"
    DAY_08 = "day_08"
    DAY_09 = "day_09"
    DAY_10 = "day_10"
    DAY_11 = "day_11"
    DAY_12 = "day_12"
    DAY_13 = "day_13"
    DAY_14 = "day_14"
    DAY_15 = "day_15"
    DAY_16 = "day_16"
    DAY_17 = "day_17"
    DAY_18 = "day_18"
    DAY_19 = "day_19"
    DAY_20 = "day_20"
    DAY_21 = "day_21"
    DAY_22 = "day_22"
    DAY_23 = "day_23"
    DAY_24 = "day_24"
    DAY_25 = "day_25"
    # [[[end]]] (checksum: 04b39e2f173693b4e01bbb7a22291090)


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


def list_to_days(days: list[DayType]) -> list[str]:
    if not days:
        return [p.name.replace(".py", "") for p in list(Path("./src").glob("day_*.py"))]
    return [d.value for d in days]


@app.command()
def benchmark(iterations: int = 10, days: list[DayType] = []) -> None:
    table = Table(title=f"AOC 2023 - Timings\n({iterations:,} iterations)")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")

    day_names = list_to_days(days)

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(day_names) * 2) * iterations)
        for day in sorted(day_names):
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
        part_1 = module.part_1(input_str)  # type: ignore[unresolved-attribute]
        progress()

        part_2 = module.part_2(input_str)  # type: ignore[unresolved-attribute]
        progress()

    return part_1, part_2


@app.command()
def answers(days: list[DayType] = []) -> None:
    table = Table(title="Advent of Code 2023 - Answers")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")

    day_names = list_to_days(days)

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(day_names) * 2))
        for day in sorted(day_names):
            p1, p2 = run_day(day, lambda: progress.update(task, advance=1))

            table.add_row(f"{int(day.split("_")[1])}", f"{p1}", f"{p2}")

    with Console() as console:
        console.print(table)


if __name__ == "__main__":
    app()
