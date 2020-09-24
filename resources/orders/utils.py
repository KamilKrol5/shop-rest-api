from typing import List, Optional, Dict

from db import db
from model.item import ItemModel
from model.order_element import OrderElementModel
from resources.common.utils import items_unique


def _validate_order_elements(elements: List[OrderElementModel]) -> Optional[Dict[str, str]]:
    """
    Validates order elements.

    Returns: dictionary with error message if validation fails, None otherwise.
    """
    if invalid := _validate_items_existence(elements):
        return {
            "message": "Some of order elements refer to nonexistent items. "
                       f"Item ids which does not exist: {','.join(map(str, invalid))}"
        }

    if not items_unique([e.item_id for e in elements]):
        return {
            "message": "Order's elements contain 2 or more the same item_ids."
        }
    return None


def _validate_items_existence(elements: List[OrderElementModel]) -> List[int]:
    """
    Validates the existence of item_id for every order element.

    Returns: List of nonexistent items.
    """
    invalid_elements = []
    with db.session.no_autoflush:
        for elem in elements:
            if not ItemModel.find_by_id(elem.item_id):
                invalid_elements.append(elem.item_id)
    return invalid_elements
