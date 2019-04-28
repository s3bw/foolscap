from fool.bars import TabBar
from fool.tables import TableItem
from fool.tables import ColumnRegistry
from fool.windows import TableWindow

column_registry = ColumnRegistry()
column_registry.setBoolean('more', size=0, align='centre')
column_registry.setColumn('title', size=20, align='left')
column_registry.setColumn('description', size=40, align='left')
column_registry.setDatetime('created', size=10, align='centre')
column_registry.setColumn('length', size=5, align='centre')

import logging
logging.basicConfig(filename="loggingMe", level=logging.INFO)


def view_notes(model):
    """This constructs how the notes will be viewed."""
    items = [
        TableItem(expansion=('more', 'sub_headings'), **kwargs)
        for kwargs in model['items']
    ]
    first = items[0]
    logging.error(first.title)
    logging.error(first.description)
    logging.error(first.created)
    logging.error(first.length)

    main = TableWindow(
        registry=column_registry,
        items=items,
        w=50,
        down='j',
        up='k',
        select='i',
        expand='e')

    tab = TabBar(model['book'], model['books'], next='l', prev='h')

    return [main, tab]
