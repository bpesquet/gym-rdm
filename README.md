# gym-rdm

A [Gymnasium](https://gymnasium.farama.org/) environment for training agents on Random Dot Motion tasks.

## Development notes

### Toolchain

This project is built with the following software:

- [Poetry](https://python-poetry.org/) for dependency management and packaging;
- [Black](https://github.com/psf/black) for code formatting;
- [Pylint](https://github.com/pylint-dev/pylint) and [mypy](http://mypy-lang.org/) to detect defaults and mistakes in the code;
- [pytest](https://docs.pytest.org) for testing the code.

### Useful commands

```bash
# Reformat all Python files
black gym_rdm tests

# Check the code for mistakes
pylint gym_rdm tests

# Run all code examples as unit tests
# The -s flag prints code output
pytest [-s]

# Run static type checking
# The -strict flag is... stricter. It should pass on the codebase
mypy [--strict] .
```

## License

[MIT](CODE_LICENSE).

Copyright © 2024-present [Baptiste Pesquet](https://bpesquet.fr).
