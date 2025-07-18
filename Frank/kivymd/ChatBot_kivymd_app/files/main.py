import kivymd
from kivymd.uix.chip.chip import MDIcon
from kivy.uix.accordion import Widget
from kivymd.uix.banner.banner import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen , ScreenManager , FadeTransition
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from openai.ai_base import get_llm
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.core.clipboard import Clipboard
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineIconListItem,IconLeftWidgetWithoutTouch,IconRightWidget
from kivymd.uix.list import MDList
from kivy.uix.image import Image
from sub_func import is_connected , is_legit_email
import random
from server_opt_dp import add_user_sign_in_data , check_user_login , check_if_exist , get_user_id_num
from server_opt_dp import Load_user_data
import json
import threading
import time
# kivymd.require(1.1.1)


History=[]
session_storage = []
class Home(Screen):

    def to_new_screen(self,name:str):
        self.manager.current=name

    def menu(self):
      setting_menu=MDGridBottomSheet()

      setting_menu.add_item(
      text='account',
      icon_src='./icon_sets/account.png',
      callback= lambda X: self.to_new_screen("account")
    )

      setting_menu.add_item(
      text='Clear chart',
      icon_src='./icon_sets/broom.png',
      callback= lambda X:toast("sdsdsd")
    )

      setting_menu.add_item(
      text='Contact Usa',
      icon_src='./icon_sets/call.png',
      callback= lambda x:toast("click"),

    )
      setting_menu.add_item(
      text='Community',
      icon_src='./icon_sets/community.png',
      callback= lambda x:self.to_new_screen('community')
    )
      setting_menu.radius_from = 'top_right'
      setting_menu.open()

    def save_offline_chat(self):
         with open('chart_db.json' , 'r') as file:
           data = json.load(file)
           data["offline_chats"].append(self.get_ill_response_api())

    def get_ill_response_api(self):
          self.question = f"""{self.ids.question_input.text}"""
          self.timestamp = time.time()
          self.chart_is_not_empty = False
          self.chart_time = time.strftime("%a, %B %d, %Y %H:%M:%S", time.localtime(self.timestamp))
          self.current_time = time.strftime("%H:%M:%S")
          response = ''
          history = History
          if self.question:

              try:
                if self.question:
                    rep , history = get_llm(self.question , history)
                    response = rep
                    self.chart_is_not_empty = True
                    # print(session_storage)
              except Exception as e:
                  print(f"error:{e}")

              session_storage.append(
                    {
                    "question":self.question,
                    "time":self.chart_time,
                    "reply":response,
                    "current_time":self.current_time
                    }
                  )

              with open('logged.json','r') as file:
               data = json.load(file)
              for item in data:
                print(item)

              if item['log_profile']:
                load = Load_user_data(item['client_username'],item['client_id_num'])
                chat = { "Question":self.question, "Time":self.chart_time, "Reply":response , "chat_id":random.randint(10000,200000)}
                load.save_client_chat(chat)

              Clock.schedule_once(self.on_task_complete)
          else:
            exit()

    def start_task(self):
      if is_connected():
        if self.ids.question_input.text:
          self.ids.send_button.disabled = True
          self.ids.ai_spinner.active = True
          self.ids.send_button.opacity =  0.0

          # Clock.schedule_once(lambda dt: self.ids.ai_spinner.__setattr__('active',True))
          threading.Thread(target=self.get_ill_response_api).start()
      else:
        content = MDBoxLayout(orientation='vertical', spacing="5dp",size_hint_y=None, height="70dp")
        img = Image(
          source='./icon_sets/network_issues.png',
          allow_stretch= True,
          pos_hint = {'center_x': 0.5,'center_y': 0.5},
          size = ('70dp','70dp'),
          size_hint=(None, None)

        )

        label= MDLabel(text='Turn on WIFI or Mobile Data',theme_text_color='Error',font_size='7sp')
        content.add_widget(img)
        # content.add_widget(label)
        self.dialog = MDDialog(
            title="Oops! ..Something went wrong",
            type="custom",
            content_cls=content
        )
        self.dialog.open()

    def on_task_complete(self,dt):
        try:
            if len(session_storage) >= 1:
                main_content_box = self.ids.content_box
                get_index_chat = session_storage[-1]
                qaustion = get_index_chat.get("question")
                answer = get_index_chat.get("reply")
                current_time = get_index_chat.get("current_time")

                user_qaustion_label  = MDLabel(
                    size_hint_y = None,
                    adaptive_height = True,
                    theme_text_color = 'Custom',
                    text = f"{qaustion}",
                    halign= 'center',
                    text_size = (0.40,None),
                    text_color = 'white',
                    font_size= '23sp',
                )

                user_response_label  = MDLabel(
                    size_hint_y = None,
                    adaptive_height = True,
                    theme_text_color = 'Custom',
                    text = f"{answer}",
                    text_color = 'white',
                    text_size = (None,None),
                    font_size= '18sp',
                )

                current_time_label = MDLabel(
                  text=f'{current_time}',
                  theme_text_color = 'Secondary',
                  font_style = 'Caption',
                  adaptive_height = True,

                  halign = 'right',
                  text_size = (0.020,0.020),
                  size_hint_y =  None,

                )

                copy_button = MDIconButton(
                  icon = 'clipboard-arrow-down-outline',
                  icon_size = "19sp",
                  pos_hint = {'right': 1, 'center_y':0.97},
                  theme_icon_color = "Secondary",
                  on_release=lambda X: self.copy_text_clipbord(user_response_label.text)

                )

                user_qaustion_card = MDCard(
                  radius = [10,10,10,10],
                  size_hint_y =  None,
                  pos_hint =  {'right': 1,},
                  size_hint_x = 0.5,

                  md_bg_color= (0.949, 0.031, 0.424),
                  orientation =  'vertical'
                )

                user_response_card = MDCard(
                    size_hint_y =  None,
                    radius = [5,5,5,5],
                    #  font_name='seguiemj',
                    size_hint_x = 0.90,
                    orientation =  'vertical'
                )
                randomSpace = Widget(
                  size_hint = (1, None),
                  height = 50,

                  )

                user_qaustion_label.bind(texture_size = lambda i , x: setattr(user_qaustion_card, 'height' , x[1]))
                user_response_label.bind(texture_size = lambda i , x: setattr(user_response_card, 'height' , x[1]))
                user_qaustion_card.add_widget(user_qaustion_label)
                user_response_card.add_widget(user_response_label)
                main_content_box.add_widget(user_qaustion_card)
                main_content_box.add_widget(current_time_label)
                main_content_box.add_widget(copy_button)
                main_content_box.add_widget(user_response_card)
                main_content_box.add_widget(randomSpace)

                self.ids.ai_spinner.active = False
                self.ids.send_button.disabled = False
                self.ids.send_button.opacity =  1
                self.ids.question_input.text = ""

        except Exception as e:
          print(e)

    def on_enter(self):
       try:
          with open('logged.json','r') as file:
            data = json.load(file)
            for item in data:
              print(item)

          with open('chart_db.json','r') as file:
            dat = json.load(file)
            for chat in dat:
              print(chat)


            if item['log_profile']:
              load = Load_user_data(item['client_username'],item['client_id_num'])
              # name = load.get_user_name()
              username = load.get_user_username()
              chip_name= self.ids.name_holder
              chip_name.text=username
              if chat['client_id_num'] is not None:
                 if chat['client_id_num'] == item["client_id_num"]:
                  #  del session_storage[:]
                   del History[:]
                   with open("chart_db.json",'w') as jj:
                        sj = json.dump(dat,jj,indent=4)
            else:
               chip_name= self.ids.name_holder
               chip_name.text="Guest"

       except Exception as err:
           print(f"{err}")

    def copy_text_clipbord(self,text):
        Clipboard.copy(text)
        return toast("Copied" ,  duration =1.5)

    def clear_chat(self):
        main_content_box = self.ids.content_box
        if  session_storage:
           main_content_box.clear_widgets()
           del History[:]
           print("clicked")
           print(History)
        else:
          toast('Chat is already empty!!' ,duration= 1.9)

