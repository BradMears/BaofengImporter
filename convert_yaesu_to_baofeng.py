#!/usr/bin/env python3
"""Convert a file exported from a Yaesu FTM400 to one that can be imported by a Baofeng UV-5R."""
import sys
import pandas as pd

IFILENAME = sys.argv[1]
OFILENAME = sys.argv[2]


def auto_truncate(val):
    return val[:7]


DF = pd.read_csv(
    IFILENAME, sep=",", keep_default_na=False, converters={"Name": auto_truncate}
)
del DF["Unnamed: 17"]

# Column headings in the file exported from RTSystemsYaesu
YAESU_COLUMNS = (
    "Channel Number",
    "Receive Frequency",
    "Transmit Frequency",
    "Offset Frequency",
    "Offset Direction",
    "Operating Mode",
    "Name",
    "Show Name",
    "Tone Mode",
    "CTCSS",
    "DCS",
    "Tx Power",
    "Skip",
    "Step",
    "Clock Shift",
    "Comment",
    "User CTCSS",
)

# Column headings expected in the file imported into chirp/Baofeng
BAOFENG_COLUMNS = (
    "Location",
    "Name",
    "Frequency",
    "Duplex",
    "Offset",
    "Tone",
    "rToneFreq",
    "cToneFreq",
    "DtcsCode",
    "DtcsPolarity",
    "Mode",
    "TStep",
    "Skip",
    "Comment",
    "URCALL",
    "RPT1CALL",
    "RPT2CALL",
    "DVCODE",
)

for actual in DF.columns:
    assert actual in YAESU_COLUMNS, f"{actual} not recognized"

df_out = pd.DataFrame(columns=BAOFENG_COLUMNS)  # pylint: disable-msg=C0103

# Populate the Location column
df_out["Location"] = DF["Channel Number"] - 1

# Populate the Name column
df_out["Name"] = DF["Name"]

# Populate the Frequency column
df_out["Frequency"] = DF["Receive Frequency"]

# Populate the Duplex column
df_out["Duplex"] = (
    DF["Offset Direction"]
    .replace("Simplex", "")
    .replace("Minus", "-")
    .replace("Plus", "+")
)

# Populate the Offset column
df_out["Offset"] = (
    DF["Offset Frequency"].replace("5.00 MHz", "5").replace("600 kHz", "0.6")
)

# Populate the Tone column
df_out["Tone"] = DF["Tone Mode"].replace("None", "")
# Populate the rToneFreq column
df_out["rToneFreq"] = DF["CTCSS"]
for ndx, s in enumerate(df_out["rToneFreq"]):
    df_out.at[ndx, "rToneFreq"] = s.replace(" Hz", "")

# Populate the cToneFreq column
df_out["cToneFreq"] = df_out["rToneFreq"]

# Populate the DtcsCode column
df_out["DtcsCode"] = "23"

# Populate the DtcsPolarity column
df_out["DtcsPolarity"] = "NN"

# Populate the Mode column
df_out["Mode"] = DF["Operating Mode"]

# Populate the TStep column
df_out["TStep"] = "5"

# Populate the Skip column
# df_out["Skip"] = (
#    DF["Skip"].replace("Off", "").replace("Select", "").replace("Skip", "S")
# )
df_out["Skip"] = ""

# Populate the Comment column
df_out["Comment"] = ""  # DF["Comment"]

# Populate the URCALL column
df_out["URCALL"] = ""

# Populate the RPT1CALL column
df_out["RPT1CALL"] = ""

# Populate the RPT2CALL column
df_out["RPT2CALL"] = ""

# Populate the DVCODE column
df_out["DVCODE"] = ""

df_out.to_csv(OFILENAME, sep=",", columns=BAOFENG_COLUMNS, index=False)
