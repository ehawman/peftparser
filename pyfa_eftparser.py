import re


class PEFTParser(object):
    def split_blocks(eft_textblock):
        info = []
        modules = []
        nonmodules = []
        abyssals = []

        # Abyssals block

        # Pattern matches the first abyssal and matches all the way to the end.
        pattern = r"^\[[1-9][0-9]*\][\S\s]*"
        abyssals = re.findall(pattern, eft_textblock, flags=re.M)
        if abyssals:
            abyssals = abyssals[0]
            # Delete the abyssal block from eft_textblock
            eft_textblock = eft_textblock.replace(abyssals, "").strip()
            print(eft_textblock)

        # Prepping for additional searches
        split_eft_textblock = eft_textblock.strip().splitlines()

        # Info "block"
        info.append(split_eft_textblock.pop(0))

        # Modules block
        enumerated_block = enumerate(split_eft_textblock)
        blank = False
        for index, line in enumerated_block:
            if line:
                modules.append(line)
                blank = False
            elif blank:
                # If finding a double blank, done with the modules block. Delete current results
                del split_eft_textblock[:index]
                break
            else:
                modules.append(line)
                blank = True

        # Nonmodules block
        eft_textblock = "\n".join(split_eft_textblock).strip()
        d_indexes = []
        d_matches = re.finditer(r"\n\n\n", eft_textblock, flags=re.M)
        if d_matches:
            for match in d_matches:
                print(f"Double match at {match.start()}")
                d_indexes.append(match.start())
        s_indexes = []
        s_matches = re.finditer(r"[^\n]\n\n[^\n]", eft_textblock, flags=re.M)
        if s_matches:
            for match in s_matches:
                print(f"Single match at {match.start()}")
                s_indexes.append(match.start())
        print("")
        # DSD (drones, implants, boosters, cargo)

        # DS (drones, implants, boosters)

        # SD (implants, boosters, cargo)

        # DD (drones, implants|boosters, cargo) ask

        # D (drones, implants|boosters|cargo) x#|no OR (implants|boosters, cargo) no|x# OR (drones, cargo) x#|x#

        # S (implants, boosters)

        results = {
            "info": info,
            "modules": modules,
            "nonmodules": nonmodules,
            "abyssals": abyssals,
        }

        return results

    @staticmethod
    def parse(eft_textblock):
        """
        Parse an EFT Text Block and return structure with specified function. Follows Pyfa structure.

        {
            "ship_type": "Leshak",
            "fit_name": "Test Leshak",
            "modules": {
                "lows": [
                    {"name": xxx, "charge": yyy}
                ],
                "mids": [
                    {"name": xxx, "charge": yyy}
                ]
                ...
            },
            "drones": [
                {"name": xxx, "quantity": yyy},
            ]
            "implants": [
                {"name": xxx}
            ],
            "boosters": [
                {"name": xxx}
            ],
            "cargo": [
                {"name": xxx, "quantity": yyy},
                {"name": xxx, "quantity": yyy},
            ]
        }
        """

        fit_lines = eft_textblock.strip().splitlines()

        lows = []
        mids = []
        highs = []
        rigs = []
        drones = []
        implants = []
        boosters = []
        cargo = []
        abyssals = []
        ship_type = ""
        fit_name = ""

        result = {
            "ship_type": ship_type,
            "fit_name": fit_name,
            "modules": {"lows": lows, "mids": mids, "highs": highs, "rigs": rigs},
            "drones": drones,
            "implants": implants,
            "boosters": boosters,
            "cargo": cargo,
            "abyssals": abyssals,
        }
        return result
