import pytest
from tests.utils import read_translation_file


@pytest.mark.asyncio
async def test_async_sanity_check():
    default_translation = read_translation_file()
    fr_translation = read_translation_file("fr")

    recursive_check(default_translation, fr_translation)


def recursive_check(default_translation, fr_translation):
    for key in default_translation.keys():
        if isinstance(default_translation[key], dict):
            recursive_check(default_translation[key], fr_translation[key])
        else:
            assert key in fr_translation.keys()
