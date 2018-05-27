from datetime import datetime

import pytest
from mock import patch

from tests.data.mock_meta_data import FAKE_SINGLE_NOTE
from tests.data.mock_meta_data import FAKE_MANY_NOTES
from tests.data.mock_meta_data import FAKE_DIFF_BOOKS
from tests.data.mock_meta_data import FAKE_SEARCH

from foolscap.meta_data import TagsModel


# Setup NotesModel fixture
@pytest.fixture(scope='function')
def note_model(request):
    from foolscap.meta_data.models import NotesModel
    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=request.param):
        model = NotesModel()
        return model


"""
Test Notes Model:
"""


@pytest.mark.parametrize("note_model", [
    (FAKE_SINGLE_NOTE),
], indirect=['note_model'])
def test_notemodel__init__(note_model):
    assert hasattr(note_model, 'notes')
    assert hasattr(note_model, 'tags')
    assert note_model.notes == FAKE_SINGLE_NOTE
    assert note_model.tags == ['fake_tag']
    assert note_model.model_type == 'notes'
    assert len(note_model) == 1

    notes = [note for note in note_model]
    assert notes == ['most_viewed']


@pytest.mark.parametrize("note_model, query", [
    (FAKE_MANY_NOTES, 'most_viewed'),
], indirect=['note_model'])
def test_notemodel_get(note_model, query):
    result = note_model.get(query)
    assert result == {'created': datetime(2000, 12, 10, 15, 25, 19, 11262),
                      'views': 4,
                      'book': 'general',
                      'description': 'This is a fake note',
                      'modified': datetime(2000, 12, 10, 15, 25, 19, 11262),
                      'tags': ['fake_tag']}


@pytest.mark.parametrize("note_model, query", [
    (FAKE_SINGLE_NOTE, 'most'),
], indirect=['note_model'])
def test_notemodel_get_no_result(note_model, query):
    with patch('foolscap.meta_data.models.fuzzy_guess') as _fuzz:
        note_model.get(query)
        _fuzz.assert_called_with(query, FAKE_SINGLE_NOTE.keys())


@pytest.mark.parametrize("note_model, query, value, expected", [
    (FAKE_SINGLE_NOTE, 'most_viewed', 'views', 4),
    (FAKE_SINGLE_NOTE, 'most_viewed', 'gibber', None),
    (FAKE_SINGLE_NOTE, 'most_viewed', 'description', 'This is a fake note'),
], indirect=['note_model'])
def test_notemodel_get_value(note_model, query, value, expected):
    result = note_model.get_value(query, value)
    assert result == expected


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_DIFF_BOOKS, 'work', 5),
    (FAKE_DIFF_BOOKS, 'general', 9),
], indirect=['note_model'])
def test_notemodel_filter_by_value(note_model, query, expected):
    result = note_model.filter_by_value(FAKE_DIFF_BOOKS.keys(), 'book', query)
    assert len(result) == expected


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_SINGLE_NOTE, 'fake_tag', ['most_viewed']),
], indirect=['note_model'])
def test_notemodel_query_tags(note_model, query, expected):
    result = note_model.query_tags(query)
    assert result == expected


@pytest.mark.parametrize("note_model, query", [
    (FAKE_SINGLE_NOTE, 'fake'),
], indirect=['note_model'])
def test_notemodel_query_tags_no_result(note_model, query):
    with patch('foolscap.meta_data.models.fuzzy_guess') as _fuzz:
        note_model.query_tags(query)
        _fuzz.assert_called_with(query, ['fake_tag'])


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_MANY_NOTES, 'th', ['third_most']),
    (FAKE_SEARCH, 'note', [
        'note',
        '_note',
        '__note',
        '___note',
        '____note']),
], indirect=['note_model'])
def test_notemodel_query_title(note_model, query, expected):
    result = note_model.query_titles(query)
    assert result == expected


@pytest.mark.parametrize("note_model, expected", [
    (FAKE_MANY_NOTES, TypeError),
], indirect=['note_model'])
def test_notemodel_query_title_no_query(note_model, expected):
    with pytest.raises(expected):
        note_model.query_titles(None)


@pytest.mark.parametrize("note_model", [
    (FAKE_MANY_NOTES),
], indirect=['note_model'])
def test_notemodel_query_title_with_no_results(note_model):
    with patch.object(note_model, 'get') as _get:
        note_model.query_titles('none')
        _get.assert_called_with('none')


"""
Test Tags Model:
"""


@pytest.mark.parametrize("note_model", [
    (FAKE_SINGLE_NOTE),
], indirect=['note_model'])
def test_tagsmodel__init__(note_model):
    tag_model = TagsModel(note_model)

    assert hasattr(tag_model, 'tags')
    assert tag_model.tags == {'fake_tag': {
                              'sub_headings': [
                                  ('most_viewed', 'This is a fake note'),
                              ],
                              'title': 'fake_tag',
                              'description': '1'}}

    assert len(tag_model) == 1

    tags = [tag for tag in tag_model]
    assert tags == ['fake_tag']


@pytest.mark.parametrize("note_model, query", [
    (FAKE_SINGLE_NOTE, 'fake_tag'),
], indirect=['note_model'])
def test_tagsmodel_get(note_model, query):
    tag_model = TagsModel(note_model)

    result = tag_model.get(query)
    assert result == {
        'sub_headings': [
            ('most_viewed', 'This is a fake note'),
        ],
        'title': 'fake_tag',
        'description': '1'
    }


@pytest.mark.parametrize("note_model, query, value, expected", [
    (FAKE_SINGLE_NOTE, 'fake_tag', 'title', 'fake_tag'),
    (FAKE_SINGLE_NOTE, 'fake_tag', 'description', '1'),
    (FAKE_SINGLE_NOTE, 'fake_tag', 'gibber', None),
], indirect=['note_model'])
def test_tagsmodel_value(note_model, query, value, expected):
    tag_model = TagsModel(note_model)

    result = tag_model.get_value(query, value)
    assert result == expected


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_SINGLE_NOTE, 'fake', ['fake_tag']),
], indirect=['note_model'])
def test_tagsmodel_query_tags(note_model, query, expected):
    tag_model = TagsModel(note_model)

    result = tag_model.query_tags(query)
    assert result == expected


@pytest.mark.parametrize("note_model, query", [
    (FAKE_SINGLE_NOTE, 'faked'),
], indirect=['note_model'])
def test_tagsmodel_query_tags_no_result(note_model, query):
    tag_model = TagsModel(note_model)

    with patch.object(tag_model, 'get') as _get:
        tag_model.query_tags(query)
        _get.assert_called_with(query)


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_MANY_NOTES, 'fa', ['fake_tag']),
], indirect=['note_model'])
def test_tagmodel_query_title(note_model, query, expected):
    tag_model = TagsModel(note_model)

    result = tag_model.query_titles(query)
    assert result == expected


@pytest.mark.parametrize("note_model, expected", [
    (FAKE_MANY_NOTES, TypeError),
], indirect=['note_model'])
def test_tagmodel_query_title_no_query(note_model, expected):
    tag_model = TagsModel(note_model)
    with pytest.raises(expected):
        tag_model.query_titles(None)


@pytest.mark.parametrize("note_model", [
    (FAKE_MANY_NOTES),
], indirect=['note_model'])
def test_tagmodel_query_title_with_no_results(note_model):
    tag_model = TagsModel(note_model)

    with patch.object(tag_model, 'get') as _get:
        tag_model.query_titles('none')
        _get.assert_called_with('none')
