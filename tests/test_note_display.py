import pytest
from mock import patch

# import foolscap.note_display as note_display
from foolscap.note_display import Controller
from foolscap.note_display import ServiceRules
from foolscap.meta_data import NotesModel
from foolscap.meta_data import TagsModel

from data.mock_meta_data import FAKE_SINGLE_NOTE
from data.mock_meta_data import FAKE_SINGLE_NOTE_2
from data.mock_meta_data import FAKE_MANY_NOTES
from data.mock_meta_data import FAKE_NOTES_EDGE_CASE
from data.mock_meta_data import FAKE_DIFF_BOOKS
from data.mock_meta_data import FOUR_FAKE_NOTES
from data.mock_meta_data import FOUR_FAKE_NOTES_TAGS


"""
Setup Notes Model fixture:
"""


@pytest.fixture(scope='function')
def note_model_init(request):
    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=request.param):
        return NotesModel


@pytest.fixture(scope='function')
def note_model(request):
    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=request.param):
        model = NotesModel()
        return model


"""
Test Controller Object:
"""


@pytest.mark.parametrize("note_model_init", [(FAKE_SINGLE_NOTE)],
    indirect=True)
def test_controller__init__(note_model_init):
    with patch('foolscap.note_display.NotesModel', note_model_init):

        ctrl = Controller('notes')
        assert hasattr(ctrl, 'model')
        assert hasattr(ctrl, 'service_rules')
        assert ctrl.model.model_type == 'notes'

        ctrl = Controller('tags')
        assert hasattr(ctrl, 'model')
        assert hasattr(ctrl, 'service_rules')
        assert ctrl.model.model_type == 'tags'


@pytest.mark.parametrize("note_model, model_type, expected", [
    (FAKE_MANY_NOTES, 'tags', [
        {'title': 'fake_tag'},
    ]),
    (FAKE_MANY_NOTES, 'notes', [
        {'title': 'recently_opened'},
        {'title': 'most_viewed'},
        {'title': 'second_most'},
        {'title': 'third_most'},
        {'title': 'A'},
        {'title': 'fake_note_1'},
        {'title': 'Z'},
    ]),
    (FAKE_SINGLE_NOTE_2, 'notes', [
        {'title': 'most_viewed'}
    ]),
    (FAKE_SINGLE_NOTE, 'tags', [
        {'title': 'fake_tag'}
    ]),
    (FAKE_SINGLE_NOTE, 'notes', [
        {'title': 'most_viewed'},
    ])],
    indirect=['note_model'])
def test_ctrl_basic_out(note_model, model_type, expected):
    with patch('foolscap.note_display.display_list') as _mock:
        ctrl = Controller(model_type)
        ctrl.model = note_model
        if model_type == 'tags':
            ctrl.model = TagsModel(note_model)

        for item in expected:
            item['model'] = ctrl.model

        ctrl.service_rules = ServiceRules(ctrl.model)
        ctrl.basic_output('general')
        _mock.assert_called_with(expected)


@pytest.mark.parametrize("note_model, model_type, query, expected", [
    (FAKE_MANY_NOTES, 'tags', 'fake_tag', [
        {'title': 'fake_tag'},
    ]),
    (FAKE_MANY_NOTES, 'notes', 'fake_tag', [
        {'title': 'recently_opened'},
        {'title': 'most_viewed'},
        {'title': 'second_most'},
        {'title': 'third_most'},
        {'title': 'A'},
        {'title': 'fake_note_1'},
        {'title': 'Z'},
    ]),
    # None passed to query - should not happen. This is controlled by
    # Actor
    (FAKE_SINGLE_NOTE, 'tags', 'fake_tag', [
        {'title': 'fake_tag'}
    ]),
    (FAKE_SINGLE_NOTE, 'notes', 'fake_tag', [
        {'title': 'most_viewed'},
    ])],
    indirect=['note_model'])
def test_ctrl_query_out(note_model, model_type, query, expected):
    with patch('foolscap.note_display.display_list') as _mock:
        ctrl = Controller(model_type)
        ctrl.model = note_model
        if model_type == 'tags':
            ctrl.model = TagsModel(note_model)
        ctrl.service_rules = ServiceRules(ctrl.model)

        for item in expected:
            item['model'] = ctrl.model

        ctrl.query_output(query)
        _mock.assert_called_with(expected)


