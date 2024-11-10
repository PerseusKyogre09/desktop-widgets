# Possible solution is to crate each QLabel individually and set its
# font size and settings individually. Enabling rich text (html) disables dragging.
# WHy? I am not that professional to know :D
# Hope this helps.

def setup_time_display(self):
    # Create separate labels for time, AM/PM, and date
    self.hour_minute_label = QLabel(self)
    self.am_pm_label = QLabel(self)
    self.date_label = QLabel(self)

    # Set font sizes individually
    self.hour_minute_label.setFont(QFont("Arial", 70))
    self.am_pm_label.setFont(QFont("Arial", 50))
    self.date_label.setFont(QFont("Arial", 30))

    # Set alignment
    self.hour_minute_label.setAlignment(Qt.AlignCenter)
    self.am_pm_label.setAlignment(Qt.AlignCenter)
    self.date_label.setAlignment(Qt.AlignCenter)

    
    layout = QVBoxLayout()
    layout.addWidget(self.hour_minute_label)
    layout.addWidget(self.am_pm_label)
    layout.addWidget(self.date_label)
    self.setLayout(layout)

def update_time(self):
    current_time = QDateTime.currentDateTime()
    hour_minute = current_time.toString("hh:mm")
    am_pm = current_time.toString("AP")
    date_text = current_time.toString("dddd, MMMM dd, yyyy")

    # Update each label with corresponding text
    self.hour_minute_label.setText(hour_minute)
    self.am_pm_label.setText(am_pm)
    self.date_label.setText(date_text)
