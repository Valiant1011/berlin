import time , sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler

# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)

# This class handles the main window of server
class server_window(QMainWindow):
	def __init__(self, data_changed_flags, task_queue):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('B.E.R.L.I.N.')
		self.setFixedSize(400, 600)
		self.setGeometry(700, 200, 400, 600) 
		# make data_changed_flag accessible from the class methods
		self.data_changed_flags = data_changed_flags
		self.task_queue = task_queue
		self.number_of_chars_per_row = 25
		self.reply_dict = self.basic_dict()
		server_window.init_UI(self)
		return

	def init_UI(self):
		try:
			self.welcome_label = QLabel('Hi! I\'m BERLIN.')
			self.welcome_label.setObjectName('ai_response')
			self.welcome_label.setFixedSize(120, 30)
			
			self.chat_widget = QWidget()
			self.chat_scroll_area = QScrollArea(self)
			self.chat_scroll_area.setMinimumSize(380, 520)
			self.chat_scroll_area.setWidgetResizable(True)
			self.chat_scroll_area.setWidget(self.chat_widget)
			self.scrollbar = self.chat_scroll_area.verticalScrollBar()
			self.scrollbar.rangeChanged.connect(self.move_scrollbar_to_bottom)

			self.chat_layout = QVBoxLayout(self.chat_widget)
			self.chat_layout.setAlignment(Qt.AlignBottom)
			self.chat_layout.addWidget(self.welcome_label)
			self.chat_layout.setAlignment(self.welcome_label, Qt.AlignLeft)

			self.reply_box = QLineEdit()
			self.reply_box.setPlaceholderText('What\'s on your mind?')
			self.reply_box.returnPressed.connect(self.user_input_handler)
			self.reply_box.setFixedSize(280, 30)

			self.reply_button = QPushButton('Reply')
			self.reply_button.setObjectName('interior_button')
			self.reply_button.setFixedSize(75, 28)
			self.reply_button.clicked.connect(self.user_input_handler)
			self.reply_button.setDefault(True)

			self.bottom_layout = QHBoxLayout()
			self.bottom_layout.addWidget(self.reply_box)
			self.bottom_layout.addSpacing(5)
			self.bottom_layout.addWidget(self.reply_button)

			self.bottom_widget = QWidget()
			self.bottom_widget.setLayout(self.bottom_layout)
			
			self.top_layout = QVBoxLayout()
			self.top_layout.addStretch(1)
			self.top_layout.addWidget(self.chat_scroll_area)
			self.top_layout.addStretch(90)
			self.top_layout.addWidget(self.bottom_widget)

			self.top_widget = QWidget()
			self.top_widget.setLayout(self.top_layout)
			self.top_widget.setObjectName("main_widget")

			# Set top_widget as our central widget
			self.setCentralWidget(self.top_widget)
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[ ERROR ] : ' , exc_type, fname, exc_tb.tb_lineno)
		return

	def move_scrollbar_to_bottom(self, min, max):
		self.chat_scroll_area.verticalScrollBar().setValue(max)
		return

	@pyqtSlot()
	def user_input_handler(self):
		user_input = self.reply_box.text()
		if user_input == '':
			return
		self.reply_box.setText('')
		user_input = self.process_text(user_input)
		print('[ USER ] : ' + user_input)
		width, height = self.get_button_dimensions(user_input)
		user_input_label = QLabel(user_input)
		user_input_label.setObjectName('user_input')
		user_input_label.setFixedSize(width, height)
		user_input_label.setContentsMargins(5, 5, 5, 5)
		self.chat_layout.addWidget(user_input_label)
		self.chat_layout.setAlignment(user_input_label, Qt.AlignRight)
		self.chat_layout.addSpacing(10)
		
		reply = self.get_reply(user_input)
		reply = self.process_text(reply)
		print('[ BERLIN ] : ' + reply)
		width, height = self.get_button_dimensions(reply)
		reply_label = QLabel(reply)
		reply_label.setObjectName('ai_response')
		reply_label.setFixedSize(width, height)
		reply_label.setContentsMargins(5, 5, 5, 5)
		self.chat_layout.addWidget(reply_label)
		self.chat_layout.setAlignment(reply_label, Qt.AlignLeft)
		self.chat_layout.addSpacing(10)
		
	def process_text(self, text):
		# Add \n every number_of_chars_per_row characters
		char_count = 0
		correction_value = 1
		text_length = len(text)
		for i in range(0, text_length):
			if text[i] == '\n':
				char_count = 0
			else:
				char_count += 1
				if (
						char_count % (
							self.number_of_chars_per_row + 
							correction_value
						) == 0 
						and 
						i != text_length - 1
					):
					char_count = 0 
					first_part = text[0: i]
					second_part = text[i :]
					text = first_part + '\n-' + second_part
		return text

	def get_button_dimensions(self, text):
		text_length = len(text)
		number_of_rows = 1 + int(text_length / self.number_of_chars_per_row)
		height = number_of_rows * 30
		width = max(min(self.number_of_chars_per_row, len(text) ) * 10, 65)
		return width, height

	def get_reply(self, text):
		backup = text
		text = text.lower()
		try:
			reply = self.reply_dict[text]
		except:
			reply = "What do you mean by " + backup

		return reply

	def basic_dict(self):
		basic_replies = {
			"hi" : "Hello!",
			"hello" : "Hey there!",
			"bye" : "See ya!",
			"how are you" : "I'm fine, thanks!",
			"wassup" : "Nothing much, you say?"
		}
		return basic_replies

	def bella_ciao():
		str = (
			# Una mattina mi sono svegliato,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# Una mattina mi sono svegliato,
			# e ho trovato l'invasor.

			# O partigiano, portami via,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# O partigiano, portami via,
			# ché mi sento di morir.

			# E se io muoio da partigiano,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# E se io muoio da partigiano,
			# tu mi devi seppellir.

			# E seppellire lassù in montagna,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# E seppellire lassù in montagna,
			# sotto l'ombra di un bel fior.

			# Tutte le genti che passeranno,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# Tutte le genti che passeranno,
			# Mi diranno «Che bel fior!»
			# «È questo il fiore del partigiano»,
			# o bella, ciao! bella, ciao! bella, ciao, ciao, ciao!
			# «È questo il fiore del partigiano, morto per la libertà!»

		)

	def closeEvent(self, event):
		event.accept()
		
class init_gui(server_window):
	def __init__(self, data_changed_flags, task_queue):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		server_app = server_window(data_changed_flags, task_queue)
		server_app.show()
		server_app.reply_box.setFocus()
		# Execute the app mainloop
		app.exec_()
		return