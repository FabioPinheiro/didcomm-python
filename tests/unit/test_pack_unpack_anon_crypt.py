import pytest

from didcomm.common.algorithms import AnonCryptAlg
from didcomm.pack_encrypted import pack_encrypted, PackEncryptedConfig
from didcomm.unpack import unpack
from tests.test_vectors.test_vectors_anon_encrypted import (
    TEST_ENCRYPTED_DIDCOMM_MESSAGE_ANON,
)
from tests.test_vectors.test_vectors_common import TEST_MESSAGE, BOB_DID, TestVector


@pytest.mark.asyncio
async def test_unpack_encrypted_anoncrypt_xc20p(resolvers_config_bob):
    await unpack_encrypted_anoncrypt(
        TEST_ENCRYPTED_DIDCOMM_MESSAGE_ANON[0], resolvers_config_bob
    )


@pytest.mark.asyncio
async def test_unpack_encrypted_anoncrypt_a256cbc(resolvers_config_bob):
    await unpack_encrypted_anoncrypt(
        TEST_ENCRYPTED_DIDCOMM_MESSAGE_ANON[1], resolvers_config_bob
    )


@pytest.mark.asyncio
async def test_unpack_encrypted_anoncrypt_a256gcm(resolvers_config_bob):
    await unpack_encrypted_anoncrypt(
        TEST_ENCRYPTED_DIDCOMM_MESSAGE_ANON[2], resolvers_config_bob
    )


async def unpack_encrypted_anoncrypt(test_vector: TestVector, resolvers_config_bob):
    unpack_result = await unpack(
        test_vector.value, resolvers_config=resolvers_config_bob
    )
    assert unpack_result.message == TEST_MESSAGE
    assert unpack_result.metadata == test_vector.metadata


@pytest.mark.asyncio
async def test_pack_encrypted_anoncrypt_xc20p(
    resolvers_config_alice, resolvers_config_bob
):
    pack_result = await pack_encrypted(
        TEST_MESSAGE,
        to=BOB_DID,
        pack_config=PackEncryptedConfig(
            enc_alg_anon=AnonCryptAlg.XC20P_ECDH_ES_A256KW, forward=False
        ),
        resolvers_config=resolvers_config_alice,
    )

    expected_metadata = TEST_ENCRYPTED_DIDCOMM_MESSAGE_ANON[0].metadata
    assert pack_result.to_kids == expected_metadata.encrypted_to
    assert pack_result.from_kid is None
    assert pack_result.sign_from_kid is None

    unpack_result = await unpack(
        pack_result.packed_msg, resolvers_config=resolvers_config_bob
    )
    assert unpack_result.message == TEST_MESSAGE
    assert unpack_result.metadata == expected_metadata
