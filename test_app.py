from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_task_lifecycle():
    # Setup headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        # Assuming the app is running locally on port 5000 during the Jenkins pipeline
        driver.get("http://localhost:5000")
        
        # 1. Add a Task
        test_task_name = "Automated Selenium Task"
        input_box = driver.find_element(By.ID, "taskInput")
        input_box.send_keys(test_task_name)
        driver.find_element(By.ID, "addButton").click()
        time.sleep(1) # Wait for page reload

        # 2. Check if added
        page_text = driver.page_source
        assert test_task_name in page_text, "Task was not added to the page!"

        # 3. Delete the Task
        # Find the list item containing our specific task, then find its delete link
        task_items = driver.find_elements(By.CLASS_NAME, "task-item")
        for item in task_items:
            if test_task_name in item.text:
                item.find_element(By.CLASS_NAME, "delete-link").click()
                break
        
        time.sleep(1)
        
        # 4. Verify Deletion
        page_text = driver.page_source
        assert test_task_name not in page_text, "Task was not deleted!"
        
        print("Test Passed: Task added, verified, and deleted successfully.")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_task_lifecycle()
