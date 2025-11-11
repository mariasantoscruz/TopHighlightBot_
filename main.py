import time
from bot.workflow import YoutubeBot   # import the main bot class that does all the heavy lifting
from selenium.common.exceptions import WebDriverException  # used to catch browser-related errors

def main():
    # It asks for a team name, creates the bot, runs the workflow,
    # and keeps the browser open until the user closes it.
    
    # ask the user to type a team name
    team_name = input("Enter the team name to search for: ")
    
    # build the search query for YouTube
    search_query = f"{team_name} highlights"
    
    bot = None  # just initializing the bot variable so it exists even if something crashes later
    try:
        # create a YoutubeBot instance
        bot = YoutubeBot()
        
        # run the bot's main workflow (this probably opens Chrome, searches, etc.)
        bot.run_workflow(search_query)
        
        print("\nWorkflow completed successfully.")
        print("The browser will remain open. Close the browser window to exit.")
        
        
        # This loop keeps running as long as the browser is open
        # once you manually close the browser window, it’ll break out of the loop
        
        while True:
            # accessing .title just checks if the browser is still alive
            # if you close it, Selenium will throw a WebDriverException
            _ = bot.driver.title  
            time.sleep(1)  # wait 1 second before checking again

    except WebDriverException as e:
        # This catches Selenium/browser errors 
        # mainly when the browser window is closed by the user
        
        if "target window already closed" in str(e) or \
           "browser connection is not valid" in str(e) or \
           "no such window" in str(e):
            print("\nBrowser window closed by user.")
        else:
            # some other Selenium error happened
            print(f"\nAn unhandled WebDriver error occurred: {e}")
            
    except Exception as e:
        
        # Catch any other random error that isn’t browser-related
        
        print(f"\nAn error occurred during the bot execution: {e}")
    
    finally:
        
        # This part runs no matter what (even if there was an error)
        # It makes sure the bot shuts down cleanly
        if bot:
            bot.shutdown()  # this method probably closes the browser and cleans things up
            print("Script finished. Shutdown complete")


if __name__ == "__main__":
    main()
