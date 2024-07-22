import subprocess
from pathlib import Path
import urllib.parse


SCRIPT_DIR = Path(__file__).parent.resolve()


def generate_example(filename, title, strip_asserts=True, insert_run_link=True):
    path_in = SCRIPT_DIR.parent / "examples" / f"{filename}.nbt"
    path_out = SCRIPT_DIR / "src" / f"example-{filename}.md"
    print(path_in)
    print(path_out)

    code = []
    with open(path_in, "r") as fin:
        for line in fin:
            if not (strip_asserts and "assert_eq" in line):
                code.append(line)

    url = f"https://numbat.dev/?q={urllib.parse.quote_plus(''.join(code))}"

    with open(path_out, "w") as fout:
        fout.write("<!-- This file is autogenerated! Do not modify it -->\n")
        fout.write("\n")
        fout.write(f"# {title}\n")
        if insert_run_link:
            fout.write(
                f'<a href="{url}"><i class="fa fa-play"></i> Run this example</a>\n'
            )
        fout.write("\n")
        fout.write("``` numbat\n")
        fout.writelines(code)
        fout.write("```\n")


generate_example("acidity", "Acidity")
generate_example("barometric_formula", "Barometric formula")
generate_example("body_mass_index", "Body mass index")
generate_example("factorial", "Factorial", strip_asserts=False)
generate_example("medication_dosage", "Medication dosage")
generate_example("molarity", "Molarity")
generate_example("musical_note_frequency", "Musical note frequency")
generate_example("paper_size", "Paper sizes")
generate_example("pipe_flow_rate", "Flow rate in a pipe")
generate_example("population_growth", "Population growth")
generate_example("recipe", "Recipe")
generate_example("voyager", "Voyager")
generate_example("xkcd_687", "XKCD 687")
generate_example("xkcd_2585", "XKCD 2585")
generate_example("xkcd_2812", "XKCD 2812")

generate_example(
    "numbat_syntax", "Syntax overview", strip_asserts=False, insert_run_link=False
)

path_units = SCRIPT_DIR / "src" / "list-units.md"
with open(path_units, "w") as f:
    print("Generating list of units...", flush=True)
    subprocess.run(
        ["cargo", "run", "--release", "--quiet", "--example=inspect", "units"],
        stdout=f,
        text=True,
    )


def list_of_functions(file_name, document):
    path = SCRIPT_DIR / "src" / f"list-functions-{file_name}.md"
    with open(path, "w") as f:
        print(f"# {document['title']}\n", file=f, flush=True)

        if introduction := document.get("introduction"):
            print(introduction + "\n", file=f, flush=True)

        sections = document["sections"]

        if len(sections) >= 3:
            links = []
            for section in sections:
                if title := section.get("title"):
                    links.append(f"[{title}](#{title.lower().replace(' ', '-')})")
            print(f"{' · '.join(links)}\n", file=f, flush=True)

        for section in sections:
            modules = section["modules"]

            if title := section.get("title"):
                print(f"## {title}\n", file=f, flush=True)

            print(f"Defined in: `{'`, `'.join(modules)}`\n", file=f, flush=True)

            for module in modules:
                print(
                    f"Generating list of functions for module '{module}'...", flush=True
                )
                subprocess.run(
                    [
                        "cargo",
                        "run",
                        "--release",
                        "--quiet",
                        "--example=inspect",
                        "--",
                        "functions",
                        module,
                    ],
                    stdout=f,
                    text=True,
                )


list_of_functions(
    "math",
    {
        "title": "Mathematical functions",
        "sections": [
            {
                "title": "Basics",
                "modules": ["core::functions"],
            },
            {
                "title": "Transcendental functions",
                "modules": ["math::transcendental"],
            },
            {
                "title": "Trigonometry",
                "modules": ["math::trigonometry"],
            },
            {
                "title": "Statistics",
                "modules": ["math::statistics"],
            },
            {
                "title": "Random sampling, distributions",
                "modules": ["core::random", "math::distributions"],
            },
            {
                "title": "Number theory",
                "modules": ["core::number_theory"],
            },
            {
                "title": "Numerical methods",
                "modules": ["numerics::diff", "numerics::solve"],
            },
            {
                "title": "Geometry",
                "modules": ["math::geometry"],
            },
            {
                "title": "Algebra",
                "modules": ["extra::algebra"],
            },
            {
                "title": "Trigonometry (extra)",
                "modules": ["math::trigonometry_extra"],
            },
        ],
    },
)

list_of_functions(
    "lists",
    {
        "title": "List-related functions",
        "sections": [
            {
                "modules": ["core::lists"],
            },
        ],
    },
)

list_of_functions(
    "strings",
    {
        "title": "String-related functions",
        "sections": [
            {
                "modules": ["core::strings"],
            },
        ],
    },
)

list_of_functions(
    "datetime",
    {
        "title": "Date and time",
        "introduction": "See [this page](./date-and-time.md) for a general introduction to date and time handling in Numbat.",
        "sections": [
            {
                "modules": ["datetime::functions", "datetime::human"],
            },
        ],
    },
)


list_of_functions(
    "other",
    {
        "title": "Other functions",
        "sections": [
            {
                "title": "Error handling",
                "modules": ["core::error"],
            },
            {
                "title": "Floating point",
                "modules": ["core::numbers"],
            },
            {
                "title": "Quantities",
                "modules": ["core::quantities"],
            },
            {
                "title": "Chemical elements",
                "modules": ["chemistry::elements"],
            },
            {
                "title": "Temperature conversion",
                "modules": ["physics::temperature_conversion"],
            },
        ],
    },
)

subprocess.run(["mdbook", "build"], text=True)
