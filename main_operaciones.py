import sys
from pathlib import Path

# Configurar el path para imports
sys.path.append(str(Path(__file__).parent))

from general.operaciones.consulta_saldo import ConsultaSaldo
from general.operaciones.deposito import Deposito
from general.operaciones.retiro import Retiro
from general.operaciones.transferencia import Transferencia

def ejecutar_operacion(tipo_operacion, *args):
    try:
        if tipo_operacion == 'consulta':
            consulta = ConsultaSaldo(args[0])
            return consulta.ejecutar()
        elif tipo_operacion == 'deposito':
            deposito = Deposito(args[0], args[1])
            return deposito.ejecutar()
        elif tipo_operacion == 'retiro':
            retiro = Retiro(args[0], args[1])
            return retiro.ejecutar()
        elif tipo_operacion == 'transferencia':
            transferencia = Transferencia(args[0], args[1], args[2])
            return transferencia.ejecutar()
        else:
            raise ValueError("Operación no válida")
    except ValueError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': f"Error inesperado: {str(e)}"}

# Ejemplo de uso
if __name__ == "__main__":
    
    # Consulta de saldo
    print("\nConsulta de saldo:", ejecutar_operacion('consulta', 'CTA-BF50CC88'))
    
    # Depósito
    print("\nResultado depósito:", ejecutar_operacion('deposito', 'CTA-BF50CC88', 100))
    
    # Retiro
    print("\nResultado retiro:", ejecutar_operacion('retiro', 'CTA-BF50CC88', 100))
    
    # Transferencia
    print("\nResultado transferencia:", 
ejecutar_operacion('transferencia', 'CTA-BF50CC88', 'CTA-C7C60B2A', 100))
    
    

    #cambiar el id de cuenta a los nuevos del json
    #prueba