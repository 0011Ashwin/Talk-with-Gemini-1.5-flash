# Gemini Chat Application

A modern chat application built with Flask and Google's Gemini AI that allows users to interact with Google's Gemini 1.5 Pro large language model.

## Features

- Clean, responsive web interface
- Real-time conversation with Gemini 1.5 Pro AI model
- Chat history management
- New chat functionality
- Dark/light theme toggle
- Mobile-friendly design

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Google's Gemini AI API
- **Styling**: Custom CSS with FontAwesome icons

## Prerequisites

- Python 3.7+
- Google Gemini API key

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install flask google-generativeai python-dotenv
   ```

4. Create a `.env` file in the root directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Start chatting with Gemini!

## Project Structure

- `app.py` - Main Flask application
- `templates/index.html` - HTML template for the chat interface
- `static/` - Directory containing CSS styles and any static assets

## API Reference

The application uses Google's Gemini 1.5 Pro model for generating responses. You'll need to [obtain an API key](https://ai.google.dev/) from Google to use this service.

## License

[MIT License](LICENSE)

## Acknowledgements

- Google for providing the Gemini AI API
- Flask team for the lightweight web framework