# Lichess Position Analyzer

![Lichess Position Analyzer](path-to-image.png)

## Overview

**Lichess Position Analyzer** is a Chrome extension designed to enhance your chess experience on Lichess by allowing you to extract and analyze positions directly from the analysis board. This extension provides users with tactical, positional, material, and strategic analyses of their chess games using a server-side engine and LLMs.

## Features

- **Extract FEN & PGN:** Capture and display the current FEN and PGN strings from the Lichess analysis board.
- **Comprehensive Analysis:** Perform tactical, positional, material, and strategic analyses based on the extracted positions.
- **Interactive Interface:** User-friendly interface with tooltips explaining each analysis type.

## Technologies Used

- **Frontend:** JavaScript, HTML, CSS
- **Backend:** Python, Flask, OpenAI API, hosted on Render
- **Chrome Extension APIs:** Service Workers, Content Scripts, Storage API
- **Server:** Gunicorn

## Screenshots and Descriptions

### Popup Interface

![Popup Interface](path-to-popup-interface-image.png)
*Displays the extension's interface where users can extract FEN and PGN, and perform various types of analysis.*

### Extracting FEN & PGN

![Extracting FEN & PGN](path-to-extract-fen-pgn-image.png)
*After clicking "Get Position," the FEN and PGN strings are displayed, allowing for further analysis.*

### Performing Tactical Analysis

![Tactical Analysis](path-to-tactical-analysis-image.png)
*The extension provides a detailed tactical analysis based on the current chess position.*

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- OpenAI Python package
- Gunicorn

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/lichess_position_analyzer.git
    cd lichess_position_analyzer
    ```

2. **Navigate to the backend directory and install the dependencies**:

    ```sh
    cd backend
    pip install -r requirements.txt
    ```

3. **Run the server**:

    ```sh
    python server.py
    ```

### Usage

1. **Load the Chrome Extension:**

    - Open Chrome and navigate to `chrome://extensions/`
    - Enable `Developer mode`
    - Click on `Load unpacked` and select the `lichess_position_analyzer/extension` directory

2. **Using the Extension:**

    - Open Lichess and navigate to the analysis board
    - Click on the extension icon in the Chrome toolbar
    - Extract the FEN and PGN by clicking "Get Position"
    - Choose an analysis type (Tactical, Positional, Material, or Strategic) to get the analysis results

### Project Structure

```bash
lichess_position_analyzer/
├── backend/
│   ├── .env                   # Environment variables
│   ├── Procfile               # Gunicorn configuration
│   ├── requirements.txt       # Backend dependencies
│   ├── server.py              # Main server file
│
└── extension/
    ├── icons/
    │   ├── icon16.png         # Extension icon (16x16)
    │   ├── icon48.png         # Extension icon (48x48)
    │   └── icon128.png        # Extension icon (128x128)
    ├── background.js          # Service worker script for background tasks
    ├── content.js             # Content script to interact with Lichess page
    ├── manifest.json          # Extension configuration
    ├── popup.html             # Popup interface
    ├── popup.js               # Script for popup interactions
    ├── style.css              # Styling for the extension
    └── image.png              # Image used in the README
