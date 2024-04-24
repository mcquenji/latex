import os
import sys
import re


def load_whitelist() -> list[str]:
    with open(".github/workflows/ignore.conf", "r") as file:
        return [line.strip() for line in file if not line.startswith("#")]


def is_whitelisted(line: str, whitelist: list[str]) -> bool:
    for pattern in whitelist:
        if re.search(pattern, line):
            return True
    return False


def main():
    WHITELIST = load_whitelist()

    errors = []
    warnings = []
    whitelisted = []

    DOWNLOAD_URL = sys.argv[1]

    with open("main.log", "r") as file:
        for line in file:
            found_error = False
            is_warning = False

            if "error " in line.lower():
                found_error = True
            elif "warning " in line.lower():
                found_error = True
                is_warning = True

            if found_error:
                if is_whitelisted(line, WHITELIST):
                    whitelisted.append(line)
                elif is_warning:
                    warnings.append(line)
                else:
                    errors.append(line)

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
                + "\n```\n</details>\n\n"
            )
    else:
        comment_body += "No critical issues found.\n"

    if whitelisted:
        comment_body += (
            "<details><summary>Suppressed errors & warnings</summary>\n\n```\n"
            + "\n".join(whitelisted)
            + "\n```\n</details>\n"
        )

    if os.path.exists("main.pdf"):
        comment_body += f"[Download Preview]({DOWNLOAD_URL})\n"
    else:
        comment_body += (
            f"Preview could not be compiled. [Download logs]({DOWNLOAD_URL})\n"
        )

    with open("comment_body.md", "w") as file:
        file.write(comment_body)


if __name__ == "__main__":
    main()
