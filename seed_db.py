import sqlite3

# Connect- creating the file
conn = sqlite3.connect('constituency_data.db')
c = conn.cursor()

# Create the 'Truth' table
c.execute('''CREATE TABLE IF NOT EXISTS polling_stations 
             (id TEXT PRIMARY KEY, constituency TEXT, expected_voters INTEGER)''')

# Add Mock Data (Simulating Kenyan Constituencies)
stations = [
    ('PS-001', 'Langata', 600),
    ('PS-002', 'Kibra', 450),
    ('PS-003', 'Roysambu', 800)
]

c.executemany('INSERT OR REPLACE INTO polling_stations VALUES (?,?,?)', stations)
conn.commit()
conn.close()
print("✅ Database seeded with 3 Mock Stations!")