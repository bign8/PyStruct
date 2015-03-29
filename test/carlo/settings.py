PORT = 8880
MASTER = '192.168.1.20'

plex_960 = [
    '192.168.1.50',  # x4
    '192.168.1.51',
    '192.168.1.52',
    '192.168.1.53',
    '192.168.1.54'
]

plex_745 = [
    '192.168.1.55',  # x2
    '192.168.1.56',
    '192.168.1.57',
    '192.168.1.58',
    '192.168.1.59',
    '192.168.1.60',
    '192.168.1.61'
]

WORKERS = plex_960 + plex_745

# # Configure worker list to use separate ports
# hashmap = {}
# for i, worker in enumerate(WORKERS):
#     if worker in hashmap:
#         num = hashmap[worker] + 1
#     else:
#         num = PORT
#     WORKERS[i] += ':{}'.format(num)
#     hashmap[worker] = num

del plex_745, plex_960
