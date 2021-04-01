try:
    from selenium import webdriver
    import datetime
    import time
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.select import Select
    import os 
    import json

    
    from subprocess import call

    CURR_DIR = os.path.dirname(os.path.realpath(__file__))

    def clear():
        # check and make call for specific operating system
        _ = os.system('clear' if os.name =='posix' else 'cls')

    def tickAttendanceProcess(username,password,classcode):
        try:
            driver = webdriver.Chrome(os.path.join(CURR_DIR,'chromedriver.exe'))
            driver.get('https://ufuture.uitm.edu.my/users/loginForm/1')
            #//*[@id="UserUsername"]
            try:
                login_username = driver.find_element_by_xpath('//*[@id="UserUsername"]')
                login_password   = driver.find_element_by_xpath('//*[@id="UserPassword"]')
                login_button = driver.find_element_by_xpath('//*[@id="UserLoginFormForm"]/div[4]/div/button')

                login_username.send_keys(username)
                login_password.send_keys(password)
                time.sleep(1.3)
                login_button.click()


                try:
                    driver.get('https://ufuture.uitm.edu.my/OnlineClasses/index/' + str(classcode))
                    sel = Select(driver.find_element_by_xpath('//*[@id="onlineclassTbl_length"]/label/select'))

                    sel.select_by_visible_text("100")
                    table = driver.find_element_by_xpath('//*[@id="onlineclassTbl"]/tbody')
                    rows = table.find_elements_by_tag_name('tr')

                    for row in rows:
                        try:
                            #//*[@id="onlineclassTbl"]/tbody/tr[1]/td[11]/span
                            status = row.find_elements_by_tag_name('td')[10].find_element_by_tag_name('span').text
                            if status == "Active":
                                view_button = row.find_elements_by_tag_name('td')[9].find_element_by_tag_name('a')
                                view_button.click()
                                try:
                                    if len(driver.find_elements_by_xpath('//*[@id="hadir"]')) > 0:
                                        attend_button = driver.find_element_by_xpath('//*[@id="hadir"]')
                                        attend_button.click()

                                        if len(driver.find_elements_by_xpath('//*[@id="listAttendance"]/tbody/tr/td[6]/i')) > 0:
                                            driver.close()
                                            return "Class Attended! (" + classcode + ")"
                                        else:
                                            driver.close()
                                            return "Error: After Attend"
                                    elif len(driver.find_elements_by_xpath('//*[@id="listAttendance"]/tbody/tr/td[6]/i')) > 0:
                                        driver.close()
                                        return "Class Attended!"
                                    else:
                                        driver.close()
                                        return "Error: Not click attend button"
                                except Exception as e:
                                    driver.close()
                                    return "In Attendance Page Exception : " + str(e)
                        except Exception as e:
                            driver.close()
                            return "Row Exception : " + str(e)
                    driver.close()
                    return "No Active Class"
                except Exception as e:
                    driver.close()
                    return "Table Exception : " + str(e)
            except Exception as e:
                driver.close()
                return "Login Exception : " + str(e)
        except Exception as e:
            driver.close()
            return "Driver Exception : " + str(e)

    option = 0

    with open('config.json') as f:
        

        data = json.loads(f.read())

        username = data["matricNo"]
        password = data["password"]


        while option != -1:
            clear()
            print("Welcome to Tick Attendance Automation by Irfan-Amy!")
            print("Visit github repository if you want to download original binary file : https://github.com/Irfan-amy/AutoSignAttendance-Ufuture")

            print()
            print("Choose option:")
            i = 0
            
            
            for val in data["class"]:
                print(str(i) + ": " + "Attend Class (" + val + ")")
                i += 1
            print()
            print("-1 : Exit")
            print()
            print("Enter option : ",end='')

            option = int(input())
            if option == -1:
                exit()
            else: 
                clear()
                print("Processing..")
                print()
                print(tickAttendanceProcess(username,password, data["class"][option]))
                print()
                print("0 : Back")
                print("-1 : Exit")
                print("Enter option : ",end='')

                option = int(input())
                
    exit()
except Exception as e:
    print(str(e))
    input()


