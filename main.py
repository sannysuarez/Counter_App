from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Fbo, Rectangle, Color
from datetime import datetime
from PIL import Image, ImageDraw
import os


class CounterApp(App):
    def __init__(self, **kwargs):
        super(CounterApp, self).__init__(**kwargs)
        self.icon = "Rsmall.png"
        self.text_input = None
        self.counter = 0
        self.total = 0

    def build(self):
        MainLayout = BoxLayout(orientation="vertical")

        self.result = TextInput(background_color="black", foreground_color="white",
                                size_hint_y=None, height=200, readonly=True)
        MainLayout.add_widget(self.result)

        self.total = TextInput(text=str(self.total), readonly=True, halign="center", background_color="black",
                                    foreground_color="white", size_hint_y=None, height=30, font_size=15)
        MainLayout.add_widget(self.total)

        self.live_count = TextInput(text=str(self.counter), readonly=True, halign="center", background_color="black",
                                    foreground_color="white", size_hint_y=None, height=40, font_size=20)
        MainLayout.add_widget(self.live_count)

        count_btn = Button(text="Count", font_size=30, background_color="grey")
        count_btn.bind(on_press=self.count)

        MainLayout.add_widget(count_btn)

        buttons = [
            ["Add", "Reset", "Save", "Done"]
        ]
        colors = ["grey", "red", "blue", "green"]
        for i, rows in enumerate(buttons):
            b_layout = BoxLayout()
            for j, each in enumerate(rows):
                btn = Button(text=each, background_color=colors[j], font_size=18, size_hint_y=None, height=60)
                btn.bind(on_press=self.all_buttons)

                b_layout.add_widget(btn)
            MainLayout.add_widget(b_layout)

        return MainLayout

    def count(self, instance):
        self.counter += 1
        self.live_count.text = self.text_input.text + '\t' + str(self.counter)

    def all_buttons(self, instance):
        button = instance.text

        if button == "Done":
            if self.counter == 0:
                Error_popup = Popup(title='Error!',  content=Label(text='zero count.'),
                                    size_hint=(None, None), size=(200, 100))
                return Error_popup.open()
            self.total.text = str(int(self.total.text) + self.counter)
            self.result.text = '\n' + self.result.text + '\n' + self.live_count.text
            self.counter = 0
            self.live_count.text = str(self.counter)

            popup_content = BoxLayout(orientation='vertical')
            self.text_input = TextInput(hint_text='Name again...', multiline=False)
            popup_content.add_widget(self.text_input)
            add_popup = Popup(title='Successfully added', content=popup_content, size_hint=(None, None), size=(200, 100))
            add_popup.open()

        if button == "Add":
            popup_content = BoxLayout(orientation='vertical')
            self.text_input = TextInput(hint_text='stacker..', multiline=False)
            popup_content.add_widget(self.text_input)
            add_popup = Popup(title='Name:', content=popup_content, size_hint=(None, None), size=(200, 100))
            add_popup.open()

        if button == "Reset":
            self.live_count.text = ''
            self.counter = 0
            self.live_count.text = str(self.counter)

        if button == "Save":
            # Get the layout instance
            layout = self.result

            # Generate a temporary filename
            temp_filename = "temp_export.png"

            # Capture the content of the widget as an image
            layout.export_to_png(temp_filename)

            # Open the captured image using Pillow
            image = Image.open(temp_filename)

            # Get the current date and time
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            current_time = datetime.now().strftime("%I:%M:%S %p")

            # Use ImageDraw to draw text on the image
            draw = ImageDraw.Draw(image)
            draw.text((5, 5), f"Date Stamp : {current_date}", fill=(255, 255, 255))
            draw.text((5, 20), f"Time Stamp : {current_time}", fill=(255, 255, 255))

            # Adjust y-coordinate for spacing
            y_coordinate = 35

            # Draw a line as a separator
            draw.line([(10, y_coordinate), (image.width - 10, y_coordinate)], fill=(255, 255, 255), width=2)

            # Get the captured content from self.result.text
            captured_content = layout.text

            # Draw the captured content below the line
            draw.text((10, y_coordinate + 10), f"Total Counts = {self.total.text}", fill=(255, 255, 255))

            # Get the user data directory
            user_data_dir = self.user_data_dir

            # Create a "results" directory within the user data directory
            results_dir = os.path.join(user_data_dir, 'results')
            os.makedirs(results_dir, exist_ok=True)

            # Generate a dynamic filename based on the current date and time
            filename_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_filename = os.path.join(results_dir, f'result_{filename_suffix}.jpg')

            # Convert the image to RGB (if it's not already in that format)
            image = image.convert('RGB')

            # Save the image with the dynamic filename
            image.save(image_filename, 'JPEG')

            # Remove the temporary file
            os.remove(temp_filename)


if __name__ == '__main__':
    app = CounterApp()
    app.run()








