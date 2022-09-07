from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
import pandas_datareader as pd
import matplotlib.pyplot as plt

Builder.load_file('main.kv')

crypto_dict = {'bitcoin': 'BTC-USD', 'ethereum': 'ETH-USD', 'tether': 'USDT-USD',
				'binance': 'BUSD-USD', 'cardano': 'ADA-USD', 'bnb': 'BNB-USD'}

class MyLayout(FloatLayout):

	plot_exists = False

	def plot_crypto(self):
		if self.plot_exists == True:
			self.ids.show_plot.clear_widgets()
			plt.clf()
		try:
			self.ids.error.text = ""
			crypto_name = crypto_dict[self.ids.crypto_name.text.lower()]
			start_date, end_date = self.ids.start_end.text.split(':')
			price = pd.DataReader(crypto_name, 'yahoo', start_date, end_date)
			fig, ax = plt.subplots()
			ax.plot(price.Close)
			fig.autofmt_xdate()
			canvas = FigureCanvasKivyAgg(fig, pos_hint={'x': 0.25, 'y': 0.1}, size_hint=(0.5,0.5))
			self.ids.show_plot.add_widget(canvas)
			canvas.draw()
			self.plot_exists = True

		except Exception as e:
			self.ids.error.text = type(e).__name__

	def remove(self):
		self.ids.error.text = ""
		self.ids.show_plot.clear_widgets()
		plt.clf()
		self.plot_exists = False



class MainApp(MDApp):
	def build(self):
		return MyLayout()

app = MainApp()
app.run()


