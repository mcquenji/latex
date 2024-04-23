import os
import sys


def main():
    errors = []
    warnings = []

    ARTIFACT_NAME = sys.argv[1]

    with open("main.log", "r") as file:
        for line in file:
            if "error" in line.lower():
                errors.append(line.strip())
            if "warning" in line.lower():
                warnings.append(line.strip())

    comment_body = "Build results:\n"
    if errors or warnings:
        if errors:
            comment_body += (
                "<details><summary>Errors</summary>\n\n```\n"
                + "\n".join(errors)
                + "\n```\n</details>\n"
            )
        if warnings:
            comment_body += (
                "<details><summary>Warnings</summary>\n\n```\n"
                + "\n".join(warnings)
                + "\n```\n</details>\n"
            )
    else:
        comment_body += "No critical issues found.\n"

    if os.path.exists("main.pdf"):
        comment_body += (
            "[Download the compiled PDF](https://github.com/${{ github.repository }}/actions/artifacts/${{ github.run_id }}?artifactName="
            + f"{ARTIFACT_NAME}"
            + ")\n"
        )

    with open("comment_body.md", "w") as file:
        file.write(comment_body)


if __name__ == "__main__":
    main()