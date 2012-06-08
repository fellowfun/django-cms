#!/usr/bin/env python
from cms.test_utils.cli import configure
from cms.test_utils.tmpdir import temp_dir
import argparse
import sys


def main(test_runner='cms.test_utils.runners.NormalTestRunner', junit_output_dir='.',
         time_tests=False, verbosity=1, failfast=False):
    with temp_dir() as STATIC_ROOT:
        with temp_dir() as MEDIA_ROOT:
            configure(TEST_RUNNER=test_runner, JUNIT_OUTPUT_DIR=junit_output_dir,
                TIME_TESTS=time_tests, ROOT_URLCONF='cms.test_utils.project.urls',
                STATIC_ROOT=STATIC_ROOT, MEDIA_ROOT=MEDIA_ROOT)
            from django.conf import settings
            from django.test.utils import get_runner
            TestRunner = get_runner(settings)
        
            test_runner = TestRunner(verbosity=verbosity, interactive=False, failfast=failfast)
            failures = test_runner.run_tests(['cms', 'menus'])
    sys.exit(failures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--jenkins', action='store_true', default=False,
            dest='jenkins')
    parser.add_argument('--jenkins-data-dir', default='.', dest='jenkins_data_dir')
    parser.add_argument('--coverage', action='store_true', default=False,
            dest='coverage')
    parser.add_argument('--failfast', action='store_true', default=False,
            dest='failfast')
    parser.add_argument('--verbosity', default=1)
    parser.add_argument('--time-tests', action='store_true', default=False,
            dest='time_tests')
    args = parser.parse_args()
    if getattr(args, 'jenkins', False):
        test_runner = 'cms.test_utils.runners.JenkinsTestRunner'
    else:
        test_runner = 'cms.test_utils.runners.NormalTestRunner'
    junit_output_dir = getattr(args, 'jenkins_data_dir', '.')
    time_tests = getattr(args, 'time_tests', False)
    main(test_runner=test_runner, junit_output_dir=junit_output_dir, time_tests=time_tests,
         verbosity=args.verbosity, failfast=args.failfast)
    