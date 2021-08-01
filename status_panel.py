
from tkinter import *
from tkinter import messagebox
from instafollower import internet_connection_test,InstaFollower,wd
from databaseManager import DatabaseManager
import threading
from cryptography.fernet import  Fernet
import time
import json
import schedule

KEY = b'J1la7UmGEikSFvLlCRBWJPnUQr1iViDP5rzH4dH5q9s='
CIPHER_SUITE = Fernet(KEY)

ITEM_NUM = 0
PANEL_HEIGHT = 400
PANEL_WIDTH = 3*304
FONT = "Times 14"
BG_BLUE = "#038ABF"
IS_STATUS_PANEL_OPEN = False
LAVENDER = "#E6E6FA"


def read_schedule_status():
    with open("./bin/schedule_status.txt", "r") as file:
        status = file.readline()
    return status

class StatusPanel:


        def __init__(self):
            global IS_STATUS_PANEL_OPEN
            if IS_STATUS_PANEL_OPEN == False:

                IS_STATUS_PANEL_OPEN = True
                self.statusPanel = Toplevel(bg=LAVENDER)
                panel = self.statusPanel
                self.screen_width = panel.winfo_screenwidth()
                self.screen_height = panel.winfo_screenheight()
                panel.geometry(f"{PANEL_WIDTH}x{PANEL_HEIGHT}+"
                               f"{int((self.screen_width-PANEL_WIDTH)/2)}+{int((self.screen_height-PANEL_HEIGHT)/2)}")

                self.h_canvas = Canvas(panel, width=3 * PANEL_WIDTH, height=73, bg=BG_BLUE)
                self.h_canvas.create_text(460, 35, text="Status", font=FONT, fill="white")
                self.h_canvas.place(x=-2, y=0)

                self.run_time_schedule(panel)

                btn_add = Button(panel,text="Add",width=12,command=self.insert_item)
                btn_add.place(x=405,y=213)

                btn_remove = Button(panel,text="Remove",width=12,command=self.remove_curr_id)
                btn_remove.place(x=405,y=243)

                # btn_add_all = Button(panel,text="Add All",width=12)
                # btn_add_all.place(x=405,y=273)

                btn_run_process = Button(panel, text="Run Process", width=12,command = lambda: self.run_process_in_thread())
                btn_run_process.place(x=529, y=310)

                btn_terminate_process = Button(panel, text="Terminate Process",command=self.terminate_process)
                btn_terminate_process.place(x=642, y=310)

                insta_acc_lbl = Label(panel, text="Insta account list :", bg=LAVENDER)
                insta_acc_lbl.place(x=84, y=176)
                self.account_list = Listbox(panel, width=48, height=6,selectmode=MULTIPLE)
                try:
                    self.ids = self.instaAccListElement()
                    i = 0
                    for val in self.ids:
                        self.account_list.insert(i,val[1])
                        i =+ 1
                except:
                    pass
                self.account_list.place(x=84, y=203)

                curr_acc_lbl = Label(panel,text="Current Insta account :",bg=LAVENDER)
                curr_acc_lbl.place(x=529,y=176)
                #current Insta Account
                self.curr_account_list = Listbox(panel, width=48, height=6)
                dm = DatabaseManager()
                items = dm.select_from_curr_id()
                i = 0
                for item in items:
                    self.curr_account_list.insert(i,item[1])
                    i += 1
                self.curr_account_list.place(x=529, y=203)

                panel.protocol('WM_DELETE_WINDOW', self.makeFalseTrue)
                panel.resizable(0, 0)

        # def selection(self):
            # called by insert_item() method
            # this method collects the IDs selected in the Insta Acc list

        def insert_item(self):
            # item_selected = []
            items = self.account_list.curselection()
            for item in items:
                # database segment
                dm = DatabaseManager()
                acc_id = self.account_list.get(item)
                self.curr_account_list.insert(item, acc_id)
                dm.insert_in_curr_id(acc_id)
                # item_selected.append(acc_id)
            # item_selected = dm.select_from_curr_id()
            # i = 0
            # for item in item_selected:
            #
            #     i += 1
            # self.collect_selected_ids(collect_selected_items)

        def remove_curr_id(self):
            id = self.curr_account_list.curselection()
            id_val = self.curr_account_list.get(id)
            dm = DatabaseManager()
            dm.delete_from_curr_id(id_val)
            self.curr_account_list.delete(id)


        def makeFalseTrue(self):
            global IS_STATUS_PANEL_OPEN
            IS_STATUS_PANEL_OPEN = False
            self.statusPanel.destroy()


        def listElement(self):
            pass

        def grab_element(self):
            return self.ids


        def instaAccListElement(self):
            dm = DatabaseManager()
            data = dm.fetch_all()
            return data

        def run_process_in_thread(self):
            self.thread = threading.Thread(target=self.run_process)
            try:
                self.thread.start()
            except:
                print('Exception Occured')

        def collect_selected_ids(self,items):
            self.selected_ids =[]
            for item in items:
                self.selected_ids.append(item)
            print(self.selected_ids)

        def collect_credentials(self):
            dm = DatabaseManager()
            credentials = []
            selected_ids = dm.select_from_curr_id()
            for id in selected_ids:
                pwd = dm.collect_password(id[1])
                cred = [id,pwd[0]]
                credentials.append(cred)
            return credentials

        def run_time_schedule(self,panel):
           SchedulePanel(panel)

        def run_process(self):
            connection_test = internet_connection_test("https://www.instagram.com", 20)

            if connection_test:
                for credential in self.collect_credentials():
                    self.bot = InstaFollower(wd)

                    bot = self.bot
                    driver_check = bot.is_driver_present
                    if driver_check:

                        dm = DatabaseManager()
                        message = dm.fetch_message(credential[0][1])
                        enc_pwd = credential[1][0].encode('ascii')
                        pass_wrd = CIPHER_SUITE.decrypt(enc_pwd).decode('ascii')
                        try:
                            login_success = bot.login(id=credential[0][1],pwd=pass_wrd)
                        except:
                            print('Login Exception occured')
                            return
                        if login_success:
                            hash_tag_list = bot.hashtags()
                            for tag in hash_tag_list:
                                check = bot.search_with_tag(tag,msg=message)
                                if check == "new":
                                    break
                            bot.logout()
                            time.sleep(2)
                        else:
                            print("login Interrupted !!!")
                            bot.driver_quit()
                    bot.driver_quit()
                self.bot.abort_web()
            else:
                messagebox.showinfo("Connection Error",message="No internet connection exists")

        def terminate_process(self):
            self.bot.abort_web()


        def scheduled_run(self):
            print("hit")


