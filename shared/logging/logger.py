import logging
import logging.handlers
import yaml
import os


class SocketHubLogger:
    def __init__(self, service_name: str, config_path: str = None) -> None:
        """
        Constructor del logger.
        service_name: nombre del servicio (ej: "auth-service")
        config_path: ruta al archivo de configuración
        """
        self.service_name = service_name
        self.config_path = config_path or "shared/logging/config.yaml"
        self.logger = None  # Se creará cuando se necesite
        
        # Configurar el logger
        self._setup_logger()


    def get_logger(self) -> logging.Logger:
        """
        Retorna el logger configurado.
        """
        return self.logger


    def _load_config(self, config_path: str) -> dict:
        """
        Carga la configuración desde el archivo YAML.
        Si el archivo no existe, retorna configuración por defecto.
        """
        # Verificar si el archivo existe
        if not os.path.exists(config_path):
            # Configuración por defecto si no existe el archivo
            return {
                'logging': {
                    'level': 'INFO',
                    'handlers': {
                        'file': {
                            'enabled': True,
                            'path': 'logs',
                            'max_bytes': 10485760,  # 10MB
                            'backup_count': 7
                        },
                        'console': {
                            'enabled': True,
                            'level': 'INFO'
                        }
                    },
                    'format': {
                        'console': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    }
                }
            }
        
        # Leer archivo YAML
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        return config

    def _setup_handlers(self, config: dict, service_name: str) -> list:
        """
        Crea los handlers (dónde se escriben los logs).
        Retorna una lista de handlers configurados.
        """
        handlers = []
        
        # Crear carpeta de logs si no existe
        log_path = config['logging']['handlers']['file']['path']
        os.makedirs(log_path, exist_ok=True)
        
        # Handler para archivo (si está habilitado)
        if config['logging']['handlers']['file']['enabled']:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=os.path.join(log_path, f"{service_name}.log"),
                maxBytes=config['logging']['handlers']['file']['max_bytes'],
                backupCount=config['logging']['handlers']['file']['backup_count']
            )
            file_handler.setLevel(logging.INFO)
            handlers.append(file_handler)
        
        # Handler para consola (si está habilitado)
        if config['logging']['handlers']['console']['enabled']:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            handlers.append(console_handler)
        
        return handlers 
    def _setup_formatters(self, config: dict) -> dict:
        """
        Crea los formatters (formatos) para los logs.
        Retorna un diccionario con formatters para consola y archivo.
        """
        # Formatter para consola (más legible)
        console_formatter = logging.Formatter(
            config['logging']['format']['console']
        )
        
        # Formatter para archivo (mismo formato que consola por ahora)
        file_formatter = logging.Formatter(
            config['logging']['format']['file']
        )
        
        return {
            'console': console_formatter,
            'file': file_formatter
        }
    
    def _setup_logger(self) -> None:
        """
        Configura el logger completo: carga config, crea handlers y formatters.
        """
        # Cargar configuración
        config = self._load_config(self.config_path)
        
        # Crear el logger
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(getattr(logging, config['logging']['level']))
        
        # Limpiar handlers existentes (evitar duplicados)
        self.logger.handlers.clear()
        
        # Crear handlers
        handlers = self._setup_handlers(config, self.service_name)
        
        # Crear formatters
        formatters = self._setup_formatters(config)
        
        # Aplicar formatters a handlers
        for handler in handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                # Es un console handler
                handler.setFormatter(formatters['console'])
            else:
                # Es un file handler
                handler.setFormatter(formatters['file'])
            
            # Agregar handler al logger
            self.logger.addHandler(handler)
