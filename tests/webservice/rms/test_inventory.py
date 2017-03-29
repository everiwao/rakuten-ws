# coding: utf-8
from __future__ import unicode_literals


def test_get_inventory_external(ws):
    result = ws.rms.inventory.getInventoryExternal(itemUrl='SKU7EHDR72ZZ4TPSSS')
    # 'N00-000' => Successfully completed
    assert result['errCode'] == 'N00-000'


def get_inventory_count(ws, sku):
    unique = False
    if not isinstance(sku, (list, tuple)):
        unique = True
        sku = [sku]
    result = ws.rms.inventory.getInventoryExternal(itemUrl=sku)
    inventory_counts = {}
    for info in result['getResponseExternalItem']['GetResponseExternalItem']:
        count = (info['getResponseExternalItemDetail']
                     ['GetResponseExternalItemDetail'][0]['inventoryCount'])
        item_url = info['itemUrl'].upper()
        inventory_counts[item_url] = count
    if unique:
        return inventory_counts[sku[0].upper()]
    else:
        return inventory_counts


def test_update_inventory_external(ws):
    count = get_inventory_count(ws, "SKU7EHDR72ZZ4TPSSS")
    update_request = {
        'itemUrl': "SKU7EHDR72ZZ4TPSSS",
        'inventoryType': 2,
        'inventoryUpdateMode': 1,
        'inventory': count + 1
    }
    result = ws.rms.inventory.updateInventoryExternal(update_request)
    # 'N00-000' => Successfully completed
    assert result['errCode'] == 'N00-000'

    new_count = get_inventory_count(ws, "SKU7EHDR72ZZ4TPSSS")
    assert new_count == count + 1


def test_multiple_update_inventory_external(ws):
    item_url_list = ['SKU7EHDR72ZZ4TPSSS', 'SKU7EHDR72ZZ4TPZZZ']
    counts = get_inventory_count(ws, item_url_list)
    update_request = [
        {
            'itemUrl': "SKU7EHDR72ZZ4TPSSS",
            'inventoryType': 2,
            'inventoryUpdateMode': 1,
            'inventory': counts["SKU7EHDR72ZZ4TPSSS"] + 10
        },
        {
            'itemUrl': "SKU7EHDR72ZZ4TPZZZ",
            'inventoryType': 2,
            'inventoryUpdateMode': 1,
            'inventory': counts["SKU7EHDR72ZZ4TPZZZ"] + 10
        }
    ]
    result = ws.rms.inventory.updateInventoryExternal(update_request)
    # 'N00-000' => Successfully completed
    assert result['errCode'] == 'N00-000'

    new_counts = get_inventory_count(ws, item_url_list)

    for item_url in item_url_list:
        assert new_counts[item_url] == counts[item_url] + 10
