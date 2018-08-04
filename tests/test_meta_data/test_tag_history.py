import pytest
from mock import patch

from foolscap.meta_data.tag_history import (
    TagsHistory,
    diff_tags,
    record_tags,
    format_new_history
)


@pytest.fixture(scope='function')
def history_object():
    """Provide a history object.
    """
    patch_load = 'foolscap.meta_data.tag_history.load_tag_history'
    with patch(patch_load) as mock_load:
        mock_load.return_value = ['tag line 1', 'tag line 2']
        return TagsHistory()


def test_TagsHistory_init(history_object):
    assert len(history_object) == 2
    assert history_object == ['tag line 1', 'tag line 2']


def test_TagsHistory_deprecate_less_than(history_object):
    with patch('foolscap.meta_data.tag_history.TAG_HISTORY', 1):
        history_object.check_deprecation(0)
        assert history_object.deprecate_lines == 1


def test_TagsHistory_deprecate_greater_than(history_object):
    with patch('foolscap.meta_data.tag_history.TAG_HISTORY', 1):
        history_object.check_deprecation(2)
        assert history_object.deprecate_lines == 3


def test_TagsHistory_save(history_object):
    patch_save = 'foolscap.meta_data.tag_history.save_tag_history'
    with patch(patch_save) as mock_save:
        history_object.check_deprecation(0)
        history_object.save()

        mock_save.assert_called_with(['tag line 1', 'tag line 2'], 0)


@pytest.mark.parametrize("diff_input, record_input",
    [
        (
            (
                ['new_tag', 'new_tag_2'],
                ['old_tag'],
                'note',
            ),
            (
                'note',
                {'old_tag'},
                {'new_tag', 'new_tag_2'},
            )
        ),
        (
            (
                ['old_tag'],
                ['old_tag'],
                'note',
            ),
            (
                'note',
                set(),
                set(),
            )
        )
    ]
)
def test_diff_tags(diff_input, record_input):
    with patch('foolscap.meta_data.tag_history.record_tags') as mock_record:
        diff_tags(*diff_input)
    mock_record.assert_called_with(*record_input)


def test_record_tags(history_object):
    patch_save = 'foolscap.meta_data.tag_history.save_tag_history'
    with patch(patch_save),\
         patch('foolscap.meta_data.tag_history.TagsHistory') as mock_history,\
         patch('foolscap.meta_data.tag_history.format_new_history') as style:

        style.return_value = ['new line']
        mock_history.return_value = history_object
        record_tags('note', {'deleted_tag'}, {'added_tag'})

        expected = [
            'tag line 1',
            'tag line 2',
            'new line',
            'new line',
        ]

        assert history_object.deprecate_lines == 0
        assert history_object == expected


def test_format_new_history():
    from datetime import date
    mock_style = "{{{tag}}} {note} {date}"
    note = 'note'
    tags = ['new', 'tags']

    with patch('foolscap.meta_data.tag_history.date') as time:
        time.today.return_value = date(2017, 2, 2)

        expected = [
            "{new} note 2017-02-02",
            "{tags} note 2017-02-02",
        ]

        result = format_new_history(mock_style, note, tags)
        assert result == expected

