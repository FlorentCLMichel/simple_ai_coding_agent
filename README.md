# Simple Coding Agent

A basic coding agent implemented in Python, inspired by the [freeCodeCamp tutorial](https://www.freecodecamp.org/news/build-an-ai-coding-agent-with-python-and-gemini/). This agent uses the Gemini API to generate code based on user prompts.

**Warning:** This implementation is intended for educational purposes only and does not come with any security or performance guarantees. Use it at your own risk.

## Features

*   Accepts user prompts and generates code using the Gemini API.
*   Demonstrates a basic implementation of an AI-powered coding agent.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/FlorentCLMichel/simple_ai_coding_agent
    cd simple_ai_coding_agent
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\\Scripts\\activate.bat  # On Windows
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**

    Create a `.env` file in the project's root directory and add your Gemini API key and model information:

    ```
    GEMINI_API_KEY=<your Gemini API key>
    MODEL=<model to use>
    ```

    See the [Gemini API documentation](https://ai.google.dev/gemini-api/docs) for instructions on how to [create and use API keys](https://ai.google.dev/gemini-api/docs/api-key) and a [list of available models](https://ai.google.dev/gemini-api/docs/models).

    **WARNING: Do not share your API key!**

## Usage

1.  **Run the `main.py` script:**

    ```bash
    python main.py <your_prompt>
    ```

    Replace `<your_prompt>` with the coding task you want the agent to perform. For example:

    ```bash
    python main.py "Write a Python function to calculate the factorial of a number."
    ```

2.  **Review the generated code:**

    The agent will print the generated code to the console and/or to a file. Carefully review the code before using it to ensure it meets your requirements and is free of errors.

## Command-Line Arguments

The `main.py` script accepts the following command-line arguments:

*   `prompt` (required): The user prompt that guides the coding agent.
*   `--verbose`, `-v` (optional): Enables verbose mode, providing more detailed output during the agent's execution.
*   `--work_dir` (optional): Specifies the working directory for the agent. Defaults to "test_calculator".
*   `--max_iter` (optional): Sets the maximum number of iterations for the agent's loop. Defaults to 20.
*   `--max_tok` (optional): Sets the maximum number of tokens to be used during the agent's execution. Defaults to 10000.  **Warning:** The actual number of tokens used may exceed this value.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, concise messages.
4.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE.txt).