class SchedulePanel(StatusPanel):

    def __init__(self,statusPanel):
        self.panel = statusPanel
        scheduleLabel = Label(statusPanel, text="Set Schedule :", bg=LAVENDER)
        scheduleLabel.place(x=529, y=88)
        self.mon = StringVar()
        monCB = Checkbutton(statusPanel, text="Mon",variable=self.mon, onvalue="mon",offvalue=0, bg=LAVENDER,activebackground=LAVENDER)
        monCB.place(x=529, y=113)
        monCB.deselect()
        self.tue = StringVar()
        tueCB = Checkbutton(statusPanel, text="Tue",variable=self.tue, onvalue="tue",offvalue=0, bg=LAVENDER,activebackground=LAVENDER)
        tueCB.place(x=589, y=113)
        tueCB.deselect()
        self.wed = StringVar()
        wedCB = Checkbutton(statusPanel, text="Wed",variable=self.wed, onvalue="wed",offvalue=0, bg=LAVENDER, activebackground=LAVENDER)
        wedCB.place(x=649, y=113)
        wedCB.deselect()
        self.thu = StringVar()
        thuCB = Checkbutton(statusPanel, text="Thu",variable=self.thu, onvalue="thu",offvalue=0, bg=LAVENDER, activebackground=LAVENDER)
        thuCB.place(x=709, y=113)
        thuCB.deselect()
        self.fri = StringVar()
        friCB = Checkbutton(statusPanel, text="Fri",variable=self.fri, onvalue="fri",offvalue=0, bg=LAVENDER, activebackground=LAVENDER)
        friCB.place(x=529, y=138)
        friCB.deselect()
        self.sat = StringVar()
        satCB = Checkbutton(statusPanel, text="Sat",variable=self.sat, onvalue="sat",offvalue=0, bg=LAVENDER, activebackground=LAVENDER)
        satCB.place(x=589, y=138)
        satCB.deselect()
        self.sun = StringVar()
        sunCB = Checkbutton(statusPanel, text="Sun",variable=self.sun, onvalue="sun",offvalue=0, bg=LAVENDER, activebackground=LAVENDER)
        sunCB.place(x=649, y=138)
        sunCB.deselect()
        self.daily = StringVar()
        items = [monCB,tueCB,wedCB,thuCB,friCB,satCB,sunCB]
        dailyCB = Checkbutton(statusPanel, text="Daily",variable=self.daily, onvalue="daily",offvalue=0, bg=LAVENDER, activebackground=LAVENDER,command=lambda: self.deactive_days(items))
        dailyCB.place(x=709, y=138)
        dailyCB.deselect()

        ##### SET TIME
        #####
        timerLabel = Label(statusPanel, text="Set Time :", bg=LAVENDER)
        timerLabel.place(x=349, y=88)
        self.hrSB = Spinbox(statusPanel, from_=0, to=23, width=5)
        self.hrSB.place(x=349, y=113)
        hrSBlbl = Label(statusPanel, text="Hr", bg=LAVENDER)
        hrSBlbl.place(x=349, y=138)
        self.minSB = Spinbox(statusPanel, from_=0, to=59, width=5)
        self.minSB.place(x=419, y=113)
        minSBlbl = Label(statusPanel, text="Min", bg=LAVENDER)
        minSBlbl.place(x=419, y=138)

        self.running_schedule_label = Label(statusPanel)
        self.running_schedule_label.place(x=84,y=120)
        self.schedule_status_label = Label(statusPanel)
        self.schedule_status_label.place(x=84, y=160)
        self.create_schedule_label()

        self.st_schedule = Button(statusPanel, text="Store Schedule", width=14, command=self.store_schedule)
        self.st_schedule.place(x=84, y=100)


        self.run_schedule = Button(statusPanel, text="Run",command=lambda: self.schedule_status("true"))
        self.run_schedule.place(x=204, y=100)
        if read_schedule_status() == "true":
            self.run_schedule.config(state=DISABLED)

        self.stop_schedule = Button(statusPanel, text="Stop",command=lambda: self.schedule_status("false"))
        self.stop_schedule.place(x=249, y=100)

    def schedule_status(self,txt):
        with open("./bin/schedule_status.txt","w") as file:
            file.write(txt)
        if txt == "true":
            self.run_schedule.config(state=DISABLED)

        else:
            self.run_schedule.config(state=ACTIVE)
        self.create_schedule_label()


    # def run_schedule(self):


    def create_schedule_label(self):
        running_schedule = self.load_schedule()
        status = read_schedule_status()
        days = []
        for day in running_schedule['days']:
            if day != '0':
                days.append(day)
        print(days)
        self.running_schedule_label.destroy()
        self.schedule_status_label.destroy()
        self.running_schedule_label = Label(self.panel,bg=LAVENDER)
        self.running_schedule_label.place(x=84, y=135)
        self.schedule_status_label = Label(self.panel,bg=LAVENDER)
        self.schedule_status_label.place(x=84, y=155)
        self.running_schedule_label.config(text=f'days: {days} | time: {running_schedule["time"]} hrs')
        self.schedule_status_label.config(text=f'Schedule Running: {status}')

    def store_schedule(self):
        if self.daily.get() == "daily":
            days = ["daily"]
        else:
            days = [self.mon.get(),self.tue.get(),self.wed.get(),self.thu.get(),self.fri.get(),self.sat.get(),self.sun.get()]
            print(days)
        hr = self.hrSB.get()
        min = self.minSB.get()
        schedule = {
            "days" : days,
            "time" : f"{hr}:{min}"
        }
        with open("./bin/schedule.txt","w") as file:
            file.write(json.dumps(schedule))
        print(schedule)
        self.create_schedule_label()
        self.load_schedule()

    def load_schedule(self):
        with open("./bin/schedule.txt","r") as file:
            data = file.readline()

        schedule = json.loads(data)
        return schedule

    def deactive_days(self,items):
        if self.daily.get() == "daily":
            for item in items:
                item.config(state=DISABLED)
                item.deselect()

        else:
            for item in items:
                item.config(state=NORMAL)


