def start_transaction(self, sort, address, price=None, data=None, caller=None, value=0, gas=2300):
        """
        Initiate a transaction
        :param sort: the type of transaction. CREATE or CALL or DELEGATECALL
        :param address: the address of the account which owns the code that is executing.
        :param price: the price of gas in the transaction that originated this execution.
        :param data: the byte array that is the input data to this execution
        :param caller: the address of the account which caused the code to be executing. A 160-bit code used for identifying Accounts
        :param value: the value, in Wei, passed to this account as part of the same procedure as execution. One Ether is defined as being 10**18 Wei.
        :param bytecode: the byte array that is the machine code to be executed.
        :param gas: gas budget for this transaction.
        """
        assert self._pending_transaction is None, "Already started tx"
        self._pending_transaction = PendingTransaction(sort, address, price, data, caller, value, gas)