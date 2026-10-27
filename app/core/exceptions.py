"""Exceções de domínio (ou de negócio) da aplicação.
"""
class ErroDeDominio(Exception):
    """Classe base de todo erro previsto de negócio.
    
    A mensagem padrão fica na classe para que quem lança a exceção não precise repeti-la em cada `raise`, mas possa sobrescrevê-la quando houver um detalhe útil a acrescentar."""
    mensagem = "Não foi possível concluir a operação."

    def __init__(self, mensagem: str | None = None) -> None:
        self.mensagem = mensagem or type(self).mensagem
        super().__init__(self.mensagem)
class RegraDeNegocioViolada(ErroDeDominio):
    """A operação é compreensível, mas contraria uma regra do negócio."""

    mensagem = "Operação recusada por uma regra de negócio."
class ValorInvalido(RegraDeNegocioViolada):
    """Valor fora do conjunto aceito por um campo do domínio."""

    mensagem = "Valor inválido para o campo."