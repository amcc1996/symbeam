# SymBeam examples suit
# README.md generation script
# ==========================================================================================
#                                                      António Carneiro <amcc@fe.up.pt> 2020

import glob
import os
import re


# Human sorting: from https://stackoverflow.com/questions/5967500/
# how-to-correctly-sort-a-string-with-a-number-inside
def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]


# Get list of examples and remove the current script
list_examples = glob.glob("./*.py")
list_examples.remove("./" + __file__)
list_examples.sort(key=natural_keys)

# Create the directory for SVG files
svg_dir = "./svg"
if not os.path.exists(svg_dir):
    os.makedirs(svg_dir)

# Start writing the README.md
with open("README.md", "w") as file:
    file.write("# Examples\n")
    file.write(
        "Here you can find a comprehensive but by no means exhaustive list of"
        + " examples exploring the capabilities of SymBeam. In each example,"
        + " you will find a hyperlink to the associated file in the repository,"
        + " the respective source code and output: both console and plot.\n"
    )

    # Loop over all examples
    for example in list_examples:
        name = os.path.basename(example)
        file.write("\n## [{0}](./{1})".format(name, name))
        print("\nRunning {0}".format(example))

        # Create an emtpy temporary file
        tmp_file = "./tmp_symbeam"
        open(tmp_file, "w").close()

        # Run the script and capture the terminal output
        os.system("python3 " + example + " >> " + tmp_file)

        # Check if a .svg file has been produced and move it into the svg/ directory
        has_svg = False
        svg_path = os.path.splitext(example)[0] + ".svg"
        if os.path.exists(svg_path):
            found = True
            print("Found {0}".format(svg_path))
            new_svg_path = os.path.join(svg_dir, svg_path)
            os.rename(svg_path, new_svg_path)

        # Read the Markdown content in each script
        with open(example, "r") as example_file:
            example_lines = example_file.readlines()

        with open(tmp_file, "r") as tfile:
            output_lines = tfile.readlines()

        # Find the documentation and source code
        doc_start = 0
        doc_end = 0
        for i, line in enumerate(example_lines):
            if len(line.split()) > 1:
                if line.split()[0] == "#":
                    if line.split()[1] == "Features:":
                        doc_start = i
                else:
                    doc_end = i - 1
                    break

        source_start = doc_end + 1
        source_end = len(example_lines) - 1

        doc_lines = []
        doc_lines.append(" ".join(example_lines[doc_start].split()[2:]))
        for i in range(doc_start + 1, doc_end + 1):
            doc_lines.append(" ".join(example_lines[i].split()[1:]))

        # Write the example features
        for line in doc_lines:
            file.write("\n" + line)

        # Write the source code and output to the README.md file
        file.write("\n```python\n")
        found_blank = 0
        for line in example_lines[source_start + 2 : source_end + 1]:
            # Stop when an emtpy line is found
            if len(line.split()) == 0:
                found_blank = found_blank + 1

            if len(line.split()) == 0 and found_blank > 2:
                break

            file.write(line)

        file.write("```")

        # Write image code
        file.write(
            '\n<p align="center">\n  <img src="{0}" width="70%">\n</p>\n'.format(
                new_svg_path
            )
        )

        # Wite terminal output
        file.write("\n```")
        for line in output_lines:
            file.write(line)

        file.write("\n```")


if os.path.exists(tmp_file):
    os.remove(tmp_file)
