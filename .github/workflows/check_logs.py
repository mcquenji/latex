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

    fail_on_warning = os.getenv("FAIL_ON_WARNING", "false").lower() == "true"
    with open("main.log", "r") as file:
        for line in file:
            found_error = False

            if "error " in line.lower():
                found_error = True
            if "warning " in line.lower() and fail_on_warning:
                found_error = True

            if found_error and not is_whitelisted(line, WHITELIST):
                sys.exit(1)  # Exit with error if a critical issue is found

    sys.exit(0)  # Exit successfully if no critical issues


if __name__ == "__main__":
    main()
