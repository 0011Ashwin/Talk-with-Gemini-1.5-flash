# Gemini Chat Application

A modern chat application built with Flask and Google's Gemini AI that provides an authentic Google Gemini experience. This application allows users to interact with Google's Gemini 1.5 Pro large language model through a sleek, responsive interface that closely resembles the official Google Gemini UI.

![Gemini Chat](https://www.gstatic.com/lamda/images/gemini_sparkle_v002_20231113_16x9.svg)

## Features

- **Authentic Google Gemini UI**: Closely mimics the official Google Gemini interface
- **Interactive Chat**: Real-time conversation with Gemini 1.5 Pro AI model
- **SVG Gemini Logo**: Includes animated SVG Gemini logo with sparkle effects
- **Suggestion Chips**: Helpful suggestion chips to kickstart conversations
- **Chat History Management**: Save and manage conversation history
- **Message Actions**: Copy, like, or dislike responses
- **Dark/Light Theme Toggle**: Switch between light and dark themes
- **Mobile-Responsive Design**: Works on all device sizes
- **Animated Elements**: Includes subtle animations for a polished feel

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Google's Gemini AI API
- **Styling**: Google's Material Design principles
- **Icons**: Font Awesome 6.5.1
- **Fonts**: Google Sans, Product Sans, and Roboto fonts

## Prerequisites

- Python 3.7+
- Google Gemini API key (from Google AI Studio)

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

- `app.py` - Main Flask application with Gemini API integration
- `templates/index.html` - HTML template for the Gemini chat interface
- `static/style.css` - CSS styling with Google's design language
- `.env` - Environment variables file (create this yourself)

## Troubleshooting

If you encounter any issues:

1. **No Response from Gemini**: Check your API key and internet connection
2. **Signal Error**: Make sure to run the app with `debug=False` to avoid signal errors
3. **Styling Issues**: Ensure all CSS is loaded correctly and clear your browser cache

## How to Get a Gemini API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create or sign in to your Google account
3. Navigate to the API section and create a new API key
4. Copy the key and add it to your `.env` file

## API Reference

The application uses Google's Gemini 1.5 Pro model for generating responses. The model is accessed through the Google Generative AI Python library, which provides a simple interface for generating text responses.

```python
model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content(question)
```

## License

[MIT License](LICENSE)

## Acknowledgements

- Google for providing the Gemini AI API and design inspiration
- Flask team for the lightweight web framework
- The open-source community for various libraries and tools used in this project