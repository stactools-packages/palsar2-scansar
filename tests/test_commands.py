import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.palsar2_scansar.commands import create_palsar2scansar_command


class CommandsTest(CliTestCase):  # type: ignore
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_palsar2scansar_command]

    def test_create_collection(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-collection command and validate

            # Example:
            destination = os.path.join(tmp_dir, "collection.json")

            result = self.run_command(f"palsar2-scansar create-collection {tmp_dir}")

            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            collection = pystac.read_file(destination)
            assert collection.id == "palsar2-scansar"
            # assert collection.other_attr...

            collection.validate()

    def test_create_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            # Run your custom create-item command and validate

            # Example:
            item_id = "ALOS2437590500-220630_WWDR2.2GUA"
            infile = f"tests/data-files/{item_id}_summary.xml"
            destination = os.path.join(tmp_dir, f"{item_id}.json")
            result = self.run_command(f"palsar2-scansar create-item {infile} {tmp_dir}")
            assert result.exit_code == 0, "\n{}".format(result.output)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            assert len(jsons) == 1

            item = pystac.read_file(destination)
            assert item.id == "ALOS2437590500-220630_WWDR2.2GUA"
            # assert item.other_attr...

            item.validate()
