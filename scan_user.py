from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
import mysql.connector
from mysql.connector import Error
import io
from kivy.core.image import Image as CoreImage

class HoverableImage(ButtonBehavior, Image):
    pass

class DatabaseApp(App):

    def __init__(self, **kwargs):
        super(DatabaseApp, self).__init__(**kwargs)
        self.db_connection = None
        self.popup = None
        self.uuid_label = None
        self.uuid_label = Label(text='')
        self.user_type = None  # Added user_type attribute

    def build(self):
        # Connect to the database
        self.connect_to_database()

        self.layout = BoxLayout(orientation='vertical')

        # Ask for password
        self.password_input = TextInput(hint_text='Enter Password', password=True)
        self.login_button = Button(text='Login', on_press=self.login)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)

        return self.layout

    def login(self, instance):
        # Check password
        password = self.password_input.text.strip()

        if not password:
            self.show_message("Please enter a password.")
            return

        user_type = self.get_user_type(password)

        if user_type is None:
            self.show_message("Incorrect password.")
            return

        # Store user_type obtained from the database
        self.user_type = user_type  
        print(f"User type set to: {self.user_type}")  # Debug print

        # If login successful, show record details input fields
        self.layout.clear_widgets()
        self.uuid_input = TextInput(hint_text='Enter UUID')
        self.search_button = Button(text='Search', on_press=self.search_record)
        self.layout.add_widget(self.uuid_input)
        self.layout.add_widget(self.search_button)


    def get_user_type(self, password):
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT user_type FROM user_credential WHERE password = %s"
            cursor.execute(query, (password,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                user_type = result['user_type']
                print(f"User type retrieved from database: {user_type}")
                return user_type
            else:
                print("No user type found for the given password.")
                return None
        except Error as e:
            print("Error fetching user type from database:", e)
            raise Exception("Failed to fetch user type from database")



    def search_record(self, instance):
        print(f"User type during search: {self.user_type}")  # Debug print
        if self.user_type is None:
            self.show_message("Please log in first.")
            return

        user_uuid = self.uuid_input.text.strip()

        if not user_uuid:
            self.show_message("Please enter a UUID.")
            return

        record = self.get_record_from_database(user_uuid)
        if record:
            if self.user_type=="zero":
                print("Executing show_basic_details")  # Debug print
                self.show_basic_details(record)
            else:
                print("Executing show_all_details")  # Debug print
                self.show_all_details(record)
        else:
            self.show_message("UUID not found in the database")

    def show_basic_details(self, record):
        print("Inside show_basic_details")  # Debug print
        popup_layout = BoxLayout(orientation='vertical')
        self.uuid_label.text = f'UUID: {record["uuid"]}'
        username_label = Label(text=f'Username: {record["username"]}')
        email_id_label = Label(text=f'Email ID: {record["email_id"]}')
        popup_layout.add_widget(self.uuid_label)
        popup_layout.add_widget(username_label)
        popup_layout.add_widget(email_id_label)
        self.popup = Popup(title='Record Details', content=popup_layout, size_hint=(None, None), size=(800, 400))
        self.popup.open()

    def show_all_details(self, record):
        print("Inside show_all_details")  # Debug print
        popup_layout = BoxLayout(orientation='vertical')
        self.uuid_label.text = f'UUID: {record["uuid"]}'
        username_label = Label(text=f'Username: {record["username"]}')
        name_label = Label(text=f'Name: {record["name"]}')
        mobile_number_label = Label(text=f'Mobile Number: {record["mobile_number"]}')
        email_id_label = Label(text=f'Email ID: {record["email_id"]}')
        popup_layout.add_widget(self.uuid_label)
        popup_layout.add_widget(username_label)
        popup_layout.add_widget(name_label)
        popup_layout.add_widget(mobile_number_label)
        popup_layout.add_widget(email_id_label)
        self.add_image_with_label(popup_layout, "Pan Card", record['pan_card_data'])
        self.add_image_with_label(popup_layout, "Aadhar Card", record['aadhar_card_data'])
        self.add_image_with_label(popup_layout, "PUC Image", record['puc_image_data'])
        self.add_image_with_label(popup_layout, "Driving License", record['driving_license_data'])

        self.popup = Popup(title='Record Details', content=popup_layout, size_hint=(None, None), size=(800, 600))
        self.popup.open()


    def add_image_with_label(self, layout, label_text, image_data):
            # Add a BoxLayout to encapsulate the label and image
            box_layout = BoxLayout(orientation='horizontal')

            # Add label for the image
            label = Label(text=label_text)
            box_layout.add_widget(label)

            # Add image to the layout
            image_widget = self.blob_to_image(image_data)
            if image_widget:
                # Set the size of the image widget
                image_widget.size_hint = (None, None)
                image_widget.size = (100, 100)
                box_layout.add_widget(image_widget)

                # Add the BoxLayout containing label and image to the main layout
                layout.add_widget(box_layout)

                # Add a download button with reduced size
                download_button = Button(text="Download", size_hint=(None, None), size=(100, 50))
                download_button.bind(on_press=lambda instance: self.download_image(image_data, label_text))
                layout.add_widget(download_button)

    def download_image(self, image_data, label_text):
            # Check if the image data is not empty
            if image_data:
                try:
                    # Provide a file name based on the label text
                    file_name = f"{label_text.replace(' ', '_').lower()}.png"
                    
                    # Write the image data to a file
                    with open(file_name, "wb") as file:
                        file.write(image_data)
                    
                    # Show a message indicating successful download
                    self.show_message(f"Image downloaded as {file_name}")
                except Exception as e:
                    # Show an error message if an exception occurs during file writing
                    self.show_message(f"Error downloading image: {str(e)}")
            else:
                # Show a message if the image data is empty
                self.show_message("No image data available for download")



    def on_stop(self):
        self.disconnect_from_database()

    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='Prajwal112002',
                user='your_user',
                password='your_password',
                database='your_database',
                port=3306,
                auth_plugin='mysql_native_password'
            )
            if self.db_connection.is_connected():
                print("Connected to the database")
        except Error as e:
            print("Error connecting to the database:", e)
            self.stop()
            raise Exception("Failed to connect to the database")

    def disconnect_from_database(self):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            print("Disconnected from the database")

    def get_record_from_database(self, user_uuid):
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM user_data WHERE uuid = %s"
            cursor.execute(query, (user_uuid,))
            record = cursor.fetchone()
            cursor.close()
            return record
        except Error as e:
            print("Error fetching record from database:", e)
            raise Exception("Failed to fetch record from database")
        finally:
            if 'connection' in locals() and self.db_connection.is_connected():
                cursor.close()

    def blob_to_image(self, blob):
        try:
            if blob is not None and isinstance(blob, bytes):
                img_texture = CoreImage(io.BytesIO(blob), ext="png").texture
                img = HoverableImage(texture=img_texture)
                img.bind(on_touch_down=self.enlarge_image)
                img.bind(on_touch_up=self.reset_image_size)
                return img
            else:
                return None
        except Exception as e:
            print("Error converting blob to image:", e)
            return None

    def enlarge_image(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.size_hint = (None, None)
            instance.size = (200, 200)
            return True
        return False

    def reset_image_size(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.size_hint = (None, None)
            instance.size = (100, 100)
            return True
        return False

    def show_message(self, message):
        popup = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        popup.add_widget(close_button)
        popup_window = Popup(title="Message", content=popup, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup_window.dismiss)
        popup_window.open()

if __name__ == '__main__':
    DatabaseApp().run()
