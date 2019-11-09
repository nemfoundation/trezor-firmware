from trezor.messages.NEM2MosaicDefinitionTransaction import NEM2MosaicDefinitionTransaction
from trezor.messages.NEM2TransactionCommon import NEM2TransactionCommon

from ..helpers import (
    NEM2_TRANSACTION_TYPE_MOSAIC_DEFINITION,
)
from ..writers import (
    serialize_tx_common,
    get_common_message_size,    
    write_uint32_le,
    write_uint64_le,
    write_uint8
)


def serialize_mosaic_definition(
    common: NEM2TransactionCommon, creation: NEM2MosaicDefinitionTransaction, public_key: bytes
):
    tx = bytearray()

    size = get_common_message_size()
    # add up the mosaic-definition specific message attribute sizes
    size += 4 # nonce is 4 bytes
    size += 8 # mosaic id is 8 bytes
    size += 1 # flags is 1 byte
    size += 1 # divisibility is 1 byte
    size += 8 # duration is 8 bytes

    write_uint32_le(tx, size)

    tx = serialize_tx_common(tx, common)

    write_uint32_le(tx, creation.nonce)
    write_uint64_le(tx, creation.mosaic_id)
    write_uint8(tx, creation.flags)
    write_uint8(tx, creation.divisibility)
    write_uint64_le(tx, creation.duration)

    return tx
