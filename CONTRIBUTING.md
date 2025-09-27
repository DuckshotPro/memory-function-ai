# Contributing to Memory Function AI

First off, thank you for considering contributing! Your help is greatly appreciated.

## How to Contribute

We follow a standard GitHub fork-and-pull-request workflow.

1.  **Fork the repository** to your own GitHub account.
2.  **Clone your fork** to your local machine.
3.  **Create a new branch** for your changes (`git checkout -b my-new-feature`).
4.  **Make your changes** and commit them with clear, descriptive messages.
5.  **Push your changes** to your fork (`git push origin my-new-feature`).
6.  **Open a Pull Request** from your fork's branch to the `main` branch of the original repository.

## Development Setup

1.  Follow the **Installation** and **Configuration** steps in the `README.md` file.
2.  Ensure you have all development dependencies installed:
    ```bash
    pip install -r mcp_server/requirements.txt
    pip install -r conversation_feeder/requirements.txt
    ```

## Running Tests

Before submitting a pull request, please ensure that all tests pass.

```bash
# Make sure you are in the root project directory
pytest
```

For the tests to run, you may need to configure a separate test database and set the `DATABASE_URL_TEST` environment variable, or ensure your main database is accessible.

## Coding Style

We use `ruff` for linting and code formatting. Please run it on your code before committing.

```bash
ruff check .
```

Thank you for your contributions!
