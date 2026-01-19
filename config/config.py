"""
Configuração global da aplicação
"""
import sys

# Verificar se foi passado o argumento --teste
_is_test_mode = "--teste" in sys.argv

def is_test_mode() -> bool:
    """Retorna True se está em modo de teste"""
    return _is_test_mode

def get_table_name(base_name: str) -> str:
    """
    Retorna o nome da tabela com sufixo _TESTE se em modo de teste
    
    Args:
        base_name: Nome base da tabela (ex: "BANCOS")
        
    Returns:
        Nome da tabela com sufixo se em teste (ex: "BANCOS_TESTE")
    """
    if is_test_mode():
        return f"{base_name}_TESTE"
    return base_name
