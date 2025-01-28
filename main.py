import os
from pytube import YouTube
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView

class YouTubeDownloaderApp(App):

    def build(self):
        self.title = "YouTube Downloader"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input field for the YouTube video URL
        self.url_input = TextInput(hint_text="Enter YouTube URL", size_hint=(1, None), height=40)
        self.root.add_widget(self.url_input)

        # File chooser to select the download location
        self.file_chooser = FileChooserIconView(size_hint=(1, 0.4))
        self.root.add_widget(self.file_chooser)

        # Spinner for video quality options
        self.quality_spinner = Spinner(
            text="Select Quality",
            values=("720p", "1080p", "144p", "360p"),
            size_hint=(1, None),
            height=40
        )
        self.root.add_widget(self.quality_spinner)

        # Download button
        self.download_button = Button(text="Download", size_hint=(1, None), height=50)
        self.download_button.bind(on_press=self.download_video)
        self.root.add_widget(self.download_button)

        # Status label
        self.status_label = Label(text="Enter a URL and select the quality", size_hint=(1, None), height=40)
        self.root.add_widget(self.status_label)

        return self.root

    def download_video(self, instance):
        url = self.url_input.text
        download_folder = self.file_chooser.selection[0] if self.file_chooser.selection else os.getcwd()
        quality = self.quality_spinner.text

        if not url:
            self.status_label.text = "Please enter a valid YouTube URL."
            return

        try:
            yt = YouTube(url)
            stream = None

            # Choose the stream based on the selected quality
            for s in yt.streams.filter(progressive=True, file_extension="mp4"):
                if quality == "720p" and s.resolution == "720p":
                    stream = s
                    break
                elif quality == "1080p" and s.resolution == "1080p":
                    stream = s
                    break
                elif quality == "360p" and s.resolution == "360p":
                    stream = s
                    break
                elif quality == "144p" and s.resolution == "144p":
                    stream = s
                    break

            if stream:
                self.status_label.text = f"Downloading {yt.title} in {quality}..."
                stream.download(download_folder)
                self.status_label.text = f"Download completed: {yt.title}"
            else:
                self.status_label.text = f"Quality {quality} not available for this video."

        except Exception as e:
            self.status_label.text = f"An error occurred: {str(e)}"


# Run the application
if __name__ == '__main__':
    YouTubeDownloaderApp().run()
