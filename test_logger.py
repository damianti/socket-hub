#!/usr/bin/env python3
"""
Test simple para verificar que el logger funciona.
"""

from shared.logging import SocketHubLogger

def test_logger():
    """Prueba básica del logger."""
    print("🧪 Probando el logger...")
    
    # Crear logger para test
    logger = SocketHubLogger("test-service").get_logger()
    
    # Probar diferentes niveles
    logger.debug("Este es un mensaje DEBUG")
    logger.info("Este es un mensaje INFO")
    logger.warning("Este es un mensaje WARNING")
    logger.error("Este es un mensaje ERROR")
    logger.critical("Este es un mensaje CRITICAL")
    
    print("✅ Test completado. Revisa:")
    print("   - Consola: deberías ver los logs aquí")
    print("   - Archivo: logs/test-service.log")

if __name__ == "__main__":
    test_logger()
