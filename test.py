#!/usr/bin/python3.5

from ptest.decorator import TestClass, Test, BeforeClass, AfterClass
from ptest.assertion import assert_equals
from ptest.plogger import preporter, pconsole
from ptest import config
from io import BytesIO
import pycurl
import json


def test_data_generator():
    with open('sites_list') as f:
        sites = f.readlines()
        sites = [x.strip() for x in sites]
        return sites


def get_request(url):
    buffer = BytesIO()
    self = pycurl.Curl()
    print('URL = ', url)
    self.setopt(self.URL, url)
    self.setopt(self.CONNECTTIMEOUT, 5)
    self.setopt(self.MAXREDIRS, 10)
    self.setopt(self.FOLLOWLOCATION, 1)
    self.setopt(self.COOKIEFILE, '')
    self.setopt(self.FAILONERROR, True)
    self.setopt(self.WRITEDATA, buffer)
    self.setopt(self.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    try:
        self.perform()
    except pycurl.error as error:
        errno, errstr = error
        print('An error occurred: ', errstr)
    return self


def close_session(self):
    self.close()


def data_printer(self):
    EFFECTIVE_URL = self.getinfo(self.EFFECTIVE_URL)
    PRIMARY_IP = self.getinfo(self.PRIMARY_IP)
    NAMELOOKUP_TIME = self.getinfo(self.NAMELOOKUP_TIME)
    CONNECT_TIME = self.getinfo(self.CONNECT_TIME)
    RESPONSE_CODE = self.getinfo(self.RESPONSE_CODE)
    REDIRECT_COUNT = self.getinfo(self.REDIRECT_COUNT)
    REDIRECT_TIME = self.getinfo(self.REDIRECT_TIME)
    SPEED_DOWNLOAD = self.getinfo(self.SPEED_DOWNLOAD)

    preporter.info('EFFECTIVE_URL: %s' % EFFECTIVE_URL)
    preporter.info('PRIMARY_IP: %s' % PRIMARY_IP)
    preporter.info('NAMELOOKUP_TIME: %f' % NAMELOOKUP_TIME)
    preporter.info('CONNECT_TIME: %f' % CONNECT_TIME)
    preporter.info('RESPONSE_CODE %i' % RESPONSE_CODE)
    preporter.info('REDIRECT_COUNT: %i' % REDIRECT_COUNT)
    preporter.info('REDIRECT_TIME: %f' % REDIRECT_TIME)
    preporter.info('SPEED_DOWNLOAD: %f' % SPEED_DOWNLOAD)

    pconsole.write_line('EFFECTIVE_URL: %s' % EFFECTIVE_URL)
    pconsole.write_line('PRIMARY_IP: %s' % PRIMARY_IP)
    pconsole.write_line('NAMELOOKUP_TIME: %f' % NAMELOOKUP_TIME)
    pconsole.write_line('CONNECT_TIME: %f' % CONNECT_TIME)
    pconsole.write_line('RESPONSE_CODE %i' % RESPONSE_CODE)
    pconsole.write_line('REDIRECT_COUNT: %i' % REDIRECT_COUNT)
    pconsole.write_line('REDIRECT_TIME: %f' % REDIRECT_TIME)
    pconsole.write_line('SPEED_DOWNLOAD: %f' % SPEED_DOWNLOAD)
    return self


def json_write(self):
    with open('result', 'w') as outfile:
        json.dumps({'EFFECTIVE_URL': self.EFFECTIVE_URL, 'PRIMARY_IP': self.PRIMARY_IP,
                    'NAMELOOKUP_TIME': self.NAMELOOKUP_TIME, 'CONNECT_TIME': self.CONNECT_TIME,
                    'RESPONSE_CODE': self.RESPONSE_CODE, 'REDIRECT_COUNT': self.REDIRECT_COUNT,
                    'REDIRECT_TIME': self.REDIRECT_TIME, 'SPEED_DOWNLOAD': self.SPEED_DOWNLOAD}, outfile, indent=4)


@TestClass(run_mode="parallel")
class PTestClass:
    # @BeforeClass(data_provider=test_data_generator())
    # def before_class(self, url):
    #     buffer = BytesIO()
    #     self = pycurl.Curl()
    #     print('URL = ', url)
    #     self.setopt(self.URL, url)
    #     self.setopt(self.CONNECTTIMEOUT, 5)
    #     self.setopt(self.MAXREDIRS, 10)
    #     self.setopt(self.FOLLOWLOCATION, 1)
    #     self.setopt(self.COOKIEFILE, '')
    #     self.setopt(self.FAILONERROR, True)
    #     self.setopt(self.WRITEDATA, buffer)
    #     self.setopt(self.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    #     try:
    #         self.perform()
    #     except pycurl.error as error:
    #         errno, errstr = error
    #         print('An error occurred: ', errstr)

    @Test(data_provider=test_data_generator())
    def test1(self, url):
        self = get_request(url)
        assert_equals(self.getinfo(self.RESPONSE_CODE), 200)
        close_session(self)

    @Test(data_provider=test_data_generator())
    def test2(self, url):
        self = get_request(url)
        data_printer(self)
        close_session(self)

    # @AfterClass()
    # def after_class(self):
    #     self.close()
