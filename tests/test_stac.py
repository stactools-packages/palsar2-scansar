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
    item = stac.create_item(
        "tests/data-files/ALOS2437590500-220630_WWDR2.2GUA_summary.xml"
    )

    # Check that it has some required attributes
    assert item.id == "ALOS2437590500-220630_WWDR2.2GUA"
    # self.assertEqual(item.other_attr...

    # Validate
    item.validate()
