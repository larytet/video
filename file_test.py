import contextlib
import errno
import os
import sys
import tempfile
if (sys.platform == 'win32'):
    import win32api, win32con

if sys.platform != 'win32':
    def _atomic_rename(src, dst):
        os.rename(src, dst)

    def _atomic_move(src, dst):
        os.link(src, dst)
        os.unlink(src)
else:
    def _atomic_rename(src, dst):   
        win32api.MoveFileEx(src, dst, win32con.MOVEFILE_WRITE_THROUGH |  win32con.MOVEFILE_REPLACE_EXISTING)

    def _atomic_move(src, dst):
        win32api.MoveFileEx(src, dst, win32con.MOVEFILE_WRITE_THROUGH)
        

def atomic_rename(src, dst):
    return _atomic_rename(src, dst)


def atomic_move(src, dst):
    return _atomic_move(src, dst)


class FileAtomic(object):
    def __init__(self, path, mode='w', overwrite=False):
        if 'a' in mode:
            raise ValueError('Appending to a file is not supported')
        if 'x' in mode:
            raise ValueError('Use the `overwrite`-parameter instead.')
        if 'w' not in mode:
            raise ValueError('file_atomic can only be written to.')
        self._f = None  
        self._path = path
        self._mode = mode
        self._overwrite = overwrite

    def open(self):
        '''
        Will open a temporary file.
        '''
        success = False
        try:
            self._f = self.create_file()
            success = True
        finally:
            if not success:
                try:
                    self.cleanup(self._f)
                except Exception:
                    pass
        return self._f

    def create_file(self, dir=None, **kwargs):
        if dir is None:
            dir = os.path.dirname(self._path)
        f = tempfile.NamedTemporaryFile(mode=self._mode, dir=dir,
                                           delete=False, **kwargs)
        return f

    def sync(self):
        '''Flush and sync everything'''
        self._f.flush()
        os.fsync(self._f.fileno())

    def commit(self):
        '''Copy the temporary file to the final location'''
        if self._overwrite:
            atomic_rename(self._f.name, self._path)
        else:
            atomic_move(self._f.name, self._path)
       
    def cleanup(self, f):
        os.unlink(f.name)

    def close(self):
        self.commit()
        self._f.close()


fa = FileAtomic("/tmp/t")
f = fa.open()
f.write("Hello");
fa.close()
