__author__ = 'tinglev'


def get_patch(self, version):
    '''
    From "2.3.45"  latest published npm version
    return "45" to use as major.minor when se.kth.automaticPublish is true
    '''
    patch_version_index = version.rfind(".") + 1
    patch_version = version[patch_version_index:]
    self.log.debug('Next free patch version is: %s', patch_version)
    
    return int(patch_version)


def get_next_patch(self, version):
    '''
    Incremented patch version.
    '''
    return self.get_patch(version) + 1


def get_major_minor(self, version):
    '''
    Gets the major minor didgits = "[1.2].3"
    '''
    patch_version_index = version.rfind(".")
    result = version[:patch_version_index]
    self.log.info("Major.minor specified in package.json version '%s' is '%s'", version, result)

    return result


def get_next(self, version):
    '''
    Gets the next version 
    major.minor.[patch +1]
    '''
    major_minor = self.get_major_minor(version)
    patch = self.get_next_patch(version)
    next_version = f"{major_minor}.{patch}"
    self.log.info("Next available version is '%s'.", next_version)

    return next_version