class Sign_Up(Screen):
    def gender_select(self):
      menu_items=[
        {

            "viewclass": "OneLineListItem",
            "text": "Female",
            "on_release": lambda x="Female": self.set_item(x),
        },
        {
            "viewclass": "OneLineListItem",
            "text": "Male",
            "on_release": lambda x="Male": self.set_item(x),
        },
        {
            "viewclass": "OneLineListItem",
            "text": "Others",
            "on_release": lambda x="Others": self.set_item(x),
        }
      ]

      self.menu = MDDropdownMenu(
            caller=self.ids.gender,
            items=menu_items,
            position="auto",
            height= 1,
            width_mult=2,
        )
      self.menu.open()

    def set_item(self,text__item):
        self.ids.gender.text = text__item
        self.menu.dismiss()

    def check_username(self,text:str):
       has_symbol = False
       has_lower = False
       has_upper = False
       has_len = False
       has_digit = False
       is_valide = False
       field = self.ids.username

       symbol = "!@$%^&*+#"

       for char in text:
          if char in symbol:
            has_symbol = True
          if "A" <= char <= "Z":
            has_upper = True
          if "a" <= char <= "z":
            has_lower = True
          if "0" <= char <= "9":
            has_digit = True
       if len(text) > 4:
         has_len = True

       if has_lower and has_len and has_digit :
          is_valide = True
       return is_valide

    def check_name(self, text:str):
       has_lower = False
       has_len = False
       is_alphabet = False
       is_valide = False
       name = text.split()
       splited_word = "".join(name)

       for i in splited_word:
         if splited_word.isalpha():
           is_alphabet = True
         if "a" <= i <="z":
           has_lower = True
       if len(text.split()) == 2:
         has_len=True


       if is_alphabet and has_len and has_lower:
         is_valide = True

       return is_valide

    def check_password(self, text:str):
       has_symbol = False
       has_lower = False
       has_digit = False
       has_upper = False
       is_long = False
       is_valide = False
       symbol = "!.@$%^&*+#"
       for password  in text:
         if "a" <= password <= "z":
           has_lower = True
         if "A" <= password <= "Z":
           has_upper = True
         if "0" <= password <= "9":
           has_digit = True
         if password in symbol:
           has_symbol = True

       if len(text) >= 8 :
         is_long = True

       if has_digit and has_lower and has_symbol and has_upper and has_upper  and is_long:
         is_valide = True
       return is_valide

    def check_email(self,email:str):
      is_ligit = False
      if is_legit_email(email):
        is_ligit = True
      return is_ligit

    def check_gender(self,gender:str):
      is_gender_valide = False
      if gender.strip() == "Female" or gender.strip() == "Others" or gender.strip() == "Male":
        is_gender_valide = True
      return is_gender_valide

    def save_user_data(self):
       name = self.ids.name.text
       username = self.ids.username.text
       email = self.ids.email.text
       gender = self.ids.gender.text
       password = self.ids.passwords.text
       re_password = self.ids.confirm_pass.text
      # validation bool
       email_bool = False
       name_bool = False
       username_bool = False
       gender_bool = False
       password_bool = False
       re_password_bool = False
       validation_bool = False
      #  err message
       name_err = self.ids.name
       username_err = self.ids.username
       email_err = self.ids.email
       gender_err = self.ids.gender
       password_err = self.ids.passwords
       re_password_err = self.ids.confirm_pass
      #  validation
       if name and username and email and gender and password and re_password:
        #  email validation
          if self.check_email(email):
            email_err.helper_text = f"{email}"
            email_err.helper_text_color_normal = "green"
            email_bool = True
          else:
            email_err.helper_text_color_normal = "red"
            email_err.line_color_focus = "red"
            email_err.line_color_focus = 'red'

           # gender validation
          if self.check_gender(gender):
            gender_err.helper_text_color_normal = "green"
            gender_bool = True
          else:
             gender_err.helper_text_color_normal = "red"
             gender_err.line_color_focus = 'red'

          # password validation
          if self.check_password(password):
             password_err.helper_text = "Password is Strong"
             password_err.helper_text_color_normal = "green"
             password_bool = True
          else:
            password_err.helper_text_color_normal = "red"
            password_err.line_color_focus='red'

          if self.check_username(username):
            username_err.helper_text = "Great username!"
            username_err.helper_text_color_normal='green'
            username_bool = True
          else:
            username_err.helper_text_color_normal='red'
            username_err.line_color_focus='red'

          if self.check_name(name):
             name_err.helper_text = "Your name is Okey"
             name_err.helper_text_color_normal = "green"
             name_bool = True
          else:
            name_err.helper_text_color_normal = "red"
            name_err.line_color_focus = "red"
            # password match
          if re_password == password:
            re_password_err.helper_text = "Password match  ✔️"
            re_password_err.helper_text_color_normal="green"
            re_password_bool = True
          else:
            re_password_err.helper_text_color_normal = 'red'
            re_password_err.line_color_focus = "red"
            re_password_err.helper_text = "Password did not match"
       else:
          self.dialog = MDDialog(
          title = 'Incomplete Fields',
          text="Please!....fill all fields are required.",

          buttons=[
                MDFlatButton(
                      text="Got it",
                      theme_text_color="Custom",
                      text_color='white',
                      on_release=lambda x: self.close_dialog()
                  ),
                ],
            )
          self.dialog.open()

       if name_bool and gender_bool and username_bool and password_bool and re_password_bool and email_bool:
          validation_bool = True
       return validation_bool

    def upload_user_data(self):
       name = self.ids.name.text
       username = self.ids.username.text
       email = self.ids.email.text
       gender = self.ids.gender.text
       password = self.ids.passwords.text
       isLogged = True

       if self.save_user_data():
         if not check_if_exist(username):
              add_user_sign_in_data(username,name.lower(),email,gender,password)
              toast("Data saved to server")

              isLogged = True
              #  saving log info fo reference
              #  file ="logged_hash.json"
              f = "logged.json"
              with open(f,'r') as json_file:
                data = json.load(json_file)

              for i in data:
                i["log_profile"]=True
                i["guest_mode"]=False
                i["client_id_num"]=get_user_id_num(username)
                i["client_username"]=username

              with open(f,'w') as j:
                jj = json.dump(data,j,indent=4)

              # with open('chart_db.json','r') as file:
              #   dat = json.load(file)
              #   for chat in dat:
              #     chat['client_id_num'] = get_user_id_num(username)
              # with open("chart_db.json",'w') as jj:
              #   sj = json.dump(dat,jj,indent=4)
              del session_storage[:]
              del History[:]

              self.manager.current = "Home"

         else:
          self.dialog = MDDialog(
          title = 'Username Error!',
          text=f"Sorry! {name.split(' ',1)[0]}. That username already exist, Make it unique.",

          buttons=[
                MDFlatButton(
                      text="Got it",
                      theme_text_color="Custom",
                      text_color='white',
                      on_release=lambda x: self.close_dialog()
                  ),
                ],
            )
          self.dialog.open()

    def close_dialog(self):
       self.dialog.dismiss()
    def on_enter(self):
       name = self.ids.name
       username = self.ids.username
       email = self.ids.email
       gender = self.ids.gender
       password = self.ids.passwords
       re_password = self.ids.confirm_pass

       name.text=""
       username.text=""
       password.text=''
       re_password.text=""
       gender.text=""
       email.text=""

class Sign_In(Screen):
    def login(self):
       username = self.ids.username.text
       password = self.ids.passwords.text
       try:
         if username and password:
           if check_user_login(username,password):
               f = "logged.json"
               with open(f,'r') as json_file:
                    data = json.load(json_file)

               for i in data:
                i["log_profile"]=True
                i["guest_mode"]=False
                i["client_id_num"]=get_user_id_num(username)
                i["client_username"]=username

               with open(f,'w') as j:
                 jj = json.dump(data,j,indent=4)
              #  self.ids.login_btn.disabled = False
              #  self.ids.ai_spinner.active = False
               self.manager.current = "Home"
               toast("Welcome back.")

           elif not check_user_login(username,password) :
              # self.ids.username.line_color_focus="red"
              # self.ids.passwords.line_color_focus = "red"
              toast("Invalid name or email")
           else:
             toast("somthing went wrong")
         else:
           toast("Fill all fields")

       except Exception as err:
           print(err)

    def on_enter(self):
       username = self.ids.username
       password = self.ids.passwords

       username.text=""
       password.text=""


class Land_Page(Screen):
   def on_enter(self):
     float_lay = self.ids.boom_boom
     float_lay.remove_widget(self.ids.btn_card)


   def triger_widget(self):
      float_lay = self.ids.boom_boom
      card = self.ids.btn_card
      return float_lay.add_widget(card)

   def activate_guest_mode(self):
        with open('logged.json','r') as file:
            data = json.load(file)
            for item in data:
              print(item)
              item["guest_mode"] = True

        with open('logged.json','w') as j:
                 jj = json.dump(data,j,indent=4)

        self.manager.transition.direction='left'
        self.manager.current = 'splash'

class Account(Screen):
  def __init_(self):
    self.card = None

  def clean_user_chat(self):
      with open('logged.json','r') as file:
            data = json.load(file)
            for item in data:
              pass
      load = Load_user_data(item["client_username"],item["client_id_num"])

      if load.get_chat_length():
        load.delete_user_conversation()
        del History[:]
        del session_storage[:]
        self.close_dialog()
        toast("Coversations have been Deleted.")

      elif not load.get_chat_length():
        self.close_dialog()
        toast("Start a Coversation First")

      else:
        toast("Somthing went wrong")

  def delete_chart(self):
      with open('logged.json','r') as file:
            data = json.load(file)
            for item in data:
              pass
      # load = Load_user_data(item["client_username"],item["client_id_num"])

      if item["log_profile"]:
          # if load.get_chat_length():
          self.dialog = MDDialog(
              title = 'Delete Conversation',
              text="Your chat will be deleted permanently. Are sure?",
              buttons=[
                    MDFlatButton(
                          text="CANCEL",
                          theme_text_color="Custom",
                          text_color='white',
                          on_release=lambda x: self.close_dialog()
                      ),
                      MDFlatButton(
                          text="DELETE",
                          theme_text_color="Custom",
                          text_color='red',
                          on_release=lambda x:self.clean_user_chat()

                        ),
                    ],
                )
          self.dialog.open()
      elif item['guest_mode']:
        toast("Your Conversation are not saved. Login Save Coversation")

  def close_dialog(self):
    self.dialog.dismiss()

  def on_enter(self):
    email = self.ids.email_label
    name = self.ids.name_label
    acc_id = self.ids.acc_id
    top_= self.ids.top_name
    delete_acc_list = self.ids.delete_acc
    login = self.ids.login_list
    delete_chart_la = self.ids.delete_conv
    try:
          with open('logged.json','r') as file:
            data = json.load(file)
            for item in data:
              print(item)

            if item['log_profile']:
              load = Load_user_data(item['client_username'],item['client_id_num'])
              names = load.get_user_name()
              emails = load.get_user_email()
              acc = load.get_user_id()
              username = load.get_user_username()
              # fl = next(zip(*names.split()))
              email.secondary_text = emails
              name.secondary_text = names
              acc_id.secondary_text = str(acc)
              top_.secondary_text = username
              login.text="Sign Out"
              login.icon_color="red"
              # login.on_release=self.logout()
              delete_chart_la.disabled = False
              delete_acc_list.disabled = False
              main = self.ids.main_body
              main.remove_widget(self.card)

            elif item["guest_mode"]:
              email.secondary_text = "not signed in"
              name.secondary_text = "not signed in"
              acc_id.secondary_text ="not signed in"
              top_.secondary_text = "not signed in"
              login.text="Login"
              login.icon_color="red"
              main = self.ids.main_body
              main.remove_widget(self.card)
              # login.on_release=self.logout()
              delete_chart_la.disabled = True
              delete_acc_list.disabled = True

    except Exception as err:
           print(f"{err}")

  def varify_log_out(self):
     with open("logged.json") as file:
       data = json.load(file)

     for item in data:
         pass

     if item["log_profile"]:
        self.dialog = MDDialog(
              title = 'LOG OUT CONFIRMATION',
              text="The next you login you will have to enter your details again. Are you sure?",
              buttons=[
                    MDFlatButton(
                          text="Cancel",
                          theme_text_color="Custom",
                          text_color='white',
                          on_release=lambda x: self.close_dialog()
                      ),
                      MDFlatButton(
                          text="Continue",
                          theme_text_color="Custom",
                          # bold=True,
                          text_color='red',
                          on_release= lambda X: self.logout()
                        ),
                    ],
                )

        self.dialog.open()

     elif item["guest_mode"]:
        toast("Directing you to sign up page.")
        return Clock.schedule_once(self.go_to_login,1)
     else:
       toast("Somthing went wrong")

  def close_dialog(self):
    self.dialog.dismiss()

  def logout(self):
      with open("logged.json") as file:
        data = json.load(file)

      for item in data:
        item["log_profile"]=False
        item["guest_mode"]=False
        item["client_id_num"]=None
        item["client_username"]=""

      with open('logged.json','w') as j:
        jj = json.dump(data,j,indent=4)

      self.close_dialog()
      toast("Log out Succesful")
      del session_storage[:]
      return Clock.schedule_once(self.go_to_home,1)

    #  elif item["guest_mode"]:
    #    self.close_dialog()
    #    toast("Directing you to sign up page.")
    #    return Clock.schedule_once(self.go_to_login,1)

  def go_to_login(self,dt):
     self.manager.current = "sign_in"

  def go_to_home(self,dt):
     self.manager.current = "splash"

  def check_name(self):
      with open("logged.json") as file:
        data = json.load(file)

      vg = None
      for item in data:
        pass
      if  item["log_profile"]:
          value = Load_user_data(item["client_username"],item["client_id_num"]).get_user_name()
          vg = value.split(' ',1)[0]
      else:
         vg = ""
      return vg

  def delete_account(self):
    self.card = MDCard(
        pos_hint = {'center_x':0.5 , 'center_y':0.5 },
        size_hint= (0.99, 0.98),
        orientation= 'vertical',
        spacing= 20
    )
    delete_button = MDRaisedButton(
        text="Delete Account",
        pos_hint={'center_x':0.5 , 'center_y':0.47},
        size_hint=(0.9,None),
        elevation= 4,
        height="90dp",
        on_release=lambda x:self.remove_account(),
        font_size= "30sp",
        theme_text_color= 'Custom',
        text_color= "white",
        font_style='Button',
        md_bg_color=(0.949, 0.031, 0.424),
    )
    cancel_btn = MDIconButton(
        icon="close-circle",
        pos_hint= {'top':0.99,'center_x': .5},
        icon_size="40",
        size_hint_y = None,
        theme_icon_color='Custom',
        icon_color="white",
        on_release=lambda x:self.remove_card()
        )

    img = Image(
      source="./icon_sets/trash_op.png",
      pos_hint=  {'center_x': 0.5,'center_y': 0.90},
      allow_stretch=False
    )

    del_msg = MDLabel(
      halign="center",
      bold = True,
      size_hint_y= None,
      pos_hint={'top': 0.80},
      text=f"{self.check_name().capitalize()}. Your Data and Coonversation will be Erased forever. Are sure you want to proceed."
      )
    space = Widget(
        size_hint = (None, None),
        size =('70dp','70dp')
    )
    space2 = Widget(
        size_hint = (None, None),
        size =('5dp','5dp')
    )

    self.card.add_widget(cancel_btn)
    self.card.add_widget(img)
    self.card.add_widget(del_msg)
    # self.card.add_widget(field)
    self.card.add_widget(space2)
    self.card.add_widget(delete_button)
    self.card.add_widget(space)
    main = self.ids.main_body
    main.add_widget(self.card)
    return self.card

  def remove_account(self):
      with open('logged.json' , 'r') as file:
           data = json.load(file)

      for item in data:
          pass

      if  item["log_profile"]:
          load = Load_user_data(item['client_username'],item["client_id_num"])
          load.delete_account()
          item["log_profile"]=False
          item['client_username']=""
          item["client_id_num"]=None
          toast("Account deleted")
          del session_storage[:]
          with open('logged.json' , 'w') as j:
              jj = json.dump(data,j,indent=4)
          return Clock.schedule_once(self.go_to_home,1)

  def remove_card(self):
    main = self.ids.main_body
    main.remove_widget(self.card)


class Chat(Screen):

  def navigation(self,location:str):
    c = self.manager.current = location
    return c

  def start_task(self):
      self.navigation('activity')
      threading.Thread(target=self.on_enter).start()

  def on_enter(self):
    with open("logged.json") as file:
       data = json.load(file)
    for item in data:
      pass
    self.card = MDCard(
            pos_hint= {'center_x':0.5 , 'center_y':0.5 },
            size_hint=( 0.99, 0.99),
            orientation= 'vertical',
            spacing= 3
        )

    if item["log_profile"]:
       data = Load_user_data(item['client_username'],item['client_id_num'])
       conversation = data.get_user_conversation()
      #  layout_box = self.ids.box
       histo_list = self.ids.box
       self.ids.main_chat_box.remove_widget(self.card)
       if  data.get_chat_length():
            time_of_chat = ''
            reply =''
            question=''
            for chat in conversation:
                question = chat['Question']
                time_of_chat = chat["Time"]
                reply = chat['Reply']
                #  chat_id = chat['chat_id']

                chat_card = ThreeLineIconListItem(
                      IconLeftWidgetWithoutTouch(
                          icon="chat",
                          theme_icon_color = 'Custom',
                          icon_color ="white",
                          icon_size = "20px"
                        ),

                      #  IconRightWidget(
                      #     theme_icon_color = 'Custom',
                      #     icon_color ="red",
                      #     icon_size = "22px",
                      #    icon="delete"

                      #  ),
                      text = f"{question}",
                      secondary_text = f"{reply}",
                      tertiary_text = f"{time_of_chat}"
                )
                histo_list.add_widget(chat_card)
       if not data.get_chat_length():
          img,msg = self.no_chat_widget()
          self.ids.main_box.orientation = 'vertical'
          self.ids.main_box.add_widget(img)
          self.ids.main_box.add_widget(msg)


    if item["guest_mode"]:
        #  g_card = self.ids.guest_card
        #  g_card.orientation = 'vertical'
        #  b_body = self.ids.main_chat_box
          img,btn,btn1,wid,wid3 = self.guest_mode_card()
          box = self.ids.main_box
          box.add_widget(img)
          box.add_widget(btn)
          box.add_widget(btn1)
          box.add_widget(wid)
          box.add_widget(wid3)


    if not item["guest_mode"] and not item["log_profile"]:
        toast("Somthing went wrong")
        return self.navigation("splash")
    Clock.schedule_once(toast("Connected to server."))


  def on_leave(self):
      self.ids.box.clear_widgets()
      self.ids.main_box.clear_widgets()
      # self.ids.main_box.remove_widget(img,msg = self.no_chat_widget())

  def no_chat_widget(self):
          msg = MDLabel(
                text='Start Conversation.\n No Conversations Found \n',
                font_size='30sp',
                halign='center',
                pos_hint = {'top':0.78}

            )
          img = Image(
            source = "./icon_sets/eempty chat.gif",
            allow_stretch= False,
            pos_hint = {'center_x': 0.5,'center_y': 0.55},
            size = ('300dp','300dp'),
            size_hint=(None, None)
            )
          return img,msg

  def guest_mode_card(self):
          img =  Image(
          source='./icon_sets/guest_icon.png',
          allow_stretch= False,
          pos_hint= {'center_x': 0.5,'center_y': 0.55},
          size=( '200dp','200dp'),
          size_hint=(None, None)
          )

          btn1=  MDRaisedButton(
                text='May be Later',
                font_style=  'Button',
                text_color= "white",
                font_size= "27sp",
                pos_hint= {'center_x': 0.5,'center_y': 0.50},
                size_hint= (0.8,None),
                elevation= 3,
                height= "53dp",
                md_bg_color= 'green',
                on_release =lambda x: self.navigation("Home")
                )

          wid = Widget(
                size_hint= (None, None),
                height= '10dp')

          btn2 = MDRaisedButton(
                text='Login',
                font_style=  'Button',
                text_color="white",
                font_size="30sp",
                pos_hint={'center_x': 0.5,'center_y': 0.50},
                size_hint=(0.8,None),
                elevation= 3,
                height= "53dp",
                md_bg_color= (0.949, 0.031, 0.424),
                on_release= lambda x: self.navigation("sign_in"))

          wid3 =   Widget(
                size_hint=(None, None),
                height= '50dp'
                )
          return img,btn1,btn2,wid,wid3


class Search_Chat(Screen):
  pass
class Share_App(Screen):
  pass
class Community(Screen):
  pass
class register_screen(Screen):
  pass
class Activity_screen(Screen):
  pass


class splash_page(Screen):
  def on_enter(self,*args):
    Clock.schedule_once(self.go_to_home,random.randint(5,20))
  def go_to_home(self,dt):

    with open("logged.json") as file:
       data = json.load(file)
    for item in data:
      pass

    if item["log_profile"] and not item["guest_mode"]:
      self.manager.current = "Home"

    elif not item["log_profile"] and  item["guest_mode"]:
        self.manager.current = "Home"
    elif  not item["log_profile"] and not item["guest_mode"]:
      self.manager.current = "landing_page"
    else:
      self.manager.current = "landing_page"

class main(MDApp):
    def build(self):
        Builder.load_file("app.kv")
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.font_styles["Custom"] = ["seguiemj" , 24 ,False , 0.15]
        screens= ScreenManager()
        screens.transition=FadeTransition()

        with open('logged.json' , 'r') as file:
           data = json.load(file)
        for item in data:
           print(item)

        if item["log_profile"]:
          screens.add_widget(Activity_screen(name='activity'))
          screens.add_widget(splash_page(name='splash'))
          screens.add_widget(Community(name='community'))
          # screens.add_widget(Share_App(name='share_app'))
          # screens.add_widget(Search_Chat(name='search'))
          screens.add_widget(Chat(name='chat'))
          screens.add_widget(Account(name="account"))
          screens.add_widget(Activity_screen(name='activity'))
          screens.add_widget(Home(name="Home"))
          screens.add_widget(Sign_In(name='sign_in'))
          screens.add_widget(Sign_Up(name="sign_up"))
          screens.add_widget(Land_Page(name='landing_page'))

        else:
          screens.add_widget(splash_page(name='splash'))
          screens.add_widget(Land_Page(name='landing_page'))
          screens.add_widget(Sign_In(name='sign_in'))
          screens.add_widget(Sign_Up(name="sign_up"))
          screens.add_widget(Community(name='community'))
          # screens.add_widget(Share_App(name='share_app'))
          # screens.add_widget(Search_Chat(name='search'))
          screens.add_widget(Chat(name='chat'))
          screens.add_widget(Account(name="account"))
          screens.add_widget(Home(name="Home"))

        return screens

if __name__ == "__main__":
    main().run()