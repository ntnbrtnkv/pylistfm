import os
import logging
from uuid import UUID


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False

    return True

def create_hardlist(source):
    _logger = logging.getLogger('pylistfm')
    _logger.info("Creating hardlist for playlist: {}".format(source))
    base_dir = os.path.dirname(source)
    source_basename = os.path.basename(source)
    source_filename = os.path.splitext(source_basename)[0]
    dest = '{}/{}'.format(base_dir, source_filename)
    _logger.info("Path for hardlist: {}".format(dest))
    if not os.path.exists(dest):
        _logger.warning("Path not found '{}', creating directories".format(dest))
        os.makedirs(dest)
    _logger.info("Creating hardlinks in destination path")
    with open(source, 'r', encoding='utf-8') as playlist_file:
        tracks_files = filter(lambda line: line[0] != '#', list(playlist_file)[1:])
        for index, line in enumerate(tracks_files):
            path = line.rstrip('\n')
            filepath = '{}/{}'.format(base_dir, path)
            filename = os.path.basename(filepath)
            os.link(filepath, '{}/{:03d} - {}'.format(dest, index, filename))
    _logger.info("Hardlist has been created")