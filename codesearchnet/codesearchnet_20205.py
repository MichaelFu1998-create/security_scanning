def barcode(iban, reference, amount, due=None):
    """Calculates virtual barcode for IBAN account number and ISO reference

    Arguments:
        iban {string} -- IBAN formed account number
        reference {string} -- ISO 11649 creditor reference
        amount {decimal.Decimal} -- Amount in euros, 0.01 - 999999.99
        due {datetime.date} -- due date
    """

    iban = iban.replace(' ', '')
    reference = reference.replace(' ', '')

    if reference.startswith('RF'):
        version = 5
    else:
        version = 4

    if version == 5:
        reference = reference[2:]  # test RF and add 00 where needed
        if len(reference) < 23:
            reference = reference[:2] + ("0" * (23 - len(reference))) + reference[2:]
    elif version == 4:
        reference = reference.zfill(20)

    if not iban.startswith('FI'):
        raise BarcodeException('Barcodes can be printed only for IBANs starting with FI')

    iban = iban[2:]
    amount = "%08d" % (amount.quantize(Decimal('.01')).shift(2).to_integral_value())
    if len(amount) != 8:
        raise BarcodeException("Barcode payment amount must be less than 1000000.00")

    if due:
        due = due.strftime("%y%m%d")
    else:
        due = "000000"

    if version == 4:
        barcode = "%s%s%s000%s%s" % (version, iban, amount, reference, due)
    elif version == 5:
        barcode = "%s%s%s%s%s" % (version, iban, amount, reference, due)

    return barcode