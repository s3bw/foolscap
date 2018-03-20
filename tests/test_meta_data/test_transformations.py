from mock import patch

from foolscap.meta_data.transformations import load_tags


def test_load_tags():
    patch_meta = 'foolscap.meta_data.transformations.load_meta'
    mock_meta = {'Title_1': {'tags': ['yes', 'no']},
                 'Title_2': {'tags': ['maybe', 'pass']}}
    with patch(patch_meta, return_value=mock_meta):
        result = load_tags()
        assert result == set(['yes', 'no', 'maybe', 'pass'])
