from trezor.messages.NEM2TransactionCommon import NEM2TransactionCommon

from apps.common.writers import (
    write_bytes,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
    write_uint8
)

# https://github.com/nemtech/nem2-sdk-typescript-javascript/blob/master/src/infrastructure/catbuffer/TransactionBuilder.ts#L167
def serialize_tx_common(
    w: bytearray,
    common: NEM2TransactionCommon
) -> bytearray:
    # we don't write the size in here as it changes depending on the transaction type
    # by the time this runs, we assume that size has already been written to the provided bytearray

    # the first 100 bytes of space would usually be occupied by size, signature and signer public key
    # we dont need/want these fields for signing transactions through trezor
    # pad them out so the payload is still the correct size
    # https://nemtech.github.io/concepts/transaction.html#signing-a-transaction

    # pad out signature (64 bytes)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)

    # pad out signer public key (32 bytes)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)
    write_uint64_le(w, 0)

    # version
    write_uint16_le(w, common.version)

    # type
    write_uint16_le(w, common.type)

    # fee
    write_uint64_le(w, int(common.max_fee))

    # deadline
    write_uint64_le(w, int(common.deadline))

    return w

def get_common_message_size():

    # calculate the size of the common message (in bytes)
    size = 0
    size += 4 # message size
    size += 64 # signature (catbuffer Signature)
    size += 32 # signer public key (catbuffer Key)
    size += 2 # version
    size += 2 # type
    size += 8 # amount (catbuffer Amount)
    size += 8 # deadline (catbuffer Timestamp)
    return size