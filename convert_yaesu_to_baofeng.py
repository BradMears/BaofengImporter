import sys
import pandas as pd

ifilename = sys.argv[1]
ofilename = sys.argv[2]

df=pd.read_csv(ifilename, sep=',', keep_default_na = False)

# Column headings in the file exported from RTSystemsYaesu
yaesu_columns = ("Channel Number", "Receive Frequency", "Transmit Frequency", 
                 "Offset Frequency", "Offset Direction", "Operating Mode", "Name", 
                 "Show Name", "Tone Mode", "CTCSS", "DCS", "Tx Power", "Skip", 
                 "Step", "Clock Shift", "Comment", "User CTCSS")

# Column headings expected in the file imported into chirp/Baofeng
baofeng_columns=("Location", "Name", "Frequency", "Duplex", "Offset", "Tone", 
                 "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "Mode", 
                 "TStep", "Skip", "Comment", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE")

del df['Unnamed: 17']
for actual in df.columns:
    assert actual in yaesu_columns, f'{actual} not recognized'

df_out = pd.DataFrame(columns=baofeng_columns)

# Populate the Location column
df_out['Location'] = df['Channel Number'] - 1

# Populate the Name column
df_out['Name'] = df['Name']

# Populate the Frequency column
df_out['Frequency'] = df['Receive Frequency']

# Populate the Duplex column
df_out['Duplex'] = df['Offset Direction'] \
    .replace('Simplex', '') \
    .replace('Minus', '-') \
    .replace('Plus', '+')

# Populate the Offset column
df_out['Offset'] = df['Offset Frequency'] \
    .replace('5.00 MHz', '5') \
    .replace('600 kHz', '0.6')

# Populate the Tone column
df_out['Tone'] = df['Tone Mode'] \
    .replace('None', '') \

# Populate the rToneFreq column
df_out['rToneFreq'] = df['CTCSS']
for ndx,s in enumerate(df_out['rToneFreq']):
    df_out.at[ndx,'rToneFreq'] = s.replace(' Hz', '')

# Populate the cToneFreq column
df_out['cToneFreq'] = df_out['rToneFreq']

# Populate the DtcsCode column
df_out['DtcsCode'] = '23'

# Populate the DtcsPolarity column
df_out['DtcsPolarity'] = 'NN'

# Populate the Mode column
df_out['Mode'] = df['Operating Mode']

# Populate the TStep column
df_out['TStep'] = '5'

# Populate the Skip column
df_out['Skip'] = df['Skip'] \
    .replace('Off', '') \
    .replace('Select', '') \
    .replace('Skip', 'S')

# Populate the Comment column
df_out['Comment'] = df['Comment']

# Populate the URCALL column
df_out['URCALL'] = ""

# Populate the RPT1CALL column
df_out['RPT1CALL'] = ""

# Populate the RPT2CALL column
df_out['RPT2CALL'] = ""

# Populate the DVCODE column
df_out['DVCODE'] = ""

df_out.to_csv(ofilename, sep=',', columns=baofeng_columns, index=False)

    
