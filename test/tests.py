import unittest
from MVC_template import View

class TestViewMethods(unittest.TestCase):

    def setUp(self):
        self.view = View()


    def test_outputfilename(self):
        self.view.set_outputfolder('build')
        self.view.set_outfilename('out')
        self.view.set_extension('png,pdf')
	outputfilenames = [output_file_name for output_file_name in self.view.get_outfile_name()]
        self.assertEqual(outputfilenames, ['build/out.png','build/out.pdf'])

if __name__ == '__main__':
    unittest.main()


