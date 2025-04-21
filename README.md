# TrashTalker

TrashTalker is a desktop application that generates offensive insults using a locally hosted language model. It provides a simple interface for generating and copying insults to your clipboard with a single keystroke.

## Features

- Generate creative offensive insults with a single keystroke (F9)
- Copy insults to clipboard with a single click
- Always-on-top window for easy access during gameplay or other activities
- Uses a locally hosted LLM for privacy and offline usage

## Requirements

- Windows operating system
- Python 3.10 or higher
- LM Studio with the llama2-13b-psyfighter2 model

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/RayWangyangMa/TrashTalker.git
   cd TrashTalker
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install and set up LM Studio:
   - Download and install [LM Studio](https://lmstudio.ai/)
   - Download the llama2-13b-psyfighter2 model within LM Studio

## Usage

1. Start LM Studio and load the llama2-13b-psyfighter2 model
2. Start the LM Studio server:
   - Go to the "Server" tab in LM Studio
   - Click "Start Server"
   - Ensure the server is running on `http://localhost:1234`

3. Run the TrashTalker application:
   ```
   python main.py
   ```

### Using the Application

1. Press **F9** to generate new insults
2. Click on any insult to copy it to your clipboard
3. The application will always stay on top of other windows for easy access

## Customization

You can customize the prompt templates in `prompt_templates.py` to change the style or language of the generated insults.

## Troubleshooting

- **"Error connecting to LM Studio API"**: Make sure LM Studio is running and the server is started on port 1234
- **"Model not found"**: Ensure you have downloaded the llama2-13b-psyfighter2 model in LM Studio
- **"Application not responding"**: The LLM may be processing - give it a moment to generate content

## License

[MIT License](LICENSE)

## Disclaimer

This application generates offensive content intended for entertainment purposes. The developers do not endorse or encourage harmful behavior based on the generated content.
