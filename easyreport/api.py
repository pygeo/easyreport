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
    def __init__(self, id, **kwargs):
        self.id = id
        for k in kwargs.keys():  # set class attributes from kwargs
            setattr(self, k, kwargs[k])

    def _att2dict(self):
        """ converts attributes to dictionary """
        o = {}
        for attr, value in self.__dict__.iteritems():
            if attr == 'id':
                pass
            else:
                o.update({attr : value})
        return {self.id : o}


class GraphicFeature(Feature):
    def __init__(self, id, caption, file, **kwargs):
        super(GraphicFeature, self).__init__(id, caption=caption, file=file, **kwargs)


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

        resdict = self._gen_final_dict()
        yaml.dump(resdict, stream=open(self.file, 'w'), default_flow_style=False)

    def _gen_final_dict(self):
        """
        convert section information to a dictionary that can be
        used for yml output
        """
        out = {}
        for k in self.sections:
            x = self.sections[k]  # always gives a list
            hlp = []
            for l in x:
                if type(l) is dict:
                    hlp.append(l)
                elif type(l) is Feature:
                    hlp.append(l._att2dict())
                else:
                    print type(l)
                    raise ValueError('Unknown input type!')
            out.update({k : hlp})

        #needs to be done recursively for Feature!!!

        return out


