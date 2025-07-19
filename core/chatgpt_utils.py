import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def generate_content_with_chatgpt(driver, prompt):
    """Input a prompt into ChatGPT and return the generated response using two methods."""
    # Switch to ChatGPT tab (tab 0) and ensure we start fresh
    driver.switch_to.window(driver.window_handles[0])
    driver.get("https://chatgpt.com/")
    
    try:
        # Wait for the input field to be present and interactable
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/div[1]/div[1]/div/div/div"))
        )
        input_field.clear()
        input_field.send_keys(prompt)
        input_field.send_keys(Keys.RETURN)
        
        # Wait for the response to appear (check for output div)
        output_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/main/div/div/div[1]/div/div/div[2]/article[2]/div/div/div/div/div[1]/div/div"))
        )
        
        # Method 1: Get text directly from the output div
        direct_output = output_div.text
        print("=== Direct Output (from div) ===")
        print(direct_output)
        print("================================")
        
        # Method 2: Use the copy button to get the clipboard content
        copy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/main/div/div/div[1]/div/div/div[2]/article[2]/div/div/div/div/div[2]/div/div/button[1]"))
        )
        copy_button.click()
        
        # Retrieve clipboard content (requires pyperclip for cross-platform clipboard access)
        try:
            import pyperclip
            clipboard_output = pyperclip.paste()
            print("=== Clipboard Output (from copy button) ===")
            print(clipboard_output)
            print("================================")
        except ImportError:
            print("pyperclip not installed. Skipping clipboard method.")
            clipboard_output = None
        
        # Return both outputs for flexibility (use clipboard_output if available, else direct_output)
        return {
            "direct_output": direct_output,
            "clipboard_output": clipboard_output
        }
        
    except TimeoutException as e:
        print(f"Error interacting with ChatGPT: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in ChatGPT interaction: {e}")
        return None