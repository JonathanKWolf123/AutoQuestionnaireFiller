from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import time
import pyautogui


def handle_question(driver, selector, answer_type='radio', valid_ans_count=1, exclude_other=True):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for answer in elements:
            if answer_type == 'radio':
                # 单选逻辑（保持不变）
                ans = answer.find_elements(By.CSS_SELECTOR, '.ui-radio')
                if exclude_other:
                    ans = [a for a in ans if "其他" not in a.find_element(By.CSS_SELECTOR, '.label').text]
                # 单选直接选择一个即可，无需循环
                if ans:
                    element = random.choice(ans)
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.element_to_be_clickable(element))
                    element.click()
            else:  # checkbox 处理逻辑（重点修改此处）
                ans = answer.find_elements(By.CSS_SELECTOR, '.ui-checkbox')
                if exclude_other:
                    ans = [a for a in ans if "其他" not in a.find_element(By.CSS_SELECTOR, '.label').text]
                # 随机选择 1 到 valid_ans_count 个选项
                if ans:
                    num_to_select = random.randint(1, min(valid_ans_count, len(ans)))
                    available_ans = ans.copy()
                    random.shuffle(available_ans)
                    selected_ans = available_ans[:num_to_select]
                    for element in selected_ans:
                        wait = WebDriverWait(driver, 10)
                        wait.until(EC.element_to_be_clickable(element))
                        element.click()
                        # 点击后等待状态更新（可选：根据页面响应时间调整）
                        time.sleep(0.5)
            time.sleep(random.randint(0, 1))
    except NoSuchElementException:
        print(f"未找到 {selector} 对应的问题元素。")
    except TimeoutException:
        print(f"处理 {selector} 问题时超时，元素可能不可点击。")


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def tiankong(driver, num):
    index = ["A", "B", "C", "D", "E"]
    answer = {"A": "无", "B": "好", "C": "good", "D": "我不留言你能奈我何", "E": "暂无"}
    try:
        input_element = driver.find_element(By.CSS_SELECTOR, f'#q{num}')
        input_element.send_keys(answer.get(index[random.randint(0, len(index) - 1)]))
    except NoSuchElementException:
        print(f"未找到第 {num} 题的填空题输入框。")


def renzheng(driver):
    wait = WebDriverWait(driver, 10)
    try:
        bth = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                         '#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0')))
        bth.click()
        time.sleep(1)
        rectBottom = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rectBottom')))
        rectBottom.click()
        time.sleep(2)
        huakuai()
    except TimeoutException:
        print("本次未出现认证界面，继续进行后续操作")


def huakuai():
    pyautogui.moveTo(random.randint(494, 496), 791, 0.2)
    time.sleep(1)
    pyautogui.dragTo(random.randint(888, 890), 791, 1)
    time.sleep(1)
    pyautogui.click(random.randint(652, 667), random.randint(793, 795))
    time.sleep(1)
    pyautogui.moveTo(random.randint(494, 496), 791, 0.2)
    time.sleep(1)
    pyautogui.dragTo(random.randint(888, 890), 791, 1)


def gundong(driver, distance):
    js = "var q=document.documentElement.scrollTop=" + str(distance)
    driver.execute_script(js)
    time.sleep(1)


def zonghe(times):
    for i in range(0, times):
        url_survey = 'https://www.wjx.cn/vm/mWSd3ci.aspx'
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.binary_location = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe'
        service = Service(r"D:\Google\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=option)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

        driver.get(url_survey)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#div1')))

        # 按顺序定义所有题目信息
        questions = [
            ('#div1 > div.ui-controlgroup.column1', 'radio', 1),
            ('#div2 > div.ui-controlgroup.column1', 'radio', 1),
            ('#div3 > div.ui-controlgroup.column1', 'radio', 1),
            ('#div4 > div.ui-controlgroup.column1', 'checkbox', 4),
            ('#div5 > div.ui-controlgroup.column1', 'radio', 1),
            ('#div6 > div.ui-controlgroup.column1', 'checkbox', 4),
            ('#div7 > div.ui-controlgroup.column1', 'checkbox', 5),
        ]

        for selector, answer_type, count in questions:
            handle_question(driver, selector, answer_type, count)
            # 每完成一题滚动一下页面
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                scroll_to_element(driver, element)
            except NoSuchElementException:
                pass

        gundong(driver, 1200)
        time.sleep(2)

        # 处理填空题
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#q8')))
            tiankong(driver, 8)
        except TimeoutException:
            print("未找到第8题的填空题元素，可能页面加载异常。")

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ctlNext')))
            driver.find_element(By.CSS_SELECTOR, '#ctlNext').click()
        except TimeoutException:
            print("未找到下一步按钮，可能页面加载异常。")

        renzheng(driver)

        try:
            success_msg = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="divdsc" and contains(text(), "您的答卷已经提交，感谢您的参与！")]'))
            )
            if success_msg:
                print('问卷提交成功！')
        except TimeoutException:
            print('未检测到提交成功提示，可能出现问题。')

        print(f'已经提交了{i + 1}次问卷')
        driver.quit()


if __name__ == "__main__":
    zonghe(1)
    