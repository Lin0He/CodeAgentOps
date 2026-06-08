from text_utils import slugify


def test_accents_normalized():
    assert slugify("Café déjà vu") == "cafe-deja-vu"


def test_max_length_does_not_end_with_hyphen():
    assert slugify("Deep Learning Inference Lab", max_length=14) == "deep-learning"


def test_digits_preserved():
    assert slugify("RTX 4090 + H100") == "rtx-4090-h100"
