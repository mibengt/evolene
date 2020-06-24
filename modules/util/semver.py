__author__ = 'tinglev'

def get_patch(version):
    '''
    From "2.3.45"  latest published npm version
    return "45" to use as major.minor when se.kth.automaticPublish is true
    '''
    patch_version_index = version.rfind(".") + 1
    patch_version = version[patch_version_index:]
    
    return int(patch_version)


def get_next_patch(version):
    '''
    Incremented patch version.
    '''
    return get_patch(version) + 1


def get_major_minor(version):
    '''
    Gets the major minor didgits = "[1.2].3"
    '''
    patch_version_index = version.rfind(".")
    result = version[:patch_version_index]

    return result


def get_next(version):
    '''
    Gets the next version 
    major.minor.[patch +1]
    '''
    major_minor = get_major_minor(version)
    patch = get_next_patch(version)
    next_version = f"{major_minor}.{patch}"

    return next_version