@pytest.mark.parametrize("note_model, model_type", [
    (FAKE_SINGLE_NOTE, 'tags'),
    (FAKE_SINGLE_NOTE, 'notes')
    ],
    indirect=['note_model'])
def test_ctrl_with_no_tag_matches(note_model, model_type):
    with pytest.raises(SystemExit):
        ctrl = Controller(model_type)
        ctrl.model = note_model
        if model_type == 'tags':
            ctrl.model = TagsModel(note_model)
        ctrl.service_rules = ServiceRules(ctrl.model)

        ctrl.query_output('no_matching_tag')


@pytest.mark.parametrize("note_model, model_type, query, expected", [
    (FAKE_MANY_NOTES, 'tags', 'fake', [
        {'title': 'fake_tag'}
    ]),
    (FAKE_MANY_NOTES, 'notes', 'most', [
        {'title': 'most_viewed'},
        {'title': 'third_most'},
        {'title': 'second_most'},
    ])],
    indirect=['note_model'])
def test_search_notes(note_model, model_type, query, expected):
    with patch('foolscap.note_display.display_list') as _mock:
        ctrl = Controller(model_type)
        ctrl.model = note_model
        if model_type == 'tags':
            ctrl.model = TagsModel(note_model)

        for item in expected:
            item['model'] = ctrl.model

        ctrl.service_rules = ServiceRules(ctrl.model)

        ctrl.search_output(query)
        _mock.assert_called_with(expected)


@pytest.mark.parametrize("note_model_init, model_type", [
    (FAKE_SINGLE_NOTE, 'notes'),
    (FAKE_SINGLE_NOTE, 'tags'),
    ], indirect=['note_model_init'])
def test_ctrl_search_output_with_no_results(note_model_init, model_type):
    ctrl = Controller(model_type)
    with patch('foolscap.meta_data.models.fuzzy_guess') as _fuzz,\
         pytest.raises(SystemExit):
        ctrl.search_output('none')
        assert _fuzz.called_with('none', [])


@pytest.mark.parametrize("note_model_init, model_type", [
    (FAKE_SINGLE_NOTE, 'notes'),
    (FAKE_SINGLE_NOTE, 'tags'),
    ], indirect=['note_model_init'])
def test_ctrl_search_no_query(note_model_init, model_type):
    with patch('foolscap.note_display.NotesModel', note_model_init):
        ctrl = Controller(model_type)
        with pytest.raises(SystemExit):
            ctrl.search_output(None)



"""
Test Service Rules Object
"""


@pytest.mark.parametrize("note_model",[
    (FAKE_SINGLE_NOTE),
], indirect=['note_model'])
def test_servicerules__init__(note_model):
    service = ServiceRules(note_model)
    assert hasattr(service, 'model')
    assert hasattr(service, 'ORDER_RULE')
    assert hasattr(service, 'TOP_N_VIEWED')


@pytest.mark.parametrize("note_model",[
    (FAKE_SINGLE_NOTE),
], indirect=['note_model'])
def test_servicerules_order(note_model):
    service = ServiceRules(note_model)
    with patch.object(service, 'order_notes') as _call:
        service.order(['most_viewed'])
        _call.assert_called_once()
        _call.assert_called_with(['most_viewed'])

    # Setting this effects test_models.test_notemodel__init__
    # this might be a bug with pytest?
    #
    # assert _note_model.model_type == 'notes'
    # asserts false - 'tags' != 'notes'
    #
    # note_model.model_type = 'tags'

    with patch.object(note_model, 'model_type', 'tags'):
        service = ServiceRules(note_model)
        with patch.object(service, 'by_count') as _call:
            service.order(['most_viewed'])
            _call.assert_called_once()
            _call.assert_called_with(['most_viewed'])


