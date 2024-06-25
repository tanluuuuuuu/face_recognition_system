def main():
    import os
    import warnings
    warnings.filterwarnings("ignore")
    from server import AIServer
    from utils import open_file_cfg

    config_path = 'config/cfg.yaml'
    
    class App():
        def __init__(self,config_path) -> None:
            self.config_path = config_path
            self.server = AIServer(self.get_cfg())
            self.server.serve()

        def get_cfg(self) -> str:
            return open_file_cfg(self.config_path)
        
    App(config_path)

if __name__ == "__main__":
    main()