from status_panel import internet_connection_test,CIPHER_SUITE
from instafollower import InstaFollower,wd
from databaseManager import DatabaseManager
import json
import schedule
import time
from win10toast import ToastNotifier
import subprocess




def run_process():
    connection_test = internet_connection_test("https://www.instagram.com", 5)

    if connection_test:
        bot = InstaFollower(wd)
        credentials = collect_credentials()
        print(credentials)
        for credential in credentials:
            print(credential[0][1])

            driver_check = bot.is_driver_present
            if driver_check:

                dm = DatabaseManager()
                message = dm.fetch_message(credential[0][1])
                enc_pwd = credential[1][0].encode('ascii')
                pass_wrd = CIPHER_SUITE.decrypt(enc_pwd).decode('ascii')
                try:
                    login_success = bot.login(id=credential[0][1], pwd=pass_wrd)
                except:
                    print('Login Exception occured')
                    return
                if login_success:
                    hash_tag_list = bot.hashtags()
                    for tag in hash_tag_list:
                        check = bot.search_with_tag(tag, msg=message)
                        if check == "new":
                            break
                    bot.logout()
                    time.sleep(2)
                else:
                    print("login Interrupted !!!")
                    bot.driver.quit()
            bot.driver.quit()
        bot.abort_web()
    else:
        pass
        messagebox.showinfo("Connection Error", message="No internet connection exists")


def collect_credentials():
    dm = DatabaseManager()
    credentials = []
    selected_ids = dm.select_from_curr_id()
    print(selected_ids)
    for id in selected_ids:
        pwd = dm.collect_password(id[1])
        cred = [id,pwd[0]]
        credentials.append(cred)
    return credentials




with open('./bin/schedule.txt','r') as file:
    data = file.readline()

schedule_data = json.loads(data)
days = schedule_data['days']
for day in days:
    if day == 'mon' :
        schedule.every().monday.at(schedule_data['time']).do(run_process)
    if day == 'tue' :
        schedule.every().tuesday.at(schedule_data['time']).do(run_process)
    if day == 'wed':
        schedule.every().wednesday.at(schedule_data['time']).do(run_process)
    if day == 'thu':
        schedule.every().thursday.at(schedule_data['time']).do(run_process)
    if day == 'fri':
        schedule.every().friday.at(schedule_data['time']).do(run_process)
    if day == 'sat':
        schedule.every().saturday.at(schedule_data['time']).do(run_process)
    if day == 'sun':
        schedule.every().sunday.at(schedule_data['time']).do(run_process)
    if day == 'daily':
        schedule.every().day.at(schedule_data['time']).do(run_process)


notifier = False
# toast = ToastNotifier()

while True:

    with open("./bin/schedule_status.txt", 'r') as file:
        status = file.readline()

    if status == 'true':

        if notifier == False:
            subprocess.call(['MessageBox.bat'])

            # toast.show_toast("Qbot Scheduler","The Scheduler is Active Now")
            notifier = True
        schedule.run_pending()
        time.sleep(1)
    else:
        if notifier == True:
            subprocess.call(['CloseMessageBox.bat'])
            # toast.show_toast("Qbot Scheduler", "The Scheduler is Turned Off")
            notifier = False
        schedule.clear()
        time.sleep(1)



