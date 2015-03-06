"""
easyreport main class
"""
import os
import tempfile
import yaml

class Report(object):
    def __init__(self, template_file, interface_file, output_directory=None, output_file=None, suffix=None, sphinx_dir='.'+ os.sep + 'easyreport' + os.sep + 'sphinx_cfg', report_format='html'):
        """
        template_file : str
            name of file which contains template to parse
        interface_file : str
            name of yaml interface file describing structure of output
        output_directory : str
            directory where report will be written to; temporary directory will be generated if not given
        output_file : str
            filename for report; temporary file will be generated if not given
        suffix : str
            file suffix (e.g. rst, txt)
        report_format : str
            ['html', 'latexpdf']
            format of report (needs to be supported by Sphinx)
        """
        self.output_directory = output_directory
        self.output_file = output_file
        self.template = template_file
        self.interface = interface_file
        self.suffix = suffix
        self.report_format = report_format
        self.sphinx_dir = sphinx_dir

        self._check()

    def _check(self):
        """
        check consitency of configuration
        """
        if self.output_directory is None:
            self.output_directory = tempfile.mkdtemp()
            print 'Generate temporary output directory ... ' + self.output_directory
        else:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)
                print 'Output directory created!'
        #~ print 'Output directory: ', self.output_directory
        if self.output_directory[-1] != os.sep:
            self.output_directory += os.sep
        assert os.path.exists(self.output_directory), 'Output directory not existing!'
        assert os.path.exists(self.template), 'Template file is not existing! ' + self.template
        assert os.path.exists(self.interface), 'Interface file is not existing! ' + self.interface
        assert self.suffix is not None, 'Suffix needs to be given'
        assert os.path.exists(self.sphinx_dir), 'Sphinx directory not existing!'

        if self.sphinx_dir[-1] != os.sep:
            self.sphinx_dir += os.sep
        if self.output_file is None:
            self.output_file = os.path.basename(tempfile.mktemp(suffix='.' + self.suffix,dir=self.output_directory))
        if self.output_file[-len(self.suffix):] == self.suffix:
            pass
        else:
            self.output_file += '.' + self.suffix

    def compile(self, run=False):
        """
        generate report and
        compile report using SPHINX
        """
        # generate report based on templates
        self._generate_report()
        if run:
            self._run_sphinx([self.output_file])

    def _generate_report(self):
        """
        report generation uses makotemplates
        """
        from mako.template import Template
        from mako.lookup import TemplateLookup

        # generate template object
        t = Template(filename=self.template)

        # render output
        res = t.render(**self.x)

        # write result to file
        o = open(self.output_directory + self.output_file, 'w')
        o.write(res)
        o.close()

    def _run_sphinx(self, flist):
        """
        run SPHINX to generate report
        uses currently a generic template

        Parameters
        ----------
        flist : list
            list of names to be included in index.rst
        """

        self._gen_sphinx_template(flist)
        curdir=os.curdir
        os.chdir(self.output_directory)
        self._make(self.report_format)
        os.chdir(curdir)

    def _gen_sphinx_template(self, flist):
        """
        generate sphinx template; currently use standard setup which
        is copied from the specified spinx directory
        """
        #TBD generate sphinx conf.py automatically by default or use a default one
        # allow user to specify their own conf.py file

        # copy sphinx standard setup
        os.system('cp -r ' + self.sphinx_dir + '* ' + self.output_directory)

        # modify index file
        F = open(self.output_directory + 'index_template.rst')
        ofile = self.output_directory + 'index.rst'
        if os.path.exists(ofile):
            os.remove(ofile)
        O = open(ofile, 'w')

        sep = '   '
        eol = '\n'

        files = ''
        for a in flist:
            files += sep + a + eol

        for l in F.readlines():
            c = l.replace('<FILES>', files)
            O.write(c)
        F.close()
        O.close()

    def _make(self, fmt):
        """ run sphinxs with specified format """
        assert fmt in ['html', 'latexpdf'], 'Unsupported format!'
        os.system('make ' + fmt)
        #TBD use sphinx directly
        #http://sphinx-doc.org/config.html#build-config

    def parse(self):
        """
        parse interface file and store results in dictionary
        """
        self.x = yaml.load(open(self.interface, 'r'))

