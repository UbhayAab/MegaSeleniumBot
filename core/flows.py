# core/flows.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.chatgpt_utils import generate_content_with_chatgpt

def perform_linkedin_post(driver, job_content):
    """Generate content with ChatGPT and post it on LinkedIn."""
    # Hardcoded custom prompt for LinkedIn
    prompt = f"Write a professional LinkedIn post about: {job_content}. Keep it concise, engaging, and under 200 words use bold and big titles, and good formatting."
    
    # Generate content using ChatGPT
    generated_content = generate_content_with_chatgpt(driver, prompt)
    
    # Switch to LinkedIn tab (tab 1)
    driver.switch_to.window(driver.window_handles[1])
    
    # Go directly to the post creation URL
    driver.get("https://www.linkedin.com/in/ubhay-anand-vatsa/overlay/create-post/")
    
    # Find the post input field (replace with actual selector)
    post_input = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div")  # Placeholder
    post_input.clear()
    post_input.send_keys(generated_content)
    
    # Find and click the post button (replace with actual selector)
    post_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")  # Placeholder
    # post_button.click()
    
    print(f"Posted on LinkedIn: {generated_content}")
    return generated_content  # Optional, for logging or verification