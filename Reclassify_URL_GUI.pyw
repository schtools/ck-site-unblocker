'''
Icon used:
https://iconarchive.com/show/polygon-icons-by-graphicloads/lock-unlock-icon.html
'''
# Big try/catch statement for all error handling
try:
    # Only import needed functions otherwise file size becomes bloated!
    from requests import get, post
    import sys  # To use _MEIPASS, I need to import all of sys
    import threading as th
    from tkinter import *
    from tkinter import scrolledtext as st
    from tkinter import messagebox
    from traceback import format_exc
    from datetime import datetime
    from os import path, getcwd
    from json import load, dump

    # For autopytoexe
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = path.abspath(".")

        return path.join(base_path, relative_path)
    
    # Tkinter window initialization
    window = Tk()
    window.withdraw()
    window.title("Contentkeeper Site Unblocker")
    window.geometry("500x300")
    window.resizable(False, False)
    window.iconbitmap(resource_path("Graphicloads-Polygon-Lock-unlock.ico"))
    
    # Settings variables
    data = {
        "requests to send" : {
            "open": False,
            "choose": True,
            "confirm": True
        },
        "url" : "https://192.168.55.243/cgi-bin/ck/re_u.cgi",
        "reclass" : "29",
        "cat" : "-1",
        "dat" : "n/a",
        "user" : "you/organization"
    }

    # Loading/creating the save file
    if path.exists("config.ini"):
        with open("config.ini", "r") as config:
            data = load(config)
            config.close()
    else:
        with open("config.ini", "w+") as config:
            dump(data, config)
            config.close()
    
    settings = None
    settings_open = False

    # My access management (done if I want to maybe push a new version or have to revoke the ability for people to use it temporarily)
    # Feel free to remove this if you are forking
    if not "--bypasscheck" in sys.argv or not "-c" in sys.argv:
        check = get("https://raw.githubusercontent.com/schtools/schtools.github.io/main/run_ublk.txt").text
        if not "true" in check.strip():
            messagebox.showinfo("Program disabled or Github unreachable", "For one reason or another, I have temporarily disabled access to this program or it cannot reach Github's server.")
            print("I have disabled this program or the github servers are down.")
            window.destroy()
            sys.exit(1)

    # Getting the possible classifications, feel free to change the txt file to what is on your appliance
    reclassifications = open(resource_path("all_classifications.txt")).readlines()
    reclassifications = [i.strip() for i in reclassifications]
    reclassifications_dict = {}
    for item in reclassifications:
        reclassifications_dict[item.split(": ")[0]] = item

    # Handling closing the window so settings is closed too
    def close_window():
        global window, settings, settings_open
        try:
            if settings_open:
                settings.destroy()
        except:
            pass
        window.destroy()

    # The reclassification function, this allows a user to reclassify a url of their choosing
    def reclassify(user_url):
        global data#url, reclass, output_txt, is_global_state, cat, dat, requests_to_send, user
        url = data['url']
        reclass = data['reclass']
        cat = data['cat']
        dat = data['dat']
        requests_to_send = data['requests to send']
        user = data['user']

        # This function checks the text of the request's response and returns True if it indicates that the Appliance accpets it
        def check_response(req_type, text):
            # These checks are very basic, yet they seem to work (at least for me)
            if req_type == "open":
                if "Submit Above Sites" in text:
                    return True
            elif req_type == "choose":
                if "to send your reclassification to ContentKeeper" in text:
                    return True
            elif req_type == "confirm":
                if "The above reclassifications are now being submitted" in text:
                    return True
            return False
        
        try:
            # Initial output text
            output_txt.insert(INSERT, "---------------------------NEW---------------------------\n")
            output_txt.insert(INSERT, f"Starting requests on {user_url}...\n")
            output_txt.insert(INSERT, f"Selected database is {dat}\n")

            # The "open" request
            if requests_to_send["open"]:
                open_req = post(url, data={
                    "NM" : f"{user},{user_url},n,0"
                }, verify = False)
                output_txt.insert(INSERT, f"Open request response code: {open_req.status_code} {'good' if open_req.status_code == 200 else 'bad :('}\n")
                is_good = check_response("open", open_req.text)
                if is_good:
                    output_txt.insert(INSERT, f"CK Appliance accepted the open request\n\n")
                else:
                    output_txt.insert(INSERT, f"CK Appliance rejected the open request\n\n")

            # The "choose" request
            if requests_to_send["choose"]:            
                choose_req = post(url, data={
                    "URL_AREA" : user_url,
                    "USER" : "",
                    "SEL_1" : reclass,
                    "URL_1" : user_url,
                    "CAT_1" : cat,
                    "DAT_1" : dat,
                    "autocat" : reclass,
                    "SUBMIT_SITE_THIRD" : "Submit Above Sites",
                    "NUM_SUBMIT_URL" : 1
                }, verify = False)
                output_txt.insert(INSERT, f"Choose request response code: {choose_req.status_code} {'good' if choose_req.status_code == 200 else 'bad :('}\n")
                is_good = check_response("choose", choose_req.text)
                if is_good:
                    output_txt.insert(INSERT, f"CK Appliance accepted the choose request\n\n")
                else:
                    output_txt.insert(INSERT, f"CK Appliance rejected the choose request\n\n")

            # The "confirm" request
            if requests_to_send["confirm"]:
                confirm_req = post(url, data={
                    "USER" : "",
                    "URL_AREA" : user_url,
                    "NUM_SUBMIT_URL" : 1,
                    "SEL_1" : reclass,
                    "CAT_1" : cat,
                    "URL_1" : user_url,
                    "DAT_1" : dat,
                    "SUBMIT_SITE_SEND" : "Send"
                }, verify = False)
                output_txt.insert(INSERT, f"Confirm request response code: {confirm_req.status_code} {'good' if confirm_req.status_code == 200 else 'bad :('}\n")
                is_good = check_response("confirm", confirm_req.text)
                if is_good:
                    output_txt.insert(INSERT, f"CK Appliance accepted the confirm request\n\n")
                else:
                    output_txt.insert(INSERT, f"CK Appliance rejected the confirm request\n\n")

            # Final output text
            output_txt.insert(INSERT, "Program done! \nCheck your submitted site to see if it worked!\n")
            output_txt.insert(INSERT, "---------------------------END---------------------------\n")
            return True
        except Exception as e:
            # If there was a request error, we print the error to the output and stop any more requests
            output_txt.insert(INSERT, f"Error occured! Details below:\n{e}\n")
            output_txt.insert(INSERT, "---------------------------END---------------------------\n")
            return False

    # The settings window
    def open_settings():
        global data, settings, reclassifications, reclassifications_dict, settings_open#url, cat, reclass, settings, reclassifications, reclassifications_dict, requests_to_send, user, settings_open, dat
        url = data['url']
        reclass = data['reclass']
        cat = data['cat']
        dat = data['dat']
        requests_to_send = data['requests to send']
        user = data['user']

        # If there is already a settings window open, prevent another one from opening
        if settings_open:
            return

        settings_open = True
        
        # Settings window setup
        settings = Tk()
        settings.title("Settings")
        settings.geometry("350x400")
        settings.resizable(False, False)
        settings.iconbitmap(resource_path("Graphicloads-Polygon-Lock-unlock.ico"))
        
        # The text labels
        Label(settings, text="Settings", font=("Arial Bold", 15)).place(x=130, y=1)
        Label(settings, text="Only edit these settings if you know what you are doing.", font=("Arial Bold", 9)).place(x=10, y=28)
        Label(settings, text="Appliance URL:", font=("Arial Bold", 9)).place(x=10, y=50)
        Label(settings, text="Initial Classification (cat):", font=("Arial Bold", 9)).place(x=10, y=100)
        Label(settings, text="Chosen Classification (cat):", font=("Arial Bold", 9)).place(x=10, y=150)
        Label(settings, text="Requests:", font=("Arial Bold", 9)).place(x=10, y=200)
        Label(settings, text="User (only needed when \"open\" is ticked):", font=("Arial Bold", 9)).place(x=10, y=250)
        Label(settings, text="Database to edit:", font=("Arial Bold", 9)).place(x=10, y=300)
        
        # The inputs
        # Appliance URL entry
        appliance_url_input = Entry(settings, width=50)
        appliance_url_input.place(x=12, y=75)
        appliance_url_input.delete(0, "end")
        appliance_url_input.insert(0, url)

        # Previous classification (cat) option menu
        cat_index = StringVar(settings)
        cat_index.set(reclassifications_dict[cat])
        cat_options = OptionMenu(settings, cat_index, *reclassifications)
        cat_options.place(x=10, y=118)

        # User-chosen classification option menu
        reclass_index = StringVar(settings)
        reclass_index = StringVar(settings)
        reclass_index.set(reclassifications_dict[reclass])
        reclass_options = OptionMenu(settings, reclass_index, *reclassifications)
        reclass_options.place(x=10, y=168)

        # Checkbutton initialization
        open_value = IntVar(settings)
        choose_value = IntVar(settings)
        confirm_value = IntVar(settings)
        # The "open" request checkbox
        open_checkbox = Checkbutton(settings, text="Open", variable=open_value, onvalue=1, offvalue=0)
        open_value.set(int(requests_to_send["open"]))
        open_checkbox.place(x=8, y=225)
        # The "choose" request checkbox
        choose_checkbox = Checkbutton(settings, text="Choose", variable=choose_value, onvalue=1, offvalue=0)
        choose_value.set(int(requests_to_send["choose"]))
        choose_checkbox.place(x=65, y=225)
        # The "confirm" request checkbox
        confirm_checkbox = Checkbutton(settings, text="Confirm", variable=confirm_value, onvalue=1, offvalue=0)
        confirm_value.set(int(requests_to_send["confirm"]))
        confirm_checkbox.place(x=135, y=225)

        # User's username/domain for the "open" request
        user_input = Entry(settings, width=25)
        user_input.place(x=12, y=275)
        user_input.delete(0, "end")
        user_input.insert(0, user)

        # Database option menu
        is_global_state = StringVar(settings)
        is_global_state.set(dat)
        is_global_list = OptionMenu(settings, is_global_state, "n/a", "Local", "Global")
        is_global_list.place(x=10, y=320)

        # Save and cancel functions
        def close_settings():
            global settings, settings_open
            settings_open = False
            settings.destroy()
        
        def save_settings():#appliance_url_input, cat_index, reclass_index, open_checkbox, choose_checkbox, confirm_checkbox, is_global_list):  # This is VERY yucky but global variables won't work for some reason
            global data#url, cat, reclass, requests_to_send, user, dat
            nonlocal url, cat, reclass, requests_to_send, user, dat, appliance_url_input, cat_index, reclass_index, open_checkbox, choose_checkbox, confirm_checkbox, is_global_list
            
            requests_to_send["open"] = bool(open_value.get())
            requests_to_send["choose"] = bool(choose_value.get())
            requests_to_send["confirm"] = bool(confirm_value.get())
            url = appliance_url_input.get()
            cat = cat_index.get().split(": ")[0]
            reclass = reclass_index.get().split(": ")[0]
            user = user_input.get()
            dat = is_global_state.get()

            data = {
                "requests to send" : requests_to_send,
                "url" : url,
                "reclass" : reclass,
                "cat" : cat,
                "dat" : dat,
                "user" : user
            }

            with open("config.ini", "w") as config:
                config.truncate(0)
                dump(data, config) 
                config.close()
            
            close_settings()
        
        # Save and cancel inputs
        cancel_button = Button(settings, text="Cancel", command=close_settings)
        cancel_button.place(x=100, y=360)
        
        save_button = Button(settings, text="Save Settings", command=save_settings)#lambda: save_settings(appliance_url_input, cat_index, reclass_index, open_checkbox, choose_checkbox, confirm_checkbox, is_global_list))  # This is VERY yucky but global variables won't work for some reason
        save_button.place(x=12, y=360)
        
        # Showing the window
        settings.protocol("WM_DELETE_WINDOW", close_settings)
        settings.mainloop()

    # Placing the widgets on the Tkinter window
    window.deiconify()
    Label(window, text="Website Unblocker", font=("Arial Bold", 25)).place(x=100, y=10)
    Label(window, text="Paste/type in the url you want unblocked here (eg: google.com):").place(x=10, y=50)
    Label(window, text="Output:").place(x=10, y=125)

    url_input = Entry(window, width=79)
    url_input.place(x=10, y=75)

    btn = Button(window, text="Reclassify/Unblock URL", command = lambda: reclassify(url_input.get()))
    btn.place(x=180, y=100)

    btn = Button(window, text="Settings", command = open_settings)
    btn.place(x=440, y=10)
    
    output_txt = st.ScrolledText(window, width=57, height=9)
    output_txt.place(x=10, y=150)
    
    window.protocol("WM_DELETE_WINDOW", close_window)  # To close the settings window if it's open
    window.mainloop()
    
    sys.exit(0)
except Exception as e:
    # Error handling by placing the error details in a traceback file that the user can submit in a Github issue
    raise Exception(e)
    messagebox.showerror("Error occured", f"An error occured, details below and in \"{getcwd()}\\\\traceback.txt\"\n{e}")
    current_time = datetime.now()
    current_time = current_time.strftime("%a, %d %b %Y %H;%M;%S")
    with open(f"Traceback {current_time}.txt", "w+") as traceback_file:
        traceback_file.write(f"Error:\n{e}\n\nTraceback:\n{format_exc()}")
        traceback_file.close()
    sys.exit(1)
