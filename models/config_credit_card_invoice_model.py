class ConfigCreditCardInvoiceModel:
    def __init__(self, invoice_id=None, card_id=None, account_id=None, 
                 invoice_month=None, invoice_year=None, invoice_amount=None, is_paid=None):
        self.invoice_id = invoice_id
        self.card_id = card_id
        self.account_id = account_id
        self.invoice_month = invoice_month
        self.invoice_year = invoice_year
        self.invoice_amount = invoice_amount
        self.is_paid = is_paid

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.
        Funciona com colunas em maiúsculo (SQLite) ou minúsculo (PostgreSQL)."""
        return cls(
            invoice_id=data.get('id_fatura_cartao_credito') or data.get('ID_FATURA_CARTAO_CREDITO'),
            card_id=data.get('id_cartao') or data.get('ID_CARTAO'),
            account_id=data.get('id_banco') or data.get('ID_BANCO'),
            invoice_month=data.get('mes_fatura') or data.get('MES_FATURA'),
            invoice_year=data.get('ano_fatura') or data.get('ANO_FATURA'),
            invoice_amount=data.get('valor_fatura') or data.get('VALOR_FATURA'),
            is_paid=data.get('paga') or data.get('PAGA'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_fatura_cartao_credito": self.invoice_id,
            "id_cartao": self.card_id,
            "id_banco": self.account_id,
            "mes_fatura": self.invoice_month,
            "ano_fatura": self.invoice_year,
            "valor_fatura": self.invoice_amount,
            "paga": self.is_paid,
        }