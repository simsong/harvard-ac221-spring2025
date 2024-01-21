"""
test_explain_columns.py - a test program
"""

import os
import argparse
import explain_columns
import pytest                   # pylint: disable=unused-import   (needed for mocker below)

FROM_FILE_CONTENTS="this,is,a,test\n1,2,3,4\n5,6,7,8\n"

# Note: mocker below is magically created because pytest-mock is included in the runtime environment.
# see https://pypi.org/project/pytest-mock/

def test_explain_columns(mocker):
    with open('from_file.csv','w') as from_file:
        from_file.write(FROM_FILE_CONTENTS)

    mocker.patch('argparse.ArgumentParser.parse_args',
                 return_value = argparse.Namespace(from_file='from_file.csv', to_file='to_file.csv'))
    explain_columns.main()
    assert os.path.exists('to_file.csv')
    with open('to_file.csv','r') as to_file:
        assert next(to_file)=='column,header\n'
        assert next(to_file)=='0,this\n'
        assert next(to_file)=='1,is\n'
        assert next(to_file)=='2,a\n'
        assert next(to_file)=='3,test\n'
        assert to_file.read()==''

    os.unlink('to_file.csv')
    assert not os.path.exists('to_file.csv')
    os.unlink('from_file.csv')
