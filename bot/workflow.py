import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options

from .locators import SearchPageLocators, VideoPageLocators
from .parser import VideoParser

class YoutubeBot:
    """
    Manages the Selenium WebDriver instance and orchestrates
    the browser automation workflow.
    """
    def __init__(self, base_url="https://www.youtube.com"):
        self.base_url = base_url
        options = Options()
        
        # --- Anti-detection options ---
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # --- Removed user-profile-dir logic ---
        # This bot will now run in a clean, logged-out session.

        # Set a common User-Agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        
        # Robust binary location check
        try:
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not os.path.exists(options.binary_location):
                options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        except Exception:
            print("Binary location not set, assuming default PATH.")

        # options.add_argument("--headless") 
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        self.wait = WebDriverWait(self.driver, 20) 
        print("WebDriver initialized.")

    def run_workflow(self, search_query: str):
        """Public method to execute the full bot workflow."""
        self._load_search_page(search_query)
        top_video_link = self._find_top_video_link()
        if top_video_link:
            # Changed to navigate only, no "like" action
            self._navigate_to_video(top_video_link)
        else:
            print("Workflow halted: No top video link was found.")

    def _load_search_page(self, query: str):
        """Loads the base URL and performs the search."""
        self.driver.get(self.base_url)
        print(f"Navigated to {self.base_url}")
        
        try:
            # Wait for cookie banner (5 sec timeout)
            cookie_wait = WebDriverWait(self.driver, 5) 
            accept_button = cookie_wait.until(
                EC.element_to_be_clickable(SearchPageLocators.ACCEPT_COOKIES_BUTTON)
            )
            accept_button.click()
            print("Cookie consent dialog handled.")
        except TimeoutException:
            print("Cookie consent dialog not found, proceeding...")

        try:
            # Wait for search elements
            search_input = self.wait.until(
                EC.element_to_be_clickable(SearchPageLocators.SEARCH_INPUT)
            )
            search_button = self.wait.until(
                EC.element_to_be_clickable(SearchPageLocators.SEARCH_BUTTON)
            )
            
            search_input.clear()
            search_input.send_keys(query)
            search_button.click()
            print(f"Performed search for: '{query}'")
        except TimeoutException:
            print("Error: Could not find search bar or search button.")
            raise # Re-raise exception to stop the workflow

    def _find_top_video_link(self) -> str:
        """Finds all video results and returns the href of the top-viewed one."""
        try:
            self.wait.until(
                EC.presence_of_element_located(SearchPageLocators.VIDEO_RESULT_ITEM)
            )
            video_elements = self.driver.find_elements(
                *SearchPageLocators.VIDEO_RESULT_ITEM
            )
            
            if not video_elements:
                raise TimeoutException("No video result elements found post-search.")

            top_video = VideoParser.find_top_video(video_elements)

            if not top_video:
                raise ValueError("Parser failed to identify a top video.")
                
            link_element = top_video.find_element(*SearchPageLocators.VIDEO_TITLE_LINK)
            video_url = link_element.get_attribute("href")
            
            if not video_url:
                 raise ValueError("Found top video element but it contains no href link.")
            
            print(f"Found video URL: {video_url}")
            return video_url

        except TimeoutException:
            print("Error: Timed out waiting for video results to load.")
            return None # Return None instead of crashing
        except Exception as e:
            print(f"Error finding top video: {e}")
            return None # Return None instead of crashing

    def _navigate_to_video(self, video_url: str):
        """Navigates to the video URL and waits for the player to load."""
        self.driver.get(video_url)
        
        try:
            # Wait for the video player to be visible as confirmation
            self.wait.until(
                EC.visibility_of_element_located(VideoPageLocators.PLAYER_CONTAINER)
            )
            print(f"Successfully navigated to video page.")
            
        except TimeoutException:
            print("Error: Timed out waiting for video page to load.")
        except Exception as e:
            print(f"Error navigating to video page: {e}")


    def shutdown(self):
        """
        Closes the WebDriver gracefully.
        Handles exceptions if the browser was already closed by the user.
        """
        if self.driver:
            try:
                self.driver.quit()
                print("WebDriver shut down.")
            except WebDriverException:
                # This happens if the user already closed the window manually.
                # It's expected, so we can just pass.
                print("Browser was already closed by user.")
            except Exception as e:
                print(f"An error occurred during shutdown: {e}")