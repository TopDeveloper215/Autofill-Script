from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, Frame, Text
from tkinter import ttk 
import pyperclip
import time

def Autofill():

    Quantidade = int(quantity_entry.get())
    print(type(Quantidade))
    País = country_var.get()
    full_address = address_text.get("1.0", "end").strip() 
    lines = full_address.splitlines()
    line_1 = lines[0]
    line_2 = lines[1]
    line_3 = lines[2]
    line_3_1, line_3_2 = line_3.split(maxsplit=1)
    line_3_2 = line_3_2.rstrip(",")
    

    browser_options = ChromeOptions()
    browser_options.headless = False
    driver = Chrome(options=browser_options)

    # browser_options = ChromeOptions()
    # browser_options.headless = True
    # browser_options.add_argument("--no-sandbox")
    # browser_options.add_argument("--disable-dev-shm-usage")
    # chrome_service = Service("C:\\chromedriver\\chromedriver.exe")

    # # Pass the service to Chrome
    # driver = Chrome(service=chrome_service, options=browser_options)

    Designação = 'C. AZUL INTERNACIONAL'
    Peso = '2000'

    Nome = 'Amazon Seller'
    Morada = 'A. Godinho'
    NIF_Right = 'R Joao Saraiva 5'
    Telemóvel = '969210320'
    Código_first = '1700'
    Código_second = '227'
    Localidade = 'Lisboa'
    Email = 'azsellpt4@sapo.pt'
    
    Nome_second = line_1
    Morada_second = line_2 
    Telemóvel_second = '123456789'
    Código_Postal_first = line_3_1
    Código_Postal_second = line_3_2
    Localidade_second = line_3_2

    driver.get('https://www.ctt.pt/femss/app/open/forms/shippingRequest.jspx')

    if driver.find_element('id', 'onetrust-accept-btn-handler').is_enabled():
        driver.find_element('id', 'onetrust-accept-btn-handler').click()

    # ---------Page 1---------
    driver.find_element('id', 'productCode').send_keys(Designação)
    time.sleep(2)
    driver.find_element('id', 'quantity').send_keys(Quantidade)
    driver.find_element('id', 'weight').send_keys(Peso)
    driver.find_element('id', 'page-content').click()
    driver.find_element('id', 'createProductButton').click()
    driver.find_element('id', 'termsConditions').click()
    driver.find_element('id', 'destinationInfoAddButtonCreate').click()
    time.sleep(6)

    # -------Tab 1 of Page 2---------
    driver.find_element('id', 'destinationInfoAddSenderNameCreate').send_keys(Nome)
    driver.find_element('id', 'destinationInfoAddSenderAddressLine1Create').send_keys(Morada)
    driver.find_element('id', 'destinationInfoAddSenderAddressLine2Create').send_keys(NIF_Right)
    driver.find_element('id', 'destinationInfoAddSenderMobilePhoneCreate').send_keys(Telemóvel)
    driver.find_element('id', 'destinationInfoAddSenderCp4Create').send_keys(Código_first)
    driver.find_element('id', 'destinationInfoAddSenderCp3Create').send_keys(Código_second)
    driver.find_element('id', 'page-content').click()
    time.sleep(6)
    driver.find_element('id', 'destinationInfoAddSenderPlaceCreate').send_keys(Localidade)
    driver.find_element('id', 'destinationInfoAddSenderEmailCreate').send_keys(Email)

    # -------Tab 2 of Page 2---------

    link = driver.find_element(By.CSS_SELECTOR, '#tabpanelCreate2 a')
    driver.execute_script("arguments[0].click();", link)

    driver.find_element('id', 'destinationInfoAddDestinationCountryCodeCreate').send_keys(País)
    driver.find_element('id', 'page-content').click()
    time.sleep(2)
    driver.find_element('id', 'destinationInfoAddAddresseeNameCreate').send_keys(Nome_second)
    driver.find_element('id', 'destinationInfoAddAddresseeAddressLine1Create').send_keys(Morada_second)
    driver.find_element('id', 'destinationInfoAddAddresseeMobilePhoneCreate').send_keys(Telemóvel_second)
    driver.find_element('id', 'destinationInfoAddAddresseeCpCreate').send_keys(Código_Postal_first)
    driver.find_element('id', 'destinationInfoAddAddresseeCpDescriptionCreate').send_keys(Código_Postal_second)
    driver.find_element('id', 'destinationInfoAddDestinationPlaceCreate').send_keys(Localidade_second)
    driver.find_element('id', 'page-content').click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'destinationInfoAddAddObjectButtonCreate'))
    ).click()

    for _ in range(int(Quantidade) - 1):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'destinationInfoEditAddObjectButtonCreate'))
        ).click()
        time.sleep(6) 
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'createInfoButton'))
    ).click()
    time.sleep(10)
    table = driver.find_element(By.ID, "DestinationInfoDetailTable")
    rows = table.find_elements(By.TAG_NAME, "tr")
    object_codes = []

    for row in rows:
        list_cols = row.find_elements(By.CLASS_NAME, "list-col")
        if len(list_cols) >= 2:
            object_codes.append(list_cols[1].text)
    with open("final_codes.html", "w") as file:
        file.write("<html>\n<head><title>Códigos finales</title></head>\n<body>\n")
        for code in object_codes:
            file.write(f"<p>{code}</p>\n")
        file.write("</body>\n</html>")

    time.sleep(1000)
    

