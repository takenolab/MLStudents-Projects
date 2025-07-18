from kivy.app import App
from kivy.uix.filechooser import FileChooser

class FileChooserApp(App):
    def build(self):
        chooser = FileChooser()
        chooser.bind(on_success=self.on_file_selected)
        # return chooser

    def on_file_selected(self, instance, path, filename):
        print(f"Selected file: {path}/{filename}")

if __name__ == '__main__':
    FileChooserApp().run()