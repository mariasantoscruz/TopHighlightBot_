# YouTube Highlights Finder Bot

OBS: This readme has done with assistance of AI.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4-green?style=for-the-badge&logo=selenium)

This project is a Python automation script designed to quickly find the best highlights of teams on YouTube.

Instead of manually searching and guessing which video has the best content, this bot automates the process. It searches by the team name, analyzes the results, and opens the video with the **highest number of views** for you to watch.

## 🤖 How It Works

The bot simulates the actions of a regular user directly in the Google Chrome browser:

1.  **Initialization**: The script starts Google Chrome using Selenium. It applies special `ChromeOptions` (such as `--disable-blink-features=AutomationControlled`) so that YouTube does not identify it as a bot.
2.  **Search**: It accesses `youtube.com`, handles the cookie pop-up (if it appears), and types the search query (e.g., "Real Madrid highlights") into the search bar.
3.  **Parsing (Analysis)**: After the results page loads, the bot uses the `VideoParser` to:
    * Find all video elements on the page.
    * Extract the view count text for each one (e.g., "1.2M views", "10K views").
    * Convert this text into an integer (e.g., `1200000`, `10000`) to allow accurate comparison.
4.  **Selection**: The script compares the view counts and identifies which video in the list is the most popular.
5.  **Navigation**: The bot navigates to the URL of the video with the highest number of views.
6.  **Wait Mode**: The main script (`main.py`) stays in wait mode, allowing the user to watch the video. To end the program, the user simply needs to **close the browser window manually**.

## ✨ Main Features

* **Automation with Selenium**: Uses the Selenium library and `webdriver-manager` to control the Chrome browser reliably.
* **Anti-Detection Mode**: The browser starts with special flags to prevent being identified as a bot, allowing access to YouTube’s standard interface.
* **Smart Parsing**: Can read and convert the view count text (like "1.2M views", "10K views", "808 views") into integers for accurate comparison.
* **Interactive Flow**: The bot completes its task and gives control back to the user, waiting for them to close the browser to end the script cleanly.

## ⚙️ Installation and Execution: Step by Step

Follow these steps to set up the environment and run the project.

### 1. Prerequisites

* **Python 3.10** or higher installed.
* **Google Chrome** installed (the bot uses this browser).

### 2. Clone the Repository

First, clone this repository to your local machine and enter the project folder:

```bash
git clone [https://github.com/your-username/your-repository.git](https://github.com/your-username/your-repository.git)
cd your-repository
```

### 3. Clone the Repository

It’s a good practice to use a virtual environment (.venv) to isolate the project’s dependencies.

```bash
# Create the virtual environment
python -m venv .venv
```

### 4. Activate the Virtual Environment

You need to activate the environment before installing the packages.

On Windows (PowerShell):


```bash
.\.venv\Scripts\Activate.ps1
```


On macOS or Linux:

```bash
source .venv/bin/activate
```



You’ll know it worked because the environment name (e.g., (.venv)) will appear at the beginning of your command prompt.

### 5. Install the Dependencies

This project uses selenium for automation and webdriver-manager to automatically download and manage the Chrome driver.

Install the dependencies listed in requirements.txt:



```bash
pip install -r requirements.txt
```

### 6. Run the Bot

With the environment activated and the packages installed, run the main.py script:


```bash
python main.py
```

### 7. Interact with the Bot

1. The terminal will prompt: Enter the team name to search for:

2. Type the team name (e.g., Real Madrid) and press Enter.

3. A new Chrome window should open. The bot will perform the search and open the video with the most views.

4. The terminal will display the message: "The browser will remain open. Close the browser window to exit."

5. When you finish watching, simply close the Chrome window. The script in the terminal will detect it and close automatically.


