from plyer import notification
import smtplib
import time
from tkinter import *
import bs4
import urllib.request

# function for sending desktop notifications
def send_notification():
    title = 'Price Drop Alert!!'
    message = "The product you've been looking for is now available at a lower price.Go check it out!!"

    notification.notify(title=title,
                        message=message,
                        app_icon=None,
                        timeout=5,
                        toast=True)

# function for sending email
def send_mail(receiver):
    sender_mail = 'amazonpricetracker760@gmail.com'
    rec_mail = receiver
    password = 'Praveen123@'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    # print('Login Success')
    message = "Dear user\n     The product you've been looking for is now available at a lower price.Go check it out!!\n      Thank you"
    server.sendmail(sender_mail, rec_mail, message)
    # print('Success')

# function get product price
def get_price():
    product_link = entry1.get()
    affordable_price = float(entry3.get())
    rec_mail = entry2.get()
    sauce = urllib.request.urlopen(product_link).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")
    try:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
        except:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        if '-' in price:
            price = soup.find("span", attrs={'id': 'priceblock_saleprice'}).string.strip()
        # print(price)
    except:
        print('Sorry! Could not find current price')
    price = price[2:]
    price = price[:-3]
    price = price.replace(',', '', price.count(','))
    price = float(price)
    return price


# function for submit button
def submit_button():
    price_list = []
    print('Success your details are submitted.')
    while 1:
        price_list.append(get_price())
        time.sleep(3600)
        if len(price_list) > 1 and price_list[-1] < price_list[-2]:
            break
    for _ in range(10):
        send_notification()
        time.sleep(3600)
    for _ in range(3):
        send_mail(entry2.get())
        time.sleep(7200)



if __name__ == '__main__':

    # user interface using Tkinter
    root = Tk()
    root.geometry('400x400')
    root.title('Input Window')
    label1 = Label(root, text='Enter your product link:', font=('Italic', 10))
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = Entry(root, width=30)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    label2 = Label(root, text='Enter mail id to get notified:', font=('Bold', 10))
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = Entry(root, width=30)
    entry2.grid(row=1, column=1, padx=10, pady=10)
    label3 = Label(root, text='Enter your affordable price:', font=('Italic', 10))
    label3.grid(row=2, column=0, padx=10, pady=10)
    entry3 = Entry(root, width=30)
    entry3.grid(row=2, column=1, padx=10, pady=10)
    Button(root, text='submit', command=submit_button).grid(row=3, column=1, padx=10, pady=10)
    root.configure(bg='lightgrey')
    root.mainloop()





