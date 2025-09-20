# SheetBridge

SheetBridge is a powerful tool that converts Excel formulas to Python code using two different approaches: traditional parsing and LLM-powered generation. It provides a Streamlit web interface for easy file upload and conversion.

## Features

- **Traditional Parser**: Uses Lark grammar parsing to convert Excel formulas to Python pandas code
- **LLM-Powered Conversion**: Leverages multiple AI providers (Local Ollama, Google Gemini, OpenRouter) to generate Python code from Excel formulas
- **Web Interface**: Clean Streamlit-based UI for file upload and conversion
- **Multiple Output Formats**: Download converted Python scripts directly
- **Support for Common Excel Functions**: SUM, AVERAGE, COUNT, MAX, MIN, MEDIAN, UNIQUE, and basic arithmetic operations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd sheetbridge
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration (Optional)

For LLM-powered features, create a `.env` file in the project root:

```bash
# For OpenRouter API
OPENROUTER_API_KEY=your_openrouter_api_key_here

# For Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here
```

**Note**: The traditional parser works without any API keys. LLM features require appropriate API keys or local Ollama installation.

### Step 5: Run the Application

```bash
streamlit run main.py
```

The application will start and be available at `http://localhost:8501` in your web browser.

## Usage

1. **Upload Excel File**: Use the file uploader to select an Excel file (.xlsx or .xls)
2. **Choose Compiler**: Select from:
   - **Traditional**: Uses grammar-based parsing
   - **LLM-powered**: Uses AI models for conversion
   - **Both**: Shows output from both methods
3. **Select Provider** (for LLM mode): Choose between Local (Ollama), Gemini, or OpenRouter
4. **Download Results**: Download the generated Python script

## Supported Excel Functions

- **Mathematical**: SUM, AVERAGE, COUNT, MAX, MIN, MEDIAN
- **Data Processing**: UNIQUE
- **Arithmetic**: +, -, *, /
- **Cell References**: A1, B2, etc.
- **Ranges**: A1:B10, etc.

## Dependencies

- `lark`: Grammar parsing for traditional conversion
- `openpyxl`: Excel file reading
- `streamlit`: Web interface
- `pandas`: Data manipulation
- `pydantic`: Data validation
- `python-dotenv`: Environment variable management
- `ollama`: Local LLM integration
- `google-genai`: Google Gemini API
- `openai`: OpenRouter API client

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Project Structure

```
sheetbridge/
├── main.py                 # Streamlit application entry point
├── grammar.lark           # Lark grammar definition for Excel formulas
├── llm/                   # LLM integration module
│   └── llm.py            # AI provider implementations
├── traditional/           # Traditional parsing module
│   ├── lark_parser.py    # Grammar parser and transformers
│   └── utils.py          # Excel file processing utilities
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Development dependencies
```

## Troubleshooting

### Common Issues

1. **Streamlit not starting**: Ensure all dependencies are installed and virtual environment is activated
2. **LLM features not working**: Check API keys in `.env` file or ensure Ollama is running locally
3. **Excel file not loading**: Ensure file is in .xlsx or .xls format and not corrupted
