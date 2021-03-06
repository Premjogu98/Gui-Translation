from selenium import webdriver
import time
import pymysql.cursors
import re
import wx
import sys, os
import html
import string
import Global_var

app = wx.App()

browser = webdriver.Chrome(executable_path=str(f"C:\\Translation EXE\\chromedriver.exe"))
browser.maximize_window()
browser.get(
    """https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
wx.MessageBox(' -_-  Add Extension and Then Click On OK BUTTON -_- ', 'GUI Google Translation', wx.OK | wx.ICON_ERROR)
time.sleep(5)
browser.get('https://translate.google.com/')

def connection():
    connection = ''
    a3 = 0
    while a3 == 0:
        try:
            connection = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            time.sleep(10)
            a3 = 0
            connection.close()


def casesensitive(ReplyStrings):
    ReplyStrings1 = string.capwords(str(ReplyStrings))
    title = ReplyStrings1.replace(" A ", " a ").replace(" An ", " an ").replace(" The ", " the ").replace(" And ",
                                                                                                          " and "). \
        replace(" If ", " if ").replace(" Else ", " else ").replace(" When ", " when ").replace(" Up ", " up ") \
        .replace(" At ", " at ").replace(" From ", " from ").replace(" By ", " by ").replace(" On ", " on ") \
        .replace(" Off ", " off ").replace(" At ", " at ").replace(" Of ", " of ").replace(" For ", " for "). \
        replace(" In ", " in ").replace(" Out ", " out ").replace(" Over ", " over ").replace(" To ", " to ") \
        .replace(" Is ", " is ").replace(" Or ", " or ").replace(" With ", " with ").replace(" Which ", " which ") \
        .replace(" Will ", " will ").replace(" Be ", " be ").replace(" There ", " there ").replace(" Where ", " where ") \
        .replace(" Have ", " have ").replace(" Do ", " do ").replace(" Nor ", " nor ").replace(" Some ", " some ") \
        .replace(" Since ", " since ").replace(" Till ", " till ").replace(" Until ", " until ").replace(" Onto ",
                                                                                                         " onto ") \
        .replace(" Used ", " used ").replace(" Of ", " of ").replace(" That ", " that ").strip()
    return title


def check_translated_textarea():
    tr_clear = False
    while tr_clear == False:
        tr_val = ''
        for tr_box in browser.find_elements_by_xpath('//*[@class="tlid-translation translation"]'):
            tr_val = 'Exist'
            print(tr_val)
            time.sleep(1)
        if tr_val == '':
            tr_clear = True
        else:
            tr_clear = False


def click_on_tryagain():
    print(' -_-  Please wait browser will be refresh automatically after 30 SEC  -_- ')
    time.sleep(30)
    try_btn_found = False
    try:
        for try_again_btn in browser.find_elements_by_xpath('//*[@class="tlid-result-container-error-button translation-error-button"]'):
            try_again_btn.click()
            try_btn_found = True
            break
    except:
        pass
    if try_btn_found == False:
        browser.refresh()
        time.sleep(5)
        for i in browser.find_elements_by_xpath('//*[@id="source"]'):
            i.clear()
            break
    time.sleep(2)


def language_detect():
    If_other_Than_English = True
    for language_detect in browser.find_elements_by_xpath('//*[@class="goog-inline-block jfk-button jfk-button-standard jfk-button-collapse-right jfk-button-checked"]'):
        language_detect = language_detect.get_attribute('innerText').lower()
        if 'english' not in language_detect:
            If_other_Than_English = True
        else:
            If_other_Than_English = False
        break
    return If_other_Than_English


def tarnslation():
    try:

        trasns = connection()
        cur = trasns.cursor()
        # cur.execute(f"SELECT * FROM `tenders_db`.`l2l_tenders_tbl` WHERE Posting_Id='523417'")  # For test
        cur.execute(f"SELECT * FROM l2l_tenders_tbl WHERE is_english = '1' AND `source` IN ({str(Global_var.Source_Name)}) ORDER BY Posting_Id ASC")  # 0 = English, 1 = Non-English
        rows = cur.fetchall()

        if len(rows) == 0:
            wx.MessageBox(' -_-  No Tender Available For Translation -_- ', 'GUI Google Translation ',
                          wx.OK | wx.ICON_INFORMATION)
            time.sleep(2)
            browser.close()
            sys.exit()

        print(f' Total Tenders Found For Translation : {len(rows)}')
        count = 0
        Tender_count_for_Refresh = 0
        # global Exception_loop
        # Exception_loop = True
        # while Exception_loop == True:
        for row in rows:
            try:
                id = "%s" % (row["Posting_Id"])
                source = "%s" % (html.unescape(row["source"]))
                notice_no = "%s" % (html.unescape(row["notice_no"]))
                purchaser = "%s" % (html.unescape(row["purchaser_name"]))
                address = "%s" % (html.unescape(row["purchaser_address"]))
                title = "%s" % (html.unescape(row["description"]))
                description = "%s" % (html.unescape(row["tender_details"]))

                en_notice_no = ''
                en_purchaser = ''
                en_address = ''
                en_title = ''
                en_description = ''

                en_notice_no_done = False
                en_purchaser_done = False
                en_address_done = False
                en_title_done = False
                en_description_done = False

                print(f'Selected Source : {Global_var.Source_Name}')
                print(f'Posting_Id : {id}')
                print(f'Source : {source}')

                if not re.match("^[\W A-Za-z0-9_@?./#&+-]*$", notice_no):
                    is_available = 1
                    for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                        i.clear()
                        notice_no = re.sub('\s+', ' ', notice_no)
                        notice_no = notice_no.replace('<br>','<br>\n').replace('<BR>','<br>\n').replace('<Br>','<br>\n')
                        check_translated_textarea()
                        i.send_keys(str(notice_no))
                        is_available = 0
                        break
                    if is_available == 1:
                        wx.MessageBox(
                            'Something Went Wrong Please Refresh Google Translation Page Then Click On -_- OK -_- ',
                            'GUI Google Translation ', wx.OK | wx.ICON_WARNING)
                    else:
                        time.sleep(5)
                        for en_notice_no in browser.find_elements_by_xpath(
                                '//*[@class="tlid-translation translation"]'):
                            en_notice_no = en_notice_no.get_attribute('innerText')
                            en_notice_no_done = True
                            break
                        if en_notice_no_done == False:
                            click_on_tryagain()
                else:
                    en_notice_no = notice_no
                    en_notice_no_done = True
                print(f'Notice_No : {en_notice_no}')

                is_available = 1
                if purchaser != '':
                    for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                        i.clear()
                        purchaser = re.sub('\s+', ' ', purchaser)
                        purchaser = purchaser.replace('<br>','<br>\n').replace('<BR>','<br>\n').replace('<Br>','<br>\n')
                        check_translated_textarea()
                        i.send_keys(str(purchaser))
                        time.sleep(5)
                        If_other_Than_English = language_detect()
                        is_available = 0
                        break
                    if is_available == 1:
                        wx.MessageBox(
                            'Something Went Wrong Please Refresh Google Translation Page Then Click On -_- OK -_- ',
                            'GUI Google Translation ', wx.OK | wx.ICON_WARNING)
                    else:
                        time.sleep(1)
                        if If_other_Than_English == True:
                            for en_purchaser in browser.find_elements_by_xpath(
                                    '//*[@class="tlid-translation translation"]'):
                                en_purchaser = en_purchaser.get_attribute('innerText').upper()
                                en_purchaser_done = True
                                break
                            if en_purchaser_done == False:
                                click_on_tryagain()
                        else:
                            en_purchaser = purchaser
                            en_purchaser_done = True
                else:
                    en_purchaser = purchaser
                    en_purchaser_done = True

                en_purchaser = en_purchaser.upper()
                print(f'Purchaser : {en_purchaser}')

                is_available = 1
                if address !='':
                    for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                        i.clear()
                        address = re.sub('\s+', ' ', address)
                        address = address.replace('<br>','<br>\n').replace('<BR>','<br>\n').replace('<Br>','<br>\n')
                        check_translated_textarea()
                        i.send_keys(str(address))
                        time.sleep(4)
                        If_other_Than_English = language_detect()
                        is_available = 0
                        break
                    if is_available == 1:
                        wx.MessageBox(
                            'Something Went Wrong Please Refresh Google Translation Page Then Click On -_- OK -_- ',
                            'GUI Google Translation ', wx.OK | wx.ICON_WARNING)
                    else:
                        time.sleep(1)
                        if If_other_Than_English == True:
                            for en_address in browser.find_elements_by_xpath('//*[@class="tlid-translation translation"]'):
                                en_address = en_address.get_attribute('innerText')
                                en_address_done = True
                                break
                            if en_address_done == False:
                                click_on_tryagain()
                        else:
                            en_address = address
                            en_address_done = True
                else:
                    en_address = address
                    en_address_done = True
                print(f'Address : {en_address}')

                is_available = 1
                if title != "":
                    for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                        i.clear()
                        title = re.sub('\s+', ' ', title)
                        title = title.replace('<br>','<br>\n').replace('<BR>','<br>\n').replace('<Br>','<br>\n')
                        check_translated_textarea()
                        i.send_keys(str(title))
                        time.sleep(5)
                        If_other_Than_English = language_detect()
                        is_available = 0
                        break
                    if is_available == 1:
                        wx.MessageBox(
                            'Something Went Wrong Please Refresh Google Translation Page Then Click On -_- OK -_- ',
                            'GUI Google Translation ', wx.OK | wx.ICON_WARNING)
                    else:
                        time.sleep(1)
                        if If_other_Than_English == True:
                            for en_title in browser.find_elements_by_xpath('//*[@class="tlid-translation translation"]'):
                                en_title = en_title.get_attribute('innerText')
                                en_title_done = True
                                break
                            if en_title_done == False:
                                click_on_tryagain()
                        else:
                            en_title = title
                            en_title_done = True
                else:
                    en_title = title
                    en_title_done = True
                en_title = casesensitive(en_title)
                print(f'Title : {en_title}')

                is_available = 1
                if description != "":
                    for i in browser.find_elements_by_xpath('//*[@id="source"]'):
                        i.clear()
                        description = re.sub('\s+', ' ', description)
                        description = description.replace('<br>','<br>\n').replace('<BR>','<br>\n').replace('<Br>','<br>\n')
                        check_translated_textarea()
                        if len(description) >= 1200:
                            description = description[:1200] + '...'
                        i.send_keys(str(description))
                        time.sleep(5)
                        If_other_Than_English = language_detect()
                        is_available = 0
                        break
                    if is_available == 1:
                        wx.MessageBox(
                            'Something Went Wrong Please Refresh Google Translation Page Then Click On -_- OK -_- ',
                            'GUI Google Translation ', wx.OK | wx.ICON_WARNING)
                    else:
                        time.sleep(1)
                        if If_other_Than_English == True:
                            for en_description in browser.find_elements_by_xpath(
                                    '//*[@class="tlid-translation translation"]'):
                                en_description = en_description.get_attribute('innerText')
                                en_description_done = True
                                break
                            if en_description_done == False:
                                click_on_tryagain()
                        else:
                            en_description = description
                            en_description_done = True
                else:
                    en_description = description
                    en_description_done = True

                print(f'Details : {en_description}')

                en_notice_no = en_notice_no.replace("'", "''").replace("< ", "<").replace(" >", ">").replace("</ ", "</").replace("\\", "\\\\")
                en_purchaser = en_purchaser.replace("'", "''").replace("< ", "<").replace(" >", ">").replace("</ ", "</").replace("\\", "\\\\")
                en_address = en_address.replace("'", "''").replace("< ", "<").replace(" >", ">").replace("</ ", "</").replace("\\", "\\\\")
                en_title = en_title.replace("'", "''").replace("< ", "<").replace(" >", ">").replace("</ ", "</").replace("\\", "\\\\")
                en_description = en_description.replace("'", "''").replace("< ", "<").replace(" >", ">").replace("</ ", "</").replace("\\", "\\\\")

                if len(en_title) > 250:
                    en_title = en_title[:246]
                    suffix = "'" 
                    suffix2 = "''"
                    if suffix2 and en_title.endswith(suffix2):
                        pass
                    elif suffix and en_title.endswith(suffix):
                        en_title = en_title[:-len(suffix)]
                    en_title = en_title + '...'

                if len(en_address) > 500:
                    en_address = en_address[:500]
                    suffix = "'"
                    suffix2 = "''"
                    if suffix2 and en_address.endswith(suffix2):
                        pass
                    elif suffix and en_address.endswith(suffix):
                        en_address = en_address[:-len(suffix)]
                    en_address = en_address + '...'

                if en_notice_no_done == True and en_purchaser_done == True and en_address_done == True and en_title_done == True and en_description_done == True:
                    a = False
                    while a == False:
                        try:
                            trasns = connection()
                            cur = trasns.cursor()
                            Update_Website_Status = f"UPDATE l2l_tenders_tbl SET is_english = '0', notice_no='{en_notice_no}',purchaser_name='{en_purchaser}',purchaser_address='{en_address}',description='{en_title}',tender_details='{en_description}' WHERE Posting_Id = '{id}'"
                            print(Update_Website_Status)
                            cur.execute(Update_Website_Status)
                            trasns.commit()
                            a = True
                        except Exception as e:
                            print(f'ERROR ON UPDATE QUERY EXCEPTION: {e}')
                            trasns.close()
                            a = False
                            time.sleep(5)
                count += 1
                print(f'Translation Completed : {count}  / {len(rows)}\n')
                # Exception_loop = False
                Tender_count_for_Refresh += 1
                if Tender_count_for_Refresh == 100:
                    Tender_count_for_Refresh = 0
                    clear = lambda: os.system('cls')  # Clear command Prompt
                    clear()
                    browser.delete_all_cookies()
                    browser.execute_script("location.reload(true);")
                    time.sleep(4)
                    print(f'Translation Completed : {count}  / {len(rows)}\n')
                    
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                    "\n",
                    exc_tb.tb_lineno)
                time.sleep(3)
                browser.refresh()
                time.sleep(2)
                # Exception_loop = True

        # wx.MessageBox('All Process Done','GUI Google Translation ', wx.OK | wx.ICON_INFORMATION)
        # time.sleep(2)
        # browser.close()
        # sys.exit()
        # time.sleep(2)
        tarnslation()
            

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
              exc_tb.tb_lineno)
        time.sleep(2)
        wx.MessageBox(' -_- (ERROR ON MAIN EXCEPTION) -_- ',
                      'GUI Google Translation ',
                      wx.OK | wx.ICON_ERROR)
        time.sleep(2)
        browser.close()
        sys.exit()


tarnslation()