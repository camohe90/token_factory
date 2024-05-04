from algopy import ARC4Contract, Global, String, Txn, UInt64, arc4, gtxn, itxn


class TokenFactory(ARC4Contract):
    unitary_price: UInt64
    asset_id: UInt64

    @arc4.abimethod()
    def create_asset(self, asset_name:String, unit_name:String) ->None:
        self.asset_created = itxn.AssetConfig (
            asset_name= asset_name,
            unit_name= unit_name,
            total= 10_000,
            decimals= 1,
            default_frozen=False
        ).submit().created_asset.id


    @arc4.abimethod()
    def set_price(self, unitary_price:UInt64)->None:
        assert Txn.sender == Global.creator_address
        self.unitary_price = unitary_price

    @arc4.abimethod()
    def sell_asset(self, buyer_txn: gtxn.PaymentTransaction, quantity: UInt64) ->None:
        assert buyer_txn.sender == Txn.sender
        assert buyer_txn.receiver == Global.current_application_address
        assert buyer_txn.amount == self.unitary_price * quantity

        itxn.AssetTransfer(
            xfer_asset=self.asset_created,
            asset_receiver= Txn.sender,
            asset_amount=quantity
        ).submit()


    @arc4.abimethod
    def get_asset_id(self)-> UInt64:
        return self.asset_created



