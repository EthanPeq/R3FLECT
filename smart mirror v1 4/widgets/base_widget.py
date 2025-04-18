class BaseWidget:
    def __init__(self, root):
        self.root = root
        self.frame = None  # Each widget will have its own frame

    def create_widget(self):
        """Create the widget UI"""
        raise NotImplementedError("Each widget must implement the 'create_widget' method.")

    def update_widget(self, data):
        """Update the widget UI with new data"""
        raise NotImplementedError("Each widget must implement the 'update_widget' method.")

    def remove_widget(self):
        """Remove the widget from the UI"""
        if self.frame:
            self.frame.destroy()
