from stactools.palsar2_scansar import stac


def test_create_collection() -> None:
    # Write tests for each for the creation of a STAC Collection
    # Create the STAC Collection...
    collection = stac.create_collection()
    collection.set_self_href("")

    # Check that it has some required attributes
    assert collection.id == "palsar2-scansar"
    # self.assertEqual(collection.other_attr...

    # Validate
    collection.validate()


def test_create_item() -> None:
    # Write tests for each for the creation of STAC Items
    # Create the STAC Item...
    item = stac.create_item("tests/data-files/ALOS2412212550-220110_WBSR2.2GUD")

    # Check that it has some required attributes
    assert item.id == "ALOS2412212550-220110_WBSR2.2GUD"
    # self.assertEqual(item.other_attr...

    # Validate
    item.validate()
