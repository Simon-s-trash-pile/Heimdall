from os import walk
from src.Logger import Logger
class PluginRegister():
	"""
	Plugin Register/Manager for Heimdall
	"""
	def __init__(self,DEBUG=False):
		self._DEBUG = DEBUG
		self.logger = Logger("PluginRegister",DEBUG=self._DEBUG)
		self.plugins = self.loadPlugins()

	def loadPlugins(self) -> dict:
		plugins = {}
		for pluginName in self.getPluginFiles():
			if pluginClassInstance := self.getPluginInstance(pluginName):
				plugins[pluginName] = {
					"displayName":pluginClassInstance.displayname(),
					"version":pluginClassInstance.version(),
					"accepts":pluginClassInstance.accepts(),
					"defaultInput":pluginClassInstance.defaultInput(),
					"display":pluginClassInstance.display,
					"runMethod":pluginClassInstance.run,
				}
				self.logger.infoMsg(f"{plugins[pluginName]['displayName']} v{plugins[pluginName]['version']} loaded succesfully!")
		return plugins

	def getPluginFiles(self) -> list[str]:
		for (_, _, filenames) in walk("./plugins"):
			files = [filename.replace(".py","") for filename in filenames if not filename.startswith("_")]
			break
		return files

	def getPluginInstance(self,pluginName) -> None:
		try:
			# Import the Plugin File
			pluginModule = __import__(f'plugins.{pluginName}', fromlist=[pluginName])
			# Create a Class instance of the Plugin
			pluginClass = getattr(pluginModule, pluginName)
			print(pluginClass(debug=self._DEBUG))
			return pluginClass(debug=self._DEBUG)
		except AttributeError as e:
			self.logger.errorMsg(f"{pluginName} could not be loaded! ({e})")
			return None

	def reload(self):
		"""
		It reloads the plugins
		"""
		self.logger.infoMsg("Reloading Plugins")
		self.plugins = self.loadPlugins()

	def runPlugin(self,pluginName,arg) -> list:
		self.logger.debugMsg(f"Running Plugin '{pluginName}' with Argument '{arg}'")
		return self.getPluginInstance(pluginName).run(arg)
