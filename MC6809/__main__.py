"""
    Allow MC6809 to be executable
    through `python -m MC6809`.
"""


from MC6809.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
