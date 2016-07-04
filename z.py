import Tkinter as tk
import tkMessageBox as tkm
import sys
import os
import zbar
from datetime import datetime as dt
import multiprocessing as mp
import time
import ctypes
import socket

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.initialize()
        self.root.mainloop()
        
    def initialize(self):
        self.root.title('Windows lol')
        self.root.geometry('900x1000')
        self.root.configure(bg = '#333333')
        self.f_log = tk.Frame(self.root)
        self.f_cur = tk.Frame(self.root)
        self.f_but = tk.Frame(self.root)
        self.numb = 'Number'
        self.name = 'Name'
        self.date = 'Date'
        self.activated = mp.Value('d', False)
        self.runningProc = mp.Value('d', False)
        
        self.logwidth = 90
        self.f_log.configure(width = self.logwidth)
        self.curwidth = 100
        self.f_cur.configure(width = self.curwidth)

        self.log_make()
        self.but_make()
        self.cur_make()

        host = '192.168.0.42'
        port = 12289

        cmdOpenMain = '01WWRD00220,01,0001\r\n'
        cmdCloseMain = '01WWRD00220,01,0000\r\n'
        cmdOpenERIT = '01WWRD00611,01,0001\r\n'
        cmdCloseERIT = '01WWRD00611,01,0000\r\n'

        cmdIL0Main = '01WWRD00133,01,0000\r\n'
        cmdILMain = '01WWRD00133,01,0001\r\n'
        cmdIL0ERIT = '01WWRD00610,01,0000\r\n'
        cmdILERIT = '01WWRD00610,01,0001\r\n'

        if sys.argv[1] == 'MAIN':
            self.cmdOpen = cmdOpenMain
            self.cmdClose = cmdCloseMain
            self.cmdIL0 = cmdIL0Main
            self.cmdIL = cmdILMain
        elif sys.argv[1] == 'ERIT':
            self.cmdOpen = cmdOpenERIT
            self.cmdClose = cmdCloseERIT
            self.cmdIL0 = cmdIL0ERIT
            self.cmdIL = cmdILERIT
        else:
            print "You need argument ['MAIN' or 'ERIT']"
            print "python z.py MAIN, for example"
            sys.exit('Argument Error in initialize method.')
            
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def log_make(self):
        fg_color = '#5af051'
        self.sbar = tk.Scrollbar(self.f_log)
        self.sbar.configure(bg = '#222222', activebackground = '#444444', troughcolor = '#ffffff')
        self.sbar.pack(side = 'right', fill = 'y')
        self.loglist_numb = tk.Listbox(self.f_log, yscrollcommand = self.sbar.set, selectmode = 'multiple', bg = '#000000',
                                       fg = fg_color)
        self.loglist_name = tk.Listbox(self.f_log, yscrollcommand = self.sbar.set, selectmode = 'multiple', bg = '#000000',
                                       fg = fg_color)
        self.loglist_date = tk.Listbox(self.f_log, yscrollcommand = self.sbar.set, selectmode = 'multiple', bg = '#000000',
                                       fg = fg_color)
        
        self.loglist_numb.bind('<Button-4>', self.logMouseWheel)
        self.loglist_name.bind('<Button-4>', self.logMouseWheel)
        self.loglist_date.bind('<Button-4>', self.logMouseWheel)
        self.loglist_numb.bind('<Button-5>', self.logMouseWheel)
        self.loglist_name.bind('<Button-5>', self.logMouseWheel)
        self.loglist_date.bind('<Button-5>', self.logMouseWheel)
        self.loglist_numb.pack(side = 'left', fill = 'y')
        self.loglist_name.pack(side = 'left', fill = 'y')
        self.loglist_date.pack(side = 'left', fill = 'both')
        
        self.sbar.config(command = self.log_scroll)
        self.f_log.pack(side = 'left', fill = 'both')

    def logMouseWheel(self, event):
        direction = 0
        if event.num == 5:
            direction = 1
        if event.num == 4:
            direction = -1
        
        self.loglist_numb.yview('scroll', direction, 'units')
        self.loglist_name.yview('scroll', direction, 'units')
        self.loglist_date.yview('scroll', direction, 'units')

        return 'break'
    def log_scroll(self, *args):
        self.loglist_numb.yview(*args)
        self.loglist_name.yview(*args)
        self.loglist_date.yview(*args)

    def cur_make(self):
        self.curbar = tk.Scrollbar(self.f_cur)
        self.curbar.configure(bg = '#222222', activebackground = '#444444', troughcolor = '#ffffff')
        self.curbar.pack(side = 'right', fill = 'y')
        self.curlist = tk.Listbox(self.f_cur, yscrollcommand = self.curbar.set, selectmode = 'multiple', bg = '#000000',
                                 fg = '#ffcc12', width = self.curwidth)
        self.curlist.pack(side = 'left', fill = 'both')
        self.curbar.config(command = self.curlist.yview)
        self.f_cur.pack(side = 'left', fill = 'both')

    def but_make(self):
        bg_color = '#000000'
        fg_color = '#fafa21'
        afg_color = '#21ffff'
        font_name = 'Courier'
        font_size = 13
        self.actButton = tk.Button(self.f_but, text = 'Activation', command = self.active_func,
                                   bg = bg_color, fg = fg_color, bd = 0, activebackground = bg_color, activeforeground = afg_color,
                                   font = (font_name, font_size))
        self.actButton.pack(fill = 'both')
        self.delButton = tk.Button(self.f_but, text = 'To File', command = self.but_to_file_func,
                                    bg = bg_color, fg = fg_color, bd = 0, activebackground = bg_color, activeforeground = afg_color,
                                    font = (font_name, font_size))
        self.delButton.pack(side = 'left')
        self.delButto = tk.Button(self.f_but, text = 'Emergency', command = self.emergency,
                                    bg = bg_color, fg = fg_color, bd = 0, activebackground = bg_color, activeforeground = afg_color,
                                    font = (font_name, font_size))
        self.delButto.pack(side = 'left')
        self.runButton = tk.Button(self.f_but, text = 'Run', command = self.runProc,
                                   bg = bg_color, fg = fg_color, bd = 0, activebackground = bg_color, activeforeground = afg_color,
                                   font = (font_name, font_size))
        self.runButton.pack(fill = 'both')
        self.f_but.pack(side = 'bottom', fill = 'both')
    def but_to_file_func(self):
        if len(self.log) == 0:
            tkm.showwarning('', 'No data.')
            return
        date = dt.now()
        file_name = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(date.second)
        f = open('./log/' + file_name + '.txt', 'w')
        for w in self.log:
            f.write(w)
        f.close()

        tkm.showinfo('', 'Complete')

    def active_func(self):
        if not self.activated.value:
            self.run_init_2()
            print self.activated.value
            if self.activated.value:
                active_color = '#a04455'
                self.actButton.configure(text = 'Activated', fg = active_color, activeforeground = active_color)
        else:
            tkm.showwarning('', 'Already activated')
            return
        
    def emergency(self):
        self.client.send(self.cmdOpen)
        self.client.send(self.cmdClose)
        resp = self.client.recv(4096)
        tkm.showinfo('', 'From Server: ' + resp)


    def gui_update(self):
        a = 2
        while not self.cam_closed.value:
            hh = dt.now().hour
            mm = dt.now().minute
            ss = dt.now().second
            '''
            for i in range(a):
                if a % 1000 == 0 and i != 0:
                    print 'Calculating'
                if i == 0:
                    continue
                elif i == a - 1:
                    print str(a) + " date:" + str(hh) + ':' + str(mm)
                    break
                else:
                    if a % (i + 1) == 0:
                        break
            a = a + 1'''
            if self.can_insert.value:
                try:
                    if int(self.to_ins_numb.value) not in self.logdict and self.fromEnter.value:
                        self.logdict[int(self.to_ins_numb.value)] = self.to_ins_name.value
                        self.loglist_numb.insert('end', self.to_ins_numb.value)
                        self.loglist_name.insert('end', self.to_ins_name.value)
                        self.loglist_date.insert('end', self.to_ins_date.value)
                        self.log.append(self.to_ins_numb.value + '-' + self.to_ins_name.value + '-' + self.to_ins_date.value)
                        loadLogFile = open('loadLogFile.txt', 'a')
                        loadLogFile.write(self.to_ins_numb.value +'-' + self.to_ins_name.value + '-' + self.to_ins_date.value + '\n')
                        loadLogFile.close()
                        
                    if int(self.to_ins_numb.value) in self.logdict and self.fromExit.value:
                        del self.logdict[int(self.to_ins_numb.value)]
                        self.loglist_numb.insert('end', self.to_ins_numb.value)
                        self.loglist_name.insert('end', self.to_ins_name.value)
                        self.loglist_date.insert('end', self.to_ins_date.value)
                        self.log.append(self.to_ins_numb.value + '-' + self.to_ins_name.value + '-' + self.to_ins_date.value)
                        loadLogFile = open('loadLogFile.txt', 'a')
                        loadLogFile.write(self.to_ins_numb.value +'-' + self.to_ins_name.value + '-' + self.to_ins_date.value + '\n')
                        loadLogFile.close()
                        
                    self.loglist_numb.yview('scroll', 1, 'units')
                    self.loglist_name.yview('scroll', 1, 'units')
                    self.loglist_date.yview('scroll', 1, 'units')
                except:
                    pass

                try:
                    if self.fromEnter.value:
                        self.curdict[int(self.to_ins_numb.value)] = (self.to_ins_name.value, self.to_ins_date.value)
                    if int(self.to_ins_numb.value) in self.curdict and self.fromExit.value:
                        del self.curdict[int(self.to_ins_numb.value)]
                except:
                    pass

                if len(self.curdict) == 0:
                    os.system('rm loadCurLogFile.txt')
                    self.client.send(self.cmdIL0)
                else:
                    self.client.send(self.cmdIL)

                time.sleep(0.1)
                if self.fromEnter.value or self.fromExit.value:                    
                    self.client.send(self.cmdOpen)
                    time.sleep(0.1)
                    self.client.send(self.cmdClose)

                
                self.curlist.delete(0, 'end')
                loadCurLogFile = open('loadCurLogFile.txt', 'w')
                for key in self.curdict:
                    self.curlist.insert('end', '%8s %s' %(self.curdict[key][0], self.curdict[key][1]))
                    loadCurLogFile.write(str(key) + '-' + self.curdict[key][0] + '-' + self.curdict[key][1] + '\n')
                loadCurLogFile.close()
                os.system('cp loadCurLogFile.txt ../temporary.txt')
                
                self.can_insert.value = False
                self.fromEnter.value = False
                self.fromExit.value = False
            self.root.update()
        self.runningProc.value = False
        print 'Im out'
        
    def enter_cam(self):
        proc = zbar.Processor()
        proc.parse_config('enable')
        device = self.mainDev.value

        proc.init(device)
        proc.set_data_handler(self.enter_handle)
        proc.visible = True
        proc.active = True

        try:
            proc.user_wait()
            self.cam_closed.value = True
        except zbar.WindowClosed:
            pass

    def enter_handle(self, proc, image, closure):

        for symbol in image.symbols:
            read_data = symbol.data

            sdata = read_data
            data_numRand = sdata[:23]
            data_numName = sdata[23:31]
            data_name = sdata[31:]
            date = dt.now()
            date_str = '%d/%02d/%02d %02d:%02d:%02d IN' %(date.year, date.month, date.day, date.hour, date.minute, date.second)
            self.can_insert.value = True
            self.to_ins_numb.value = data_numName
            self.to_ins_name.value = data_name
            self.to_ins_date.value = date_str
            self.fromEnter.value = True
            self.fromExit.value = False
            ringInProc = mp.Process(target = self.ringIn)
            ringInProc.start()
            print 'Enter'
            
    def exit_cam(self):
        proc = zbar.Processor()
        proc.parse_config('enable')
        device = self.subDev.value

        proc.init(device)
        proc.set_data_handler(self.exit_handle)
        proc.visible = True
        proc.active = True
        try:
            proc.user_wait()
            self.cam_closed.value = True
        except zbar.WindowClosed:
            pass

    def exit_handle(self, proc, image, closure):

        for symbol in image.symbols:
            read_data = symbol.data

            sdata = read_data
            data_numRand = sdata[:23]
            data_numName = sdata[23:31]
            data_name = sdata[31:]
            date = dt.now()
            date_str = '%d/%02d/%02d %02d:%02d:%02d OUT' %(date.year, date.month, date.day, date.hour, date.minute, date.second)
            self.can_insert.value = True
            self.to_ins_numb.value = data_numName
            self.to_ins_name.value = data_name
            self.to_ins_date.value = date_str
            self.fromEnter.value = False
            self.fromExit.value = True
            ringOutProc = mp.Process(target = self.ringOut)
            ringOutProc.start()
            print 'Exit'
        
    def runProc(self, *args):
        
        if not self.activated.value:
            tkm.showwarning('', 'Not Activated')
            return
        if self.runningProc.value:
            tkm.showwarning('', 'Already running')
            return
        self.runningProc.value = True
        curDir = os.listdir('./')
        self.cam_closed = mp.Value('d', False)
        self.can_insert = mp.Value('d', True)
        self.fromEnter = mp.Value('d', False)
        self.fromExit = mp.Value('d', False)

        self.curdict = dict()
        self.logdict = dict()
        self.log = []

        if 'loadLogFile.txt' in curDir:
            loadLogFile = open('loadLogFile.txt', 'r')
            loadLogList = loadLogFile.readlines()
            self.loglist_numb.delete(0, 'end')
            self.loglist_name.delete(0, 'end')
            self.loglist_date.delete(0, 'end')
            for i, LLL in enumerate(loadLogList):
                LLL = LLL.rsplit('\n')[0]
                numb = LLL.split('-')[0]
                name = LLL.split('-')[1]
                date = LLL.split('-')[2]
                if i == len(loadLogList) - 1:
                    if 'IN' in date:
                        self.logdict[int(numb)] = name
                    elif 'OUT' in date:
                        if int(numb) in self.logdict:
                            del self.logdict[int(numb)]
                    else:
                        print 'You need Debug. In function runProc()'
                        return
                self.loglist_numb.insert('end', numb)
                self.loglist_name.insert('end', name)
                self.loglist_date.insert('end', date)
                self.loglist_numb.yview('scroll', 1, 'units')
                self.loglist_name.yview('scroll', 1, 'units')
                self.loglist_date.yview('scroll', 1, 'units')
                self.log.append(numb + '-' + name +'-' + '-' + date)
        if 'loadCurLogFile.txt' in curDir:
            loadCurLogFile = open('loadCurLogFile.txt', 'r')
            loadCurLogList = loadCurLogFile.readlines()
            self.curlist.delete(0, 'end')
            for LCLL in loadCurLogList:
                LCLL = LCLL.rsplit('\n')[0]
                numb = LCLL.split('-')[0]
                name = LCLL.split('-')[1]
                date = LCLL.split('-')[2]
                self.curdict[int(numb)] = (name, date)
                self.curlist.insert('end', '%8s %s' % (name, date))
        
        to_ins_numb_buf = ctypes.create_string_buffer('Number', 30)
        to_ins_name_buf = ctypes.create_string_buffer('Name', 30)
        to_ins_date_buf = ctypes.create_string_buffer('Date', 30)
        
        self.to_ins_numb = mp.Array(ctypes.c_char, to_ins_numb_buf)
        self.to_ins_name = mp.Array(ctypes.c_char, to_ins_name_buf)
        self.to_ins_date = mp.Array(ctypes.c_char, to_ins_date_buf)
        
        camProc1 = mp.Process(target = self.enter_cam)
        camProc2 = mp.Process(target = self.exit_cam)
        camProc1.start()
        camProc2.start()
        self.gui_update()

    def ringIn(self):
        os.system('sudo python ringIn.py')
    def ringOut(self):
        os.system('sudo python ringOut.py')

    def run_init_2(self):
        main_dev_buf = ctypes.create_string_buffer('', 20)
        sub_dev_buf = ctypes.create_string_buffer('', 20)
        
        self.mainDev = mp.Array(ctypes.c_char, main_dev_buf)
        self.subDev = mp.Array(ctypes.c_char, sub_dev_buf)
        self.showActivation = mp.Value('d', False)
        self.showNonActivationCam1 = mp.Value('d', False)
        self.showNonActivationCam2 = mp.Value('d', False)

        cam1Proc = mp.Process(target = self.cam1)
        cam2Proc = mp.Process(target = self.cam2)
        cam1Proc.start()
        cam2Proc.start()
        self.showMessage()
        
        cam1Proc.join()
        cam2Proc.join()

    def showMessage(self):
        while not self.activated.value:
            if self.showActivation.value:
                tkm.showinfo('', 'Activated')
                return
            elif self.showNonActivationCam1.value and self.showNonActivationCam2.value and not self.showActivation.value:
                tkm.showwarning('', 'Not Activated, again')
                return
    def cam1(self):
        cam1 = zbar.Processor()
        cam1.parse_config('enable')
        self.device1 = '/dev/video0'
        self.device2 = '/dev/video1'
        cam1.init(self.device1)
        cam1.set_data_handler(self.handler1)
        cam1.visible = True
        cam1.active = True

        try:
            time.sleep(0.3)
            cam1.user_wait()
            self.showNonActivationCam1.value = True
        except zbar.WindowClosed:
            pass
    def handler1(self, cam1, image, closure):
        for symbol in image.symbols:
            if not self.activated.value:
                self.mainDev.value = self.device1
                self.subDev.value = self.device2
                self.showActivation.value = True
                time.sleep(0.1)
                self.activated.value = True
                
    def cam2(self):
        cam2 = zbar.Processor()
        cam2.parse_config('enable')
        self.device1 = '/dev/video0'
        self.device2 = '/dev/video1'
        cam2.init(self.device2)
        cam2.set_data_handler(self.handler2)
        cam2.visible = True
        cam2.active = True

        try:
            time.sleep(0.3)
            cam2.user_wait()
            self.showNonActivationCam2.value = True
        except zbar.WindowClosed:
            pass
    def handler2(self, cam2, image, closure):
        for symbol in image.symbols:
            if not self.activated:
                self.mainDev.value = self.device2
                self.subDev.value = self.device1
                self.showActivation.value = True
                time.sleep(0.1)
                self.activated.value = True
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'You need one argument. MAIN or ERIT'
        print 'python z.py MAIN, for example.'
        sys.exit('Argument Error in main function')
    os.system('v4l2-ctl -d /dev/video0 --set-fmt-video=width=220,height=220')
    os.system('v4l2-ctl -d /dev/video1 --set-fmt-video=width=220,height=220')
    app = App()
