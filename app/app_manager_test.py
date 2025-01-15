from app.app_manager import AppManager

config_file = "/Users/cole/PycharmProjects/ObjectDectectApp/assets/configs/app_manager.yaml"
app_manager = AppManager()
app_manager.initialize(config_file)
app_manager.run()
# # # #
# # # #
try:
    app_manager.display_stream()
except KeyboardInterrupt:
    print("Stream interrupted.")

