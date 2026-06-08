from text_utils import slugify


def test_basic_slugify():
    assert slugify("Hello, World!") == "hello-world"


def test_repeated_separators():
    assert slugify("  GPU   Inference---Lab  ") == "gpu-inference-lab"


def test_empty_fallback():
    assert slugify("!!!") == "n-a"