def paste_from_clipboard():
    clipboard_text = pyperclip.paste()  
    address_text.delete("1.0", "end") 
    address_text.insert("1.0", clipboard_text)  
    
# --------GUI App----------

root = Tk()
root.title('main')
root.geometry('880x500')
root.configure(bg='#f0f4f7', padx=40, pady=40)

frame = Frame(root, bg='#f0f4f7')
frame.grid(row=0, column=0, sticky="nsew")

Label(frame, text="Seleccione Cantidad de objetos y país", font=("Helvetica", 16, "bold"), bg='#f0f4f7', fg='#333').grid(row=0, column=0, columnspan=2, pady=(0, 15))

Label(frame, text="Quantidade de objetos:", font=("Helvetica", 14), bg='#f0f4f7').grid(row=1, column=0, sticky='w', padx=(0, 20), pady=10)

quantity_entry = Entry(frame, width=45, font=("Helvetica", 14), borderwidth=2, relief='solid',  highlightcolor="black")
quantity_entry.grid(row=1, column=1, padx=5, pady=10)

Label(frame, text="País:", font=("Helvetica", 14), bg='#f0f4f7').grid(row=2, column=0, sticky='w', padx=(0, 20), pady=10)

country_var = StringVar(root)
countries = [
    'Alemanha (sem territórios extracomunitários)', 'Áustria', 'Bélgica', 'Checa, Rep.', 'Chipre', 'Croácia, Rep.',
    'Dinamarca', 'Eslováquia', 'Eslovénia', 'Espanha (sem territórios extracomunitários)', 'Estónia', 'Finlândia',
    'França', 'Grécia (sem territórios extracomunitários)', 'Holanda', 'Hungria, Rep.', 'Irlanda', 'Itália (sem territórios extracomunitários)',
    'Letónia', 'Lituânia', 'Luxemburgo', 'Malta', 'Polónia, Rep.', 'Suécia'
]  
country_var.set(countries[0]) 
style = ttk.Style()
style.configure('TCombobox', font=("Helvetica", 14), padding=5)

country_dropdown = ttk.Combobox(frame, textvariable=country_var, values=countries, font=("Helvetica", 14), width=30, state="readonly", style='TCombobox')
country_dropdown.grid(row=2, column=1, padx=5, pady=10, sticky="we")

Label(frame, text="Destinatário:", font=("Helvetica", 14), bg='#f0f4f7').grid(row=3, column=0, sticky='nw', padx=(0, 20), pady=10)

address_text = Text(frame, width=45, height=6, font=("Helvetica", 14), wrap='word', borderwidth=2, relief='solid')
address_text.grid(row=3, column=1, padx=5, pady=10)

paste_button = Button(frame, text="Pegar desde PC", font=("Helvetica", 12), command=paste_from_clipboard, width=20, height=2)
paste_button.grid(row=4, column=0, columnspan=2, padx=(0, 250), pady=20)

submit_button = Button(frame, text="Iniciar script", command=lambda: Autofill(), font=("Helvetica", 12, "bold"), bg='#4CAF50', fg='white', width=20, height=2)
submit_button.grid(row=4, column=0, columnspan=2, padx=(455, 0), pady=(0, 0))


root.mainloop()