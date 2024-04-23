import os
import sys


def main():
    fail_on_warning = os.getenv("FAIL_ON_WARNING", "false").lower() == "true"
    with open("main.log", "r") as file:
        for line in file:
            if "error: " in line.lower():
                sys.exit(1)  # Exit with error if there are errors
            if "warning: " in line.lower() and fail_on_warning:
                sys.exit(
                    1
                )  # Exit with error if FAIL_ON_WARNING is true and there are warnings

    sys.exit(0)  # Exit successfully if no critical issues


if __name__ == "__main__":
    main()
