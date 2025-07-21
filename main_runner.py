import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.browser_launcher import launch_browser_for_user, open_core_tabs
from core.flows import perform_linkedin_post  # Import the new flow

# Directory where Telegram bot saves JSON jobs
JOB_DIR = os.path.abspath("jobs")
print(f"Monitoring directory: {JOB_DIR}")

# Dictionary to store Chrome driver instances for each user
user_drivers = {}

class JobHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".json"):
            print(f"New job detected: {event.src_path}")
            process_job(event.src_path)

observer = Observer()
observer.schedule(JobHandler(), JOB_DIR, recursive=False)
observer.start()
print("Main runner started. Listening for new jobs...")

drivers = {}

def get_or_launch_driver(user):
    if user not in drivers:
        driver = launch_browser_for_user(user)
        open_core_tabs(driver)  # Opens ChatGPT, LinkedIn, X.com
        drivers[user] = driver
    return drivers[user]

def process_job(job_file):
    try:
        with open(job_file, "r") as f:
            job = json.load(f)
        
        user = job["user"]
        job_type = job["type"]
        job_content = job["content"]
        
        driver = get_or_launch_driver(user)
        
        if job_type == "linkedin":
            perform_linkedin_post(driver, job_content)
        elif job_type == "tweet":
            print("Tweet flow not implemented yet.")  # Placeholder
        else:
            print(f"Unknown job type: {job_type}")
        
        os.remove(job_file)
    except Exception as e:
        print(f"Error processing job {job_file}: {e}")

if __name__ == "__main__":
    # Ensure jobs directory exists
    os.makedirs(JOB_DIR, exist_ok=True)
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        # Clean up: close all Chrome instances
        for driver in user_drivers.values():
            driver.quit()
        print("Main runner stopped.")
    observer.join()

def perform_tweet(driver, content):
    """Post a tweet using the Twitter tab."""
    driver.switch_to.window(driver.window_handles[2])  # Twitter tab
    print(f"Tweeting: {content}")
    # TODO: Add Selenium logic to post the tweet

def perform_connect(driver, content, profile_links):
    """Send LinkedIn connect requests."""
    driver.switch_to.window(driver.window_handles[1])  # LinkedIn tab
    for link in profile_links:
        print(f"Sending connect request to {link} with message: {content}")
        # TODO: Add Selenium logic to send connect requests

def perform_tag(driver, content, profile_links):
    """Tag Twitter accounts in a tweet."""
    usernames = [link.split('/')[-1] for link in profile_links]
    tweet_content = f"{content} {' '.join(['@' + user for user in usernames])}"
    perform_tweet(driver, tweet_content)

def perform_comment_twitter(driver, content, profile_links):
    """Comment on latest tweets."""
    driver.switch_to.window(driver.window_handles[2])  # Twitter tab
    for link in profile_links:
        print(f"Commenting on {link}’s latest tweet: {content}")
        # TODO: Add Selenium logic to comment on tweets