@pytest.mark.parametrize("note_model, notes, expected",[
    (FAKE_MANY_NOTES, FAKE_MANY_NOTES.keys(),
     ['recently_opened', 'most_viewed', 'second_most', 'third_most',
      'A', 'fake_note_1', 'Z']),

    (FOUR_FAKE_NOTES, FOUR_FAKE_NOTES.keys(),
     ['C', 'B', 'A', 'recently_opened']),

    (FAKE_NOTES_EDGE_CASE, FAKE_NOTES_EDGE_CASE.keys(),
     ['G', 'A', 'B', 'C', 'D', 'E', 'F']),

    (FAKE_SINGLE_NOTE, FAKE_SINGLE_NOTE.keys(),
     ['most_viewed']),
], indirect=['note_model'])
def test_servicerules_order_notes(note_model, notes, expected):
    service = ServiceRules(note_model)
    result = service.order_notes(notes)
    assert result == expected


@pytest.mark.parametrize("note_model, query, expected", [
    (FAKE_DIFF_BOOKS, 'work', 5),
    (FAKE_DIFF_BOOKS, 'general', 9),
], indirect=['note_model'])
def test_servicerules_filter_items(note_model, query, expected):
    service = ServiceRules(note_model)
    result = service.filter_items(FAKE_DIFF_BOOKS.keys(), query)
    assert len(result) == expected


@pytest.mark.parametrize("note_model, query", [
    (FAKE_DIFF_BOOKS, 'typo'),
], indirect=['note_model'])
def test_servicerules_filter_items_notfound(note_model, query):
    with patch('foolscap.meta_data.models.fuzzy_guess') as _fuzz,\
         pytest.raises(SystemExit):
        service = ServiceRules(note_model)
        result = service.filter_items(FAKE_DIFF_BOOKS.keys(), query)


@pytest.mark.parametrize("note_model, notes, expected",[
    (FAKE_MANY_NOTES, FAKE_MANY_NOTES.keys(),
     ['A', 'fake_note_1', 'most_viewed', 'recently_opened', 'second_most',
     'third_most', 'Z']),
], indirect=['note_model'])
def test_servicerule_alphabetise(note_model, notes, expected):
    service = ServiceRules(note_model)
    result = service.alphabetise(notes)
    assert result == expected


@pytest.mark.parametrize("note_model, notes, expected",[
    (FOUR_FAKE_NOTES, FOUR_FAKE_NOTES.keys(),
     ['C', 'B', 'A', 'recently_opened']),
], indirect=['note_model'])
def test_servicerule_most_viewed(note_model, notes, expected):
    service = ServiceRules(note_model)
    result = service.by_views(notes)
    assert result == expected


@pytest.mark.parametrize("note_model, notes, expected",[
    (FOUR_FAKE_NOTES, FOUR_FAKE_NOTES.keys(),
     'recently_opened'),
], indirect=['note_model'])
def test_servicerule_last_viewed(note_model, notes, expected):
    service = ServiceRules(note_model)
    # I am only testing the last viewed appears 1st
    # can assume the same for the rest.
    result = service.last_viewed(notes)[0]
    assert result == expected


@pytest.mark.parametrize("note_model, tags, expected",[
    (FOUR_FAKE_NOTES_TAGS, ['two', 'one', 'three'],
     ['one', 'two', 'three']),
], indirect=['note_model'])
def test_servicerule_by_count(note_model, tags, expected):
    from foolscap.meta_data import TagsModel
    tag_model = TagsModel(note_model)
    service = ServiceRules(tag_model)

    result = service.by_count(tags)
    assert result == expected


@pytest.mark.parametrize("note_model, notes, tags",[
    (FAKE_SINGLE_NOTE_2, ['most_viewed'], ['fake_tag']),
], indirect=['note_model'])
def test_servicerule_structure(note_model, notes, tags):
    service = ServiceRules(note_model)
    result = service.structure(notes)
    assert result == [
      {
        'title': 'most_viewed',
        'model': note_model,
      }
    ]

    from foolscap.meta_data import TagsModel
    tag_model = TagsModel(note_model)
    service = ServiceRules(tag_model)
    result = service.structure(tags)
    assert result == [
      {
        'title': 'fake_tag',
        'model': tag_model
      }
    ]
