import algokit_utils
import pytest
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    PayParams,
)
from algosdk.atomic_transaction_composer import TransactionWithSigner

from smart_contracts.artifacts.token_factory.client import TokenFactoryClient


@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Genera un cliente de Algorand para interactuar con la app"""
    return AlgorandClient.default_local_net()


@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> AddressAndSigner:
    return algorand.account.dispenser()


@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    acct = algorand.account.random()

    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


@pytest.fixture(scope="session")
def test_asset_id(algorand: AlgorandClient, creator: AddressAndSigner) -> int:
    sent_txn = algorand.send.asset_create(
        AssetCreateParams(sender=creator.address, total=10)
    )
    return sent_txn["confirmation"]["asset-index"]


@pytest.fixture(scope="session")
def token_factory_client(
    algorand: AlgorandClient, creator: AddressAndSigner
) -> TokenFactoryClient:
    client = TokenFactoryClient(
        algod_client=algorand.client.algod,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    return client


def test_set_price(token_factory_client: TokenFactoryClient):
    result = token_factory_client.set_price(unitary_price=300_000)
    assert result.confirmed_round



def test_create_asset(
        token_factory_client: TokenFactoryClient,
        creator: AddressAndSigner,
        algorand: AlgorandClient
        ):

        algorand.send.payment(
            PayParams(
                    sender = creator.address,
                    receiver= token_factory_client.app_address,
                    amount=2_000_000,
                )
        )

        assert(
            algorand.account.get_information(token_factory_client.app_address)["amount"] == 2_000_000
        )

        sp = algorand.client.algod.suggested_params()
        sp.fee = 2000

        result = token_factory_client.create_asset(
            asset_name="New Coin",
            unit_name="NEW",
            transaction_parameters=algokit_utils.TransactionParameters(
                sender=creator.address,
                signer=creator.signer,
                suggested_params=sp
            ),
        )

        assert result.confirmed_round

        asset_id = token_factory_client.get_asset_id().return_value
        result = algorand.account.get_information(token_factory_client.app_address)

        assert result["assets"][0]["amount"] == 10000
        assert asset_id ==  result["assets"][0]["asset-id"]


def test_transfer_asset(
        token_factory_client: TokenFactoryClient,
        creator: AddressAndSigner,
        algorand: AlgorandClient
        ):

        algorand.send.asset_opt_in(
            AssetOptInParams(
                sender=creator.address,
                asset_id= token_factory_client.get_asset_id().return_value
            )
        )

        assert algorand.account.get_information(creator.address)["total-assets-opted-in"] == 1
        asset_id = token_factory_client.get_asset_id().return_value

        buyer_txn = algorand.transactions.payment(
        PayParams(
            sender=creator.address,
            receiver=token_factory_client.app_address,
            amount=3 * 300_000,
            extra_fee=1000,
            )
        )

        result = token_factory_client.sell_asset(
            quantity=3,
            buyer_txn = TransactionWithSigner(txn=buyer_txn, signer=creator.signer),
            transaction_parameters=algokit_utils.TransactionParameters(
            foreign_assets=[asset_id],
            sender=creator.address,
            signer=creator.signer,
            )
         )

        assert result.confirmed_round

        result = algorand.account.get_information(creator.address)
        assert result["assets"][0]["amount"] == 3
