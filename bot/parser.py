import re
from selenium.webdriver.remote.webelement import WebElement
from .locators import SearchPageLocators

class VideoParser:
    """
    Handles parsing of raw data from WebElements.
    Decouples parsing logic from browser interaction logic.
    """

    @staticmethod
    def _parse_view_count(view_text: str) -> int:
        """
        Converts formatted view strings (e.g., '1.2M views', '10K views')
        into a parsable integer.
        """
        # Remove "views" (or other text) and whitespace
        view_text = view_text.split(' ')[0].strip().upper()
        
        # Use regex to find digits and multipliers
        match = re.match(r'([\d\.]+)([KMB]?)', view_text)
        if not match:
            return 0

        value_str, multiplier = match.groups()
        
        try:
            value = float(value_str)
        except ValueError:
            return 0
        
        if multiplier == 'K':
            value *= 1_000
        elif multiplier == 'M':
            value *= 1_000_000
        elif multiplier == 'B':
            value *= 1_000_000_000
            
        return int(value)

    @staticmethod
    def find_top_video(video_elements: list[WebElement]) -> WebElement | None:
        """
        Iterates through a list of video WebElements, parses their view
        counts, and returns the element with the highest view count.
        """
        max_views = -1
        top_video_element = None

        if not video_elements:
            raise ValueError("No video elements found in the provided list.")

        for video in video_elements:
            try:
                # Find view count element relative to the video container
                view_element = video.find_element(*SearchPageLocators.VIEW_COUNT_TEXT)
                view_text = view_element.text
                
                current_views = VideoParser._parse_view_count(view_text)

                if current_views > max_views:
                    max_views = current_views
                    top_video_element = video
            
            except Exception:
                # Ignore elements where view count isn't found (e.g., ads, channels)
                continue
        
        if top_video_element:
            print(f"Identified top video with {max_views:,} views.")
        else:
            print("Could not identify a top video from the results.")
            
        return top_video_element