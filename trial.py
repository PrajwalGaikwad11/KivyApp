from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.popup import Popup
import qrcode
import cv2
import mysql.connector
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import os
import uuid
from kivy.uix.image import Image, AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.core.window import Window
import subprocess
import re
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput



SMTP_SERVER = 'smtp-relay.brevo.com'
SMTP_PORT = 587
EMAIL_ADDRESS = "gaikwaddeepa65@gmail.com"
EMAIL_PASSWORD = "mHY7V86P3Fh9O5qS"


Window.clearcolor = (0.2, 0.2, 0.2, 1)

class QRCodeWidget(Image):
    pass

class StylishButton(Button):
    def __init__(self, **kwargs):
        super(StylishButton, self).__init__(**kwargs)
        self.background_color = (0.1, 0.6, 0.3, 1) 
        self.font_size = '18sp'
        self.color = (1, 1, 1, 1) 
        
        if 'Create Account' in self.text:
            self.background_color = (0.1, 0.6, 0.3, 1)  
        elif 'Login' in self.text:
            self.background_color = (0.1, 0.6, 0.3, 1) 
        elif 'Formal User' in self.text:
            self.background_color = (0.2, 0.5, 0.7, 1)  
        elif 'Authorized User' in self.text:
            self.background_color = (0.8, 0.2, 0.2, 1)
            

class StylishTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StylishTextInput, self).__init__(**kwargs)
        self.background_color = (0.4, 0.4, 0.4, 1) 
        self.font_size = '18sp'
        self.foreground_color = (1, 1, 1, 1)
        

def generate_otp():
    return str(random.randint(100000, 999999))



class HomePage(App):
    
    db_config = {
    'host':'Prajwal112002',
    'user': 'your_user',
    'password':'your_password',
    'database':'your_database',
    'port':3306,
    'auth_plugin':'mysql_native_password'
}
    
    
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.data_input = TextInput()
        self.qr_code_widget = QRCodeWidget()
        self.file_chooser_dict = {}
        self.db_connection = None
        self.cursor = None
        self.current_user_uuid= None
        self.result_label = Label()
        self.uuid_input = TextInput()
        self.popup = None 
        self.layout= None
        self.new_password_input= TextInput()
        self.new_username_input=TextInput()
        
            
    def get_selected_image(self, file_chooser):
        if file_chooser.selection:
            selected_file_path = file_chooser.selection[0]
            with open(selected_file_path, 'rb') as file:
                return file.read()
        return None
    
    
    def show_user_form(self, instance):
        self.root.clear_widgets()
    
    
    def build(self):
        self.db_connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.db_connection.cursor()

        layout = FloatLayout()

        # Add a traffic light image to the background
        traffic_light_image = AsyncImage(source='C:/Users/prajw/OneDrive/Pictures/traffic_light.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(traffic_light_image)

        # Apply a faded effect to the background image using Canvas instructions
        with layout.canvas:
            Color(1, 1, 1, 0.5)
            Rectangle(pos=(0, 0), size=Window.size)

        create_account_button = StylishButton(
            text="Create Account",
            on_press=self.create_account,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        login_button = StylishButton(
            text="Login",
            on_press=self.login,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        bike_image = Image(source='C:/Users/prajw/OneDrive/Pictures/bike.png', size_hint=(0.06, 0.06), pos_hint={'center_x': 0.6, 'center_y': 0.6})
        layout.add_widget(create_account_button)
        layout.add_widget(bike_image)
        layout.add_widget(login_button)

        # Add animation for the bike
        bike_animation = Animation(pos_hint={'top': 0.9, 'center_x': 0.12}, duration=10)
        bike_animation.repeat = True
        bike_animation.start(bike_image)

        stop_sign_image = Image(source='C:/Users/prajw/OneDrive/Pictures/stop_sign.png', size_hint=(0.16, 0.16),
                                pos_hint={'left': 1, 'center_y': 0.6})  # Adjust the position
        layout.add_widget(stop_sign_image)

        # Add TextInput fields for new username and password

        screen_manager = ScreenManager()

        # Create an initial screen (you may already have this)
        initial_screen = Screen(name='initial_screen')

        # Add the initial screen to the ScreenManager
        screen_manager.add_widget(initial_screen)

        # Add the ScreenManager to the layout
        layout.add_widget(screen_manager)

        return layout
    
    
    

    def create_account(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.layout= layout
        formal_user_button = StylishButton(
            text="Formal User",
            on_press=self.formal_user,
            size_hint=(0.3, 0.07),  # Set the button size
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Adjust the position as needed
        )

        authorized_user_button = StylishButton(
            text="Authorized User",
            on_press=self.authorized_user,
            size_hint=(0.3, 0.07),  # Set the button size
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Adjust the position as needed
        )

        layout.add_widget(formal_user_button)
        layout.add_widget(authorized_user_button)

        self.root.clear_widgets()
        self.root.add_widget(layout)
        
        
        
        

    def formal_user(self, instance):
        self.layout.clear_widgets()
        self.email_input = TextInput(hint_text='Enter your email')
        self.name_input = TextInput(hint_text='Enter your name')
        self.password_input = TextInput(hint_text='Enter your password', password=True)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.password_input)

        self.verify_email_button = Button(text='Verify Email')
        self.verify_email_button.bind(on_press=self.verify_and_send_otp)
        self.layout.add_widget(self.verify_email_button)

    def authorized_user(self, instance):
        self.layout.clear_widgets()
        self.email_input = TextInput(hint_text='Enter your email')
        self.name_input = TextInput(hint_text='Enter your name')
        self.password_input = TextInput(hint_text='Enter your password', password=True)
        self.designation_input = TextInput(hint_text='Enter your designation')
        self.department_input = TextInput(hint_text='Enter your department')
        self.post_credited_input = TextInput(hint_text='Enter post credited')
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.designation_input)
        self.layout.add_widget(self.department_input)
        self.layout.add_widget(self.post_credited_input)

        self.verify_email_button = Button(text='Verify Email')
        self.verify_email_button.bind(on_press=self.verify_and_send_otp)
        self.layout.add_widget(self.verify_email_button)

    def verify_and_send_otp(self, instance):
        email = self.email_input.text.strip()
        if email:
            otp = self.send_email_verification(email)
            if otp:
                self.layout.clear_widgets()
                self.layout.add_widget(Label(text=f"OTP sent to {email}"))
                otp_input = TextInput(hint_text='Enter OTP')
                verify_otp_button = Button(text='Verify OTP')
                verify_otp_button.bind(on_press=lambda x: self.verify_otp(otp, otp_input.text.strip(), email))
                self.layout.add_widget(otp_input)
                self.layout.add_widget(verify_otp_button)
            else:
                self.layout.clear_widgets()
                self.layout.add_widget(Label(text='Failed to send OTP, please try again'))

    def verify_otp(self, sent_otp, entered_otp, email):
        if sent_otp == entered_otp:
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text='Email verified successfully!'))
            self.submit_button = Button(text='Submit')
            self.submit_button.bind(on_press=lambda x: self.submit_details(email))
            self.layout.add_widget(self.submit_button)
        else:
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text='Incorrect OTP, please try again'))

    def submit_details(self, email):
        name = self.name_input.text.strip()
        password = self.password_input.text.strip()
        user_type = 'zero'
        if hasattr(self, 'designation_input'):
            designation = self.designation_input.text.strip()
            department = self.department_input.text.strip()
            post_credited = self.post_credited_input.text.strip()
            user_type = 'one'
        else:
            designation = department = post_credited = None

        try:
            # Check if the name has been taken
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_credential WHERE name = %s", (name,))
            existing_name = cursor.fetchone()
            if existing_name:
                self.layout.clear_widgets()
                self.layout.add_widget(Label(text='This name has already been taken. Please choose another name.'))
                return

            # Check if the email ID already exists in the database
            cursor.execute("SELECT * FROM user_credential WHERE email = %s", (email,))
            existing_email = cursor.fetchone()
            if existing_email:
                self.layout.clear_widgets()
                self.layout.add_widget(Label(text='This email ID is already registered. Please use a different email ID.'))
                return

            # Inserting into database
            cursor.execute("INSERT INTO user_credential (email, name, password, user_type, designation_input, department_input, post_credited_input) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (email, name, password, user_type, designation, department, post_credited))
            self.db_connection.commit()  # Commit changes to the database
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text='Details submitted successfully!'))

            # Redirect the user to the home page (you need to implement this logic)
            self.redirect_to_home_page()

        except mysql.connector.Error as err:
            print("Error:", err)
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text='Error occurred while submitting details. Please try again.'))

        finally:
            cursor.close()



        
    def send_email_verification(self, email):
        # Generate OTP
        otp = generate_otp()

        # Email content
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Email Verification OTP'
        body = f'Your OTP for email verification is: {otp}'
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            return otp
        except Exception as e:
            print("Error sending email:", e)
            return None
        

    def redirect_to_home_page(self):
    # Implement the logic to redirect the user to the home page
        pass  

        
        
        
    
        

    def login(self, instance):
        self.root.clear_widgets()

        username_label = Label(text="Username:")
        username_input = TextInput()
        password_label = Label(text="Password:")
        password_input = TextInput(password=True)
        
        forget_credentials_button = Button(text="Forgot Credentials")
        forget_credentials_button.bind(on_press=lambda x: self.forgot_credentials())


        submit_button = Button(text="Submit", on_press=lambda x: self.check_login_credentials(username_input.text, password_input.text))

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(username_label)
        layout.add_widget(username_input)
        layout.add_widget(password_label)
        layout.add_widget(password_input)
        layout.add_widget(submit_button)
        layout.add_widget(forget_credentials_button)

        self.root.add_widget(layout)
        
    def forgot_credentials(self):
        self.root.clear_widgets()

        email_label = Label(text="Enter your Registered Emial And Click Suitable Option's :")
        email_input = TextInput()
        
        forget_username_button = Button(text="Forget Username")
        forget_username_button.bind(on_press=lambda x: self.send_otp_forget_username(email_input.text))
        forget_password_button = Button(text="Forget Password")
        forget_password_button.bind(on_press=lambda x: self.send_otp_forget_password(email_input.text))



        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(email_label)
        layout.add_widget(email_input)
        layout.add_widget(forget_username_button)
        layout.add_widget(forget_password_button)

        self.root.add_widget(layout)

    def send_otp_forget_username(self, email):
        if not self.validate_email(email):
            self.root.add_widget(Label(text="Invalid email format. Please enter a valid email."))
            return

        otp = generate_otp()
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Username Reset OTP'
        body = f'Your OTP for resetting username is: {otp}'
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            # After sending OTP, proceed with OTP verification for resetting username
            self.verify_otp_forget_username(email, otp)
        except Exception as e:
            print("Error sending email:", e)
            self.root.add_widget(Label(text="Failed to send OTP for resetting username. Please try again."))


    def send_otp_forget_password(self, email):
        if not self.validate_email(email):
            self.root.add_widget(Label(text="Invalid email format. Please enter a valid email."))
            return

        otp = generate_otp()
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Password Reset OTP'
        body = f'Your OTP for resetting password is: {otp}'
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            # After sending OTP, proceed with OTP verification for resetting password
            self.verify_otp_forget_password(email, otp)
        except Exception as e:
            print("Error sending email:", e)
            self.root.add_widget(Label(text="Failed to send OTP for resetting password. Please try again."))


    def verify_otp_forget_username(self, email, sent_otp):
        self.root.clear_widgets()
        self.root.add_widget(Label(text=f"An OTP has been sent to {email}. Please check your email and enter the OTP below."))

        otp_input = TextInput(hint_text='Enter OTP')
        verify_otp_button = Button(text='Verify OTP')
        verify_otp_button.bind(on_press=lambda x: self.verify_otp_and_reset_username(email, sent_otp, otp_input.text.strip()))
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(otp_input)
        layout.add_widget(verify_otp_button)

        self.root.add_widget(layout)


    def verify_otp_forget_password(self, email, sent_otp):
        self.root.clear_widgets()
        self.root.add_widget(Label(text=f"An OTP has been sent to {email}. Please check your email and enter the OTP below."))

        otp_input = TextInput(hint_text='Enter OTP')
        verify_otp_button = Button(text='Verify OTP')
        verify_otp_button.bind(on_press=lambda x: self.verify_otp_and_reset_password(email, sent_otp, otp_input.text.strip()))
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(otp_input)
        layout.add_widget(verify_otp_button)

        self.root.add_widget(layout)

        
        
    def verify_otp_and_reset_password(self, email, sent_otp, entered_otp):
        if sent_otp == entered_otp:
            self.root.clear_widgets()  # Clear previous widgets
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            layout.add_widget(Label(text="OTP verified. Enter new password:"))  # Inform the user
            new_password_input = TextInput(password=True, hint_text='Enter new password')
            layout.add_widget(new_password_input)  # Add TextInput for new password
            submit_button = Button(text="Submit", on_press=lambda x: self.submit_new_password(email, new_password_input.text.strip()))
            layout.add_widget(submit_button)  # Add submit button
            self.root.add_widget(layout)
        else:
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="Incorrect OTP. Please try again.")) 


    def verify_otp_and_reset_username(self, email, sent_otp, entered_otp):
        if sent_otp == entered_otp:
            self.root.clear_widgets()  # Clear previous widgets
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            layout.add_widget(Label(text="OTP verified. Enter new username:"))  # Inform the user
            new_username_input = TextInput(hint_text='Enter new username')
            layout.add_widget(new_username_input)  # Add TextInput for new username
            submit_button = Button(text="Submit", on_press=lambda x: self.submit_new_username(email, new_username_input.text.strip()))
            layout.add_widget(submit_button)  # Add submit button
            self.root.add_widget(layout)
        else:
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="Incorrect OTP. Please try again.")) 


            
            
    def submit_new_password(self, email, new_password):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE user_credential SET password = %s WHERE email = %s", (new_password, email))
            self.db_connection.commit()  # Commit the changes to the user_credential table
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="Password updated successfully!"))  # Inform the user
        except mysql.connector.Error as err:
            print("Error updating password:", err)
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="An error occurred while updating password. Please try again."))  # Inform the user
        finally:
            cursor.close()

    def submit_new_username(self, email, new_username):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE user_credential SET name = %s WHERE email = %s", (new_username, email))
            self.db_connection.commit()  # Commit the changes to the user_credential table
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="Username updated successfully!"))  # Inform the user
        except mysql.connector.Error as err:
            print("Error updating username:", err)
            self.root.clear_widgets()  # Clear previous widgets
            self.root.add_widget(Label(text="An error occurred while updating username. Please try again."))  # Inform the user
        finally:
            cursor.close()


    def check_login_credentials(self, username, password):
        query = "SELECT * FROM user_credential WHERE name = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        if result:
            self.root.clear_widgets()
            self.show_user_form()
        else:
            self.root.add_widget(Label(text="Invalid username or password"))
            
            
    def validate_email(self, email):
        # Regular expression for validating email format
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(pattern.match(email))            
            
            
            

    def open_file_picker(self, field_name):
        pictures_folder = "C:/Users/prajw/OneDrive/Pictures"
        chooser = FileChooserIconView(path=pictures_folder, filters=['.png', '.jpg', '*.jpeg'])

        # Adjust the icon size and spacing for better visibility
        chooser.icon_size = (150, 150)  # Increase icon size
        chooser.spacing = 20  # Increase spacing between icons
        chooser.icon_text = True  # Display text below each icon

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create a Popup containing the FileChooser
        file_popup = Popup(title=f"Select {field_name} Image", content=content, size_hint=(0.8, 0.8))
        file_popup.open()

        # Add the FileChooser to the Popup's content
        content.add_widget(chooser)

        # Add a button to close the Popup and store the selected file path
        close_button = Button(text="Close", size_hint=(None, None))
        close_button.bind(on_press=lambda x: self.on_file_selected(field_name, chooser.selection, file_popup))
        content.add_widget(close_button)

        # Store the FileChooser instance in the dictionary
        self.file_chooser_dict[field_name] = chooser



    def on_file_selected(self, field_name, selected_files, file_popup):
        if selected_files:
            file_path = selected_files[0]
            print(f"{field_name} file selected: {file_path}")
            with open(file_path, 'rb') as file:
                file_data = file.read()
            # Handle the file data as needed (e.g., store in the database)
        else:
            print(f"No file selected for {field_name}")

        # Close the Popup
        file_popup.dismiss()

    def get_selected_image(self, file_chooser):
        if file_chooser.selection:
            selected_file_path = file_chooser.selection[0]
            with open(selected_file_path, 'rb') as file:
                return file.read()
        return b''  # Return an empty bytes object if no file is selected

    def show_user_form(self):
        user_form_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Add text input fields for the user form
        username_input = TextInput(hint_text="Username")
        password_input = TextInput(hint_text="Password", password=True)
        name_input = TextInput(hint_text="Name")
        mobile_number_input = TextInput(hint_text="Mobile Number")
        email_input = TextInput(hint_text="Email ID")
        registration_number_input = TextInput(hint_text="Registration Number")
        engine_number_input = TextInput(hint_text="Engine Number")

        # Add FileChooserIconView for image fields
        puc_image_chooser = FileChooserIconView(path="C:/Users/prajw/OneDrive/Pictures", filters=['.png', '.jpg', '*.jpeg'])
        aadhar_card_chooser = FileChooserIconView(path="C:/Users/prajw/OneDrive/Pictures", filters=['.png', '.jpg', '*.jpeg'])
        pan_card_chooser = FileChooserIconView(path="C:/Users/prajw/OneDrive/Pictures", filters=['.png', '.jpg', '*.jpeg'])
        driving_license_chooser = FileChooserIconView(path="C:/Users/prajw/OneDrive/Pictures", filters=['.png', '.jpg', '*.jpeg'])
        
        # Adjust the size of FileChooserIconView widgets
        puc_image_chooser.size_hint_y = None
        puc_image_chooser.height = dp(40)  # Adjust the height as needed

        aadhar_card_chooser.size_hint_y = None
        aadhar_card_chooser.height = dp(40)  # Adjust the height as needed

        pan_card_chooser.size_hint_y = None
        pan_card_chooser.height = dp(40)  # Adjust the height as needed

        driving_license_chooser.size_hint_y = None
        driving_license_chooser.height = dp(40)  # Adjust the height as needed

        # Create a GridLayout for each image chooser
        def create_chooser_layout(chooser, label_text):
            chooser_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=44)
            label = Label(text=label_text)
            icon_name = Label(text=chooser.path.split('/')[-1])  # Use the last part of the path as the icon's name
            chooser_layout.add_widget(label)
            chooser_layout.add_widget(icon_name)
            chooser_layout.add_widget(chooser)
            return chooser_layout

        # Add FileChooserIconView widgets with labels and icon names before the submit button
        user_form_layout.add_widget(username_input)
        user_form_layout.add_widget(password_input)
        user_form_layout.add_widget(name_input)
        user_form_layout.add_widget(mobile_number_input)
        user_form_layout.add_widget(email_input)
        user_form_layout.add_widget(registration_number_input)
        user_form_layout.add_widget(engine_number_input)
        user_form_layout.add_widget(create_chooser_layout(puc_image_chooser, "PUC Image"))
        user_form_layout.add_widget(create_chooser_layout(aadhar_card_chooser, "Aadhar Card Image"))
        user_form_layout.add_widget(create_chooser_layout(pan_card_chooser, "PAN Card Image"))
        user_form_layout.add_widget(create_chooser_layout(driving_license_chooser, "Driving License Image"))

        # Add a button to submit the user form
        submit_button = Button(text="Submit", on_press=lambda x: self.submit_user_form(
            username_input.text, password_input.text, name_input.text, mobile_number_input.text,
            email_input.text, registration_number_input.text, engine_number_input.text,
            self.get_selected_image(puc_image_chooser), self.get_selected_image(aadhar_card_chooser),
            self.get_selected_image(pan_card_chooser), self.get_selected_image(driving_license_chooser)
        ))
        user_form_layout.add_widget(submit_button)

        # Replace the existing widgets with the user form
        self.root.clear_widgets()
        self.root.add_widget(user_form_layout)


    def submit_user_form(self, username, password, name, mobile_number, email_id,
                         registration_number_value, engine_number_value,
                         puc_image_value, aadhar_card_value, pan_card_value, driving_license_value):
        # Generate a UUID for the user
        user_uuid = str(uuid.uuid4())
        self.current_user_uuid = user_uuid

        try:
            query = "INSERT INTO user_data (uuid, username, password, name, mobile_number, email_id, " \
                    "registration_number, engine_number, puc_image_data, " \
                    "aadhar_card_data, pan_card_data, driving_license_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Check if each file data is not None before executing the query
            if None not in (puc_image_value, aadhar_card_value, pan_card_value, driving_license_value):
                values = (user_uuid, username, password, name, mobile_number, email_id,
                          registration_number_value, engine_number_value, puc_image_value,
                          aadhar_card_value, pan_card_value, driving_license_value)

                # Execute the query and commit the changes
                self.cursor.execute(query, values)
                self.db_connection.commit()

                # Save files to the user_data directory
                puc_image_value = self.save_file(user_uuid, "puc", puc_image_value)
                aadhar_card_value = self.save_file(user_uuid, "aadhar", aadhar_card_value)
                pan_card_value = self.save_file(user_uuid, "pan", pan_card_value)
                driving_license_value = self.save_file(user_uuid, "driving_license", driving_license_value)

                self.show_submission_success()
            else:
                self.show_submission_error()

        except Exception as e:
            print(f"Error in submit_user_form: {e}")
            self.show_submission_error()

    def save_file(self, user_uuid, file_type, file_data):
        file_dir = f"user_data/{user_uuid}"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = os.path.join(file_dir, f"{file_type}.jpeg")

        with open(file_path, 'wb') as file:
            file.write(file_data)

        return file_path

    def show_submission_error(self):
        error_label = Label(text="Error submitting data. Please try again.")
        self.root.clear_widgets()
        self.root.add_widget(error_label)

    def show_submission_success(self):
        success_label = Label(text="Data submitted successfully!")

        generate_qr_button = Button(text="Generate QR Code", on_press=self.generate_qr_code)
        scan_qr_button = Button(text="Scan QR Code", on_press=self.scan_qr_code)


        search_button = Button(text="Search", size_hint=(None, None), size=(200, 50))
        search_button.bind(on_press=self.launch_search)

    # Clear existing widgets
        self.root.clear_widgets()

    # Create a vertical box layout for better organization
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    # Add widgets to the layout
        layout.add_widget(success_label)
        layout.add_widget(self.qr_code_widget)
        layout.add_widget(generate_qr_button)
        layout.add_widget(scan_qr_button)
      
        layout.add_widget(search_button)

    # Add the layout to the root
        self.root.add_widget(layout)
        
    def launch_search(self, instance):
        subprocess.Popen(['python', 'C:/Users/prajw/OneDrive/Documents/rajendra sir/scan_user.py'])
        

    def generate_qr_code(self, instance):
        if self.current_user_uuid:
            user_uuid = self.current_user_uuid
            print(f"Generating QR code for user UUID: {user_uuid}")

        # Check if the "user_data" directory exists; create it if not
            user_data_dir = 'user_data'
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)

        # Generate QR code for the user UUID
            data_to_encode = user_uuid

        # Set an initial version, e.g., version 5
            version = 5

            qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
        )

        # Try adding the data to check the required version
            qr.add_data(data_to_encode)

            try:
            # Attempt to make the QR code and get the actual version used
                qr.make(fit=True)
                version = qr.version
            except qrcode.exceptions.DataOverflowError:
            # If the data overflows, increase the version
                version += 1

        # Reinitialize the QRCode instance with the correct version
            qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
        )

        # Add the data again
            qr.add_data(data_to_encode)
            qr.make(fit=True)

        # Create an image from the QR Code instance
            img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to the "user_data" directory
            qr_code_path = os.path.join(user_data_dir, f"{user_uuid}_qrcode.png")
            img.save(qr_code_path)

        # Display the generated QR code in the app
            self.qr_code_widget.source = qr_code_path
            self.show_message("QR Code generated successfully!")
        else:
            self.show_message("No user UUID available.")

    def scan_qr_code(self, instance):
    # Implement QR code scanning logic using the camera
        camera_id = 0
        delay = 1
        window_name = 'OpenCV QR Code'

        qcd = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(camera_id)

        scanned_flag = False  # Flag to track whether QR code is scanned

        while not scanned_flag:
            ret, frame = cap.read()

            if ret:
                ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
                if ret_qr:
                    for s, p in zip(decoded_info, points):
                        if s:
                            print("Scanned QR Code Data:", s)
                        # Display the scanned UUID in a popup
                            self.show_scanned_data_screen(s)
                            color = (0, 255, 0)
                            scanned_flag = True  # Set the flag to True once scanned
                            break
                        else:
                            color = (255, 0, 0)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
                cv2.imshow(window_name, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

    # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

    def show_scanned_data_screen(self, scanned_uuid):
        message = f"ID: {scanned_uuid}"

        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))

        copy_button = Button(text="Copy to Clipboard", size_hint=(1, 0.2))
        copy_button.bind(on_press=lambda instance: self.copy_to_clipboard(scanned_uuid))
        popup_layout.add_widget(copy_button)

        # Increase the width of the popup
        popup_width = 400

        self.popup = Popup(title="Scanned Data", content=popup_layout, size_hint=(None, None), size=(popup_width, 200))
        self.popup.open()

    def close_popup(self, instance):
        if self.popup:
            self.popup.dismiss()

    def copy_to_clipboard(self, text):
        Clipboard.copy(text)
        self.show_message("UUID copied to clipboard!")
        
    

                
    def show_message(self, message):
        popup = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        popup.add_widget(close_button)

        popup_window = Popup(title="Message", content=popup, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup_window.dismiss)
        popup_window.open()
        
        
if __name__ == "__main__":
    HomePage().run()