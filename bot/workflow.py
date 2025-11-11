import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options

# importing helper stuff from other files in this project
from .locators import SearchPageLocators, VideoPageLocators
from .parser import VideoParser


class YoutubeBot:
    # This class controls the whole browser automation thing.
    # It starts Chrome, runs searches on YouTube, grabs the top video, and handles shutdown
    def __init__(self, base_url="https://www.youtube.com"):
        self.base_url = base_url
        options = Options()
        
        # Anti-detection tweaks:
        # these options make the bot look a little less like a bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # no user profile, runs like a fresh Chrome session
        # so it's not logged into any Google account

        # set a fake but realistic browser "user-agent"
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        
        # check where Chrome is installed (Windows paths)
        try:
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not os.path.exists(options.binary_location):
                options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        except Exception:
            print("Binary location not set, assuming default PATH.")

        # uncomment this if you want it to run without showing the browser window:
        # options.add_argument("--headless") 
        
        # launch Chrome automatically using webdriver-manager
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # make a wait object to pause until elements load
        self.wait = WebDriverWait(self.driver, 20) 
        print("WebDriver initialized.")

    def run_workflow(self, search_query: str):
        # Runs the main workflow: go to YouTube, search, find top video, open it ###
        self._load_search_page(search_query)
        top_video_link = self._find_top_video_link()
        if top_video_link:
            # open the top video (doesn’t press anything)
            self._navigate_to_video(top_video_link)
        else:
            print("Workflow halted: No top video link was found.")

    def _load_search_page(self, query: str):
        # Open YouTube, handles cookies, do the search 
        self.driver.get(self.base_url)
        print(f"Navigated to {self.base_url}")
        
        try:
            # try to handle the “accept cookies” popup if it shows up
            cookie_wait = WebDriverWait(self.driver, 5) 
            accept_button = cookie_wait.until(
                EC.element_to_be_clickable(SearchPageLocators.ACCEPT_COOKIES_BUTTON)
            )
            accept_button.click()
            print("Cookie consent dialog handled.")
        except TimeoutException:
            print("Cookie consent dialog not found, proceeding...")

        try:
            # wait until the search bar and button are ready
            search_input = self.wait.until(
                EC.element_to_be_clickable(SearchPageLocators.SEARCH_INPUT)
            )
            search_button = self.wait.until(
                EC.element_to_be_clickable(SearchPageLocators.SEARCH_BUTTON)
            )
            
            # type the query and click the button
            search_input.clear()
            search_input.send_keys(query)
            search_button.click()
            print(f"Performed search for: '{query}'")
        except TimeoutException:
            print("Error: Could not find search bar or search button.")
            raise  # stop everything if the search fails

    def _find_top_video_link(self) -> str:
        ### Finds all video results and picks the top one (the most viewed, I guess) ###
        try:
            # wait until search results are visible
            self.wait.until(
                EC.presence_of_element_located(SearchPageLocators.VIDEO_RESULT_ITEM)
            )
            video_elements = self.driver.find_elements(
                *SearchPageLocators.VIDEO_RESULT_ITEM
            )
            
            if not video_elements:
                raise TimeoutException("No video result elements found post-search.")

            # let the parser figure out which one is the “top” video
            top_video = VideoParser.find_top_video(video_elements)

            if not top_video:
                raise ValueError("Parser failed to identify a top video.")
                
            # grab the link from the top video
            link_element = top_video.find_element(*SearchPageLocators.VIDEO_TITLE_LINK)
            video_url = link_element.get_attribute("href")
            
            if not video_url:
                 raise ValueError("Found top video element but it contains no href link.")
            
            print(f"Found video URL: {video_url}")
            return video_url

        except TimeoutException:
            print("Error: Timed out waiting for video results to load.")
            return None  # don’t crash, just stop the workflow
        except Exception as e:
            print(f"Error finding top video: {e}")
            return None  # again, stop w/o crash

    def _navigate_to_video(self, video_url: str):
        ### Opens the video page and waits for the player to load 
        self.drive
