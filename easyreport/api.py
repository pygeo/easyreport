"""
API to be integrated in client programs
"""

import os
import sys
import yaml


class Feature(object):
    """
    class to handle
    """
    def __init__(self, **kwargs):
        for k in kwargs.keys():  # set class attributes from kwargs
            setattr(self, k, kwargs[k])

class GraphicFeature(Feature):
    def __init__(self, caption, file, **kwargs):
        super(GraphicFeature, self).__init__(caption=caption, file=file, **kwargs)


class EasyReport(object):
    """
    main class to handle entire IO process for the client program

    Example
    -------

    F = EasyReport(file='test')
    F.add('model', myfeature1)
    F.add('model', 'hello')
    F.save()  # will result in a file test.yml

    """
    def __init__(self, file=None, **kwargs):
        self.file = file
        self.sections = {}

        assert self.file is not None, 'Filename needs to be specified!'
        if self.file[:-4] != '.yml':
            self.file += '.yml'


    def add(self, section, v):
        """
        add a section to the report and store results in it

        section : str
            section to which the entry shall be added
        v : tuple or Feature
            value that shall be stored; needs to be either a (key,value) pair
            or a Feature object
        """

        def _append(v):
            if type(v) is tuple:
                return {v[0] : v[1]}
            else:
                return v

        assert (type(v) is tuple) or (type(v) is Feature)

        if section in self.sections.keys():
            h = self.sections[section]
        else:
            h = []  # always as list
        h.append(_append(v))
        self.sections.update({section: h})

    def save(self):
        if os.path.exists(self.file):
            os.remove(self.file)
        yaml.dump(self.sections, stream=open(self.file, 'w'), default_flow_style=False)


