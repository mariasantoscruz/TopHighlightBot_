import time
from bot.workflow import YoutubeBot
# Import this exception to detect when the browser is closed
from selenium.common.exceptions import WebDriverException

def main():
    """
    Main entry point for the application.
    Handles user input and orchestrates the bot's workflow.
    """
    team_name = input("Enter the team name to search for: ")
    search_query = f"{team_name} highlights"
    
    bot = None
    try:
        bot = YoutubeBot()
        bot.run_workflow(search_query)
        
        print("\nWorkflow completed successfully.")
        print("The browser will remain open. Close the browser window to exit.")
        
        # This loop will run as long as the browser is open.
        # It will break when the user manually closes the browser window.
        while True:
            # Accessing .title is a lightweight way to check if the browser is alive.
            # If the user closes the window, this will raise a WebDriverException.
            _ = bot.driver.title 
            time.sleep(1)

    except WebDriverException as e:
        # This specific exception is raised when the browser is closed manually.
        if "target window already closed" in str(e) or \
           "browser connection is not valid" in str(e) or \
           "no such window" in str(e):
            print("\nBrowser window closed by user.")
        else:
            # A different WebDriver error occurred
            print(f"\nAn unhandled WebDriver error occurred: {e}")
            
    except Exception as e:
        # Catch any other non-Selenium errors
        print(f"\nAn error occurred during the bot execution: {e}")
    
    finally:
        if bot:
            # The shutdown() method will now handle cleanup gracefully
            bot.shutdown()
            print("Script finished. Shutdown complete.")

if __name__ == "__main__":
    main()