<<<<<<< HEAD
import os
import pickle
from time import sleep
from random import randint
from selenium import webdriver
from html2text import html2text
from selenium.webdriver.common.keys import Keys

os.chdir(r'C:\Users\Samuel\Google Drive\DnD\Data')

credentials = pickle.load(open('Login - Roll20.pkl', 'rb'))
username = credentials['username']
password = credentials['password']

driver = webdriver.Chrome(r'chromedriver.exe')
driver.set_page_load_timeout('10')
driver.get('http://roll20.net')

driver.find_element_by_id('menu-signin').click()
sleep(1)

driver.find_element_by_id('input_login-email').send_keys(username)
sleep(1)

driver.find_element_by_id('input_login-password').send_keys(password)
sleep(1)

driver.find_element_by_id('input_login-password').send_keys(Keys.ENTER)
sleep(5)


# SRD

driver.get('https://roll20.net/compendium/dnd5e/Monsters%20List#content')

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass

bad_list = ['Monsters', 'BookIndex', 'Index', 'License']    
link_list = list(set(link_list))
link_list = [link for link in link_list if not any(bad in link for bad in bad_list)]

monster_list = []

for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    monster_list.append(monster)
    
    print(f'monster: {monster}')
    
    driver.get(link)
    sleep(randint(3, 6))
    
    out = html2text(driver.page_source)
    
    with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
        file.write(out)
    


# Monster Manual

driver.get('https://app.roll20.net/compendium/dnd5e/Monsters%20List?Source=2#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')


# Volo

driver.get('https://app.roll20.net/compendium/dnd5e/Monsters%20List?Source=1#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')



# Mordenkainen

driver.get('https://roll20.net/compendium/dnd5e/Monsters%20List?Source=4#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')















































=======
import os
import pickle
from time import sleep
from random import randint
from selenium import webdriver
from html2text import html2text
from selenium.webdriver.common.keys import Keys

os.chdir(r'C:\Users\Samuel\Google Drive\DnD\Data')

credentials = pickle.load(open('Login - Roll20.pkl', 'rb'))
username = credentials['username']
password = credentials['password']

driver = webdriver.Chrome(r'chromedriver.exe')
driver.set_page_load_timeout('10')
driver.get('http://roll20.net')

driver.find_element_by_id('menu-signin').click()
sleep(1)

driver.find_element_by_id('input_login-email').send_keys(username)
sleep(1)

driver.find_element_by_id('input_login-password').send_keys(password)
sleep(1)

driver.find_element_by_id('input_login-password').send_keys(Keys.ENTER)
sleep(5)


# SRD

driver.get('https://roll20.net/compendium/dnd5e/Monsters%20List#content')

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass

bad_list = ['Monsters', 'BookIndex', 'Index', 'License']    
link_list = list(set(link_list))
link_list = [link for link in link_list if not any(bad in link for bad in bad_list)]

monster_list = []

for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    monster_list.append(monster)
    
    print(f'monster: {monster}')
    
    driver.get(link)
    sleep(randint(3, 6))
    
    out = html2text(driver.page_source)
    
    with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
        file.write(out)
    


# Monster Manual

driver.get('https://app.roll20.net/compendium/dnd5e/Monsters%20List?Source=2#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')


# Volo

driver.get('https://app.roll20.net/compendium/dnd5e/Monsters%20List?Source=1#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')



# Mordenkainen

driver.get('https://roll20.net/compendium/dnd5e/Monsters%20List?Source=4#content')
sleep(5)

link_list = []

for link in driver.find_elements_by_xpath('.//a'):
    try:
        if 'dnd5e' in link.get_attribute('href'):
            link_list.append(link.get_attribute('href'))
    except TypeError:
        pass
    
link_list = list(set(link_list))
link_list = [link for link in link_list 
             if not any(bad in link for bad in bad_list)]
    
for link in link_list:   
    monster = link[link.find('dnd5e/'):][6:].replace('%20', ' ')
    
    if monster not in monster_list:
        monster_list.append(monster)
        
        print(f'monster: {monster}')
        
        driver.get(link)
        sleep(randint(3, 6))
        
        out = html2text(driver.page_source)
        
        with open(f'Monsters\\{monster}.txt', 'w', encoding='utf8') as file:
            file.write(out)
            
    else:
        print(f'Monster {monster} already captured')















































>>>>>>> c3ba50651ae962bd77cab733eff5e7c8b805e848
