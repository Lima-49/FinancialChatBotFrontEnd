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

    @staticmethod
    def from_dict(data):
        return ConfigCreditCardInvoiceModel(
            invoice_id=data.get('invoice_id'),
            card_id=data.get('card_id'),
            account_id=data.get('account_id'),
            invoice_month=data.get('invoice_month'),
            invoice_year=data.get('invoice_year'),
            invoice_amount=data.get('invoice_amount'),
            is_paid=data.get('is_paid'),
        )

    @staticmethod
    def to_dict(data):
        return {
            "ID_FATURA_CARTAO_CREDITO": data.invoice_id,
            "ID_CARTAO": data.card_id,
            "ID_BANCO": data.account_id,
            "MES_FATURA": data.invoice_month,
            "ANO_FATURA": data.invoice_year,
            "VALOR_FATURA": data.invoice_amount,
            "PAGA": data.is_paid,
        }
