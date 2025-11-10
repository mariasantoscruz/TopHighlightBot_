from selenium.webdriver.common.by import By

class SearchPageLocators:
    """Locators for the search results page."""

    # Cookie consent button (multi-language support)
    ACCEPT_COOKIES_BUTTON = (
        By.XPATH, 
        "//button[starts-with(@aria-label, 'Accept') or "
        "starts-with(@aria-label, 'Aceptar') or "
        "starts-with(@aria-label, 'Aceitar')]"
    )
    
    # Search input field
    SEARCH_INPUT = (By.NAME, "search_query")
    
    # Search button (multi-language support)
    SEARCH_BUTTON = (
        By.XPATH, 
        "//button[@aria-label='Search' or @aria-label='Pesquisar']"
    )
    
    # A single video result item in the search list
    VIDEO_RESULT_ITEM = (By.CSS_SELECTOR, "ytd-video-renderer")
    
    # The title link within a video item, used to get the href
    VIDEO_TITLE_LINK = (By.CSS_SELECTOR, "a#video-title")
    
    # The text span containing view count (e.g., "1.2M views")
    VIEW_COUNT_TEXT = (By.CSS_SELECTOR, "#metadata-line > span:first-of-type")

class VideoPageLocators:
    """Locators for the video watch page."""
    
    # The HTML5 video player element, used to confirm the page has loaded
    PLAYER_CONTAINER = (By.TAG_NAME, "video")