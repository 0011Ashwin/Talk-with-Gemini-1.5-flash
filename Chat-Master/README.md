# PDF Intellichat

![PDF Intellichat](https://img.shields.io/badge/PDF-Intellichat-blue)
![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)

A powerful PDF document assistant that leverages Google's Gemini AI to provide intelligent responses to your questions based on the content of your PDF documents.

## Features

- **Document Processing**: Upload multiple PDFs for processing and analysis
- **AI-Powered Chat**: Ask natural language questions about your documents
- **Vector Search**: Utilizes FAISS to perform semantic search on document content
- **Professional UI**: Modern, responsive interface with light/dark mode support
- **PDF Statistics**: View detailed information about your uploaded documents
- **Chat History**: Maintains conversation context for better interaction
- **Custom Settings**: Configure model parameters and processing options

## Requirements

- Python 3.7+
- Streamlit
- PyPDF2
- LangChain
- Google Generative AI API
- FAISS vector store
- Streamlit-Lottie

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pdf-intellichat.git
cd pdf-intellichat
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run multi_chat_reader.py
```

2. Upload PDF documents through the sidebar interface
3. Click "Process PDFs" to analyze the documents
4. Start asking questions about your documents in the chat interface

## How It Works

1. **Text Extraction**: Extracts raw text from PDF documents
2. **Text Chunking**: Splits text into manageable chunks for processing
3. **Vector Embedding**: Creates semantic embeddings of text using Google's AI
4. **Similarity Search**: Finds relevant document sections based on user queries
5. **LLM Response**: Generates comprehensive answers using Gemini LLM

## Customization

- **Dark Mode**: Toggle between light and dark interface themes
- **Model Selection**: Choose between different Gemini AI models
- **Temperature**: Adjust the creativity level of AI responses
- **Expert Mode**: Fine-tune chunk size and overlap for advanced users

## License

MIT

## Acknowledgements

- Google Generative AI
- Streamlit Team
- LangChain
- PyPDF2
- FAISS 