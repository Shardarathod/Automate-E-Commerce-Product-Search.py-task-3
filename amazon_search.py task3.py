# amazon_search.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.amazon.com/")

# Wait helper
wait = WebDriverWait(driver, 10)

# Search for "laptop"
search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_box.send_keys("laptop")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")))

# Extract product names and prices
products = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")
results = []

for product in products[:10]:  # top 10 products
    try:
        name = product.find_element(By.CSS_SELECTOR, "h2 a span").text
    except:
        name = "N/A"
    try:
        price_whole = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
        price = f"${price_whole}.{price_fraction}"
    except:
        price = "N/A"
    results.append({"name": name, "price": price})

# Print results
for idx, r in enumerate(results, 1):
    print(f"{idx}. {r['name']} - {r['price']}")

# Close browser
driver.quit()
