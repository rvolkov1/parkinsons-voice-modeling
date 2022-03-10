import synapseclient
import json

syn = synapseclient.Synapse()

syn.login('rvolkov', 'mhs19542')

entity = syn.get('syn5511444')

for offset in range(0, 65000, 100):
    results = syn.tableQuery('SELECT * FROM syn5511444 LIMIT 100 OFFSET '+str(offset))
    file_map = syn.downloadTableColumns(results, ['audio_audio.m4a', 'audio_countdown.m4a'])
