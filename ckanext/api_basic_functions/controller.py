from logging import getLogger
from ckan.lib.base import request, BaseController, abort, json, c

import pylons.config as config

import sys
import os
import subprocess
import shlex
import getpass

log = getLogger(__name__)

class Resource_api_basic_functionsController(BaseController):

        def create_file(self,file_route,received_data):

            print '*** USER: ' + getpass.getuser()
            print '*** WKD: ' + os.getcwd()

            try:
                file = open(file_route, "w")
                file.truncate()
                file.write(received_data)
                file.close()
            except IOError as (errno, strerror):
                log.info('I/O error({0}): {1}'.format(errno, strerror))
                abort(500, 'I/O error({0}): {1}'.format(errno, strerror))
            except (OSError) as (errno, strerror):
                log.info('OS error({0}): {1}'.format(errno, strerror))
                abort(500, 'OS error({0}): {1}'.format(errno, strerror))
            except:
                log.info('Unexpected error')
                abort(500, 'Unexpected error')
                raise

        def reindex_solr(self):

            if not request.method == 'GET':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic functions - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            config_file = config.get('ckan.api_basic.config_file', '')

            if config_file == '':
                log.info('API basic function - error detected, config_file parameter not defined in configuration file')
                abort(403, 'Forbidden, config_file parameter not defined in configuration file')

            ve_route = config.get('ckan.api_basic.virtual_evnvironment_route')

            if ve_route == '':
                log.info('API basic function - error detected, ve_route parameter not defined in configuration file')
                abort(403, 'Forbidden, ve_route parameter not defined in configuration file')

            log.info('API basic function reindex solr - Validations ok, execute command reindex')
            result = subprocess.check_output(
                shlex.split(ve_route + '/bin/paster --plugin=ckan search-index rebuild --config=' + config_file),
                cwd=ve_route + '/src/ckan')

            print result

        def clear_index_solr(self):

            if not request.method == 'GET':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic functions - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            solr_url = config.get('solr_url', '')

            if solr_url == '':
                log.info('API basic function - error detected, solr parameter not defined in configuration file')
                abort(403, 'Forbidden, config_file parameter not defined in configuration file')

            ve_route = config.get('ckan.api_basic.virtual_evnvironment_route')

            if ve_route == '':
                log.info('API basic function - error detected, ve_route parameter not defined in configuration file')
                abort(403, 'Forbidden, ve_route parameter not defined in configuration file')

            log.info('API basic function reindex solr - Validations ok, execute command reindex')
            result = subprocess.check_output(
                shlex.split('curl ' + solr_url.strip() + '/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E'),
                cwd=ve_route + '/src/ckan')

            print result

            result = subprocess.check_output(
                shlex.split('curl ' + solr_url.strip() + '/update?stream.body=<commit/>'),
                cwd=ve_route + '/src/ckan')

            print result

        def execute_query(self):

            if not request.method == 'POST':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic function - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            if not request.body:
                log.info('API basic function - error detected, no request body received')
                abort(400, 'No body data received')

            content_type = request.headers.get('Content-Type', '')

            if not content_type.startswith('text/plain'):
                log.info('API basic function - error detected, invalid content type')
                abort(415, 'Content-Type should be text/plain')

            query = request.body

            con_string = config.get('sqlalchemy.url', '')

            if con_string == '':
                log.info('API basic function - error detected, sqlalchemy.url parameter not defined in configuration file')
                abort(403, 'Forbidden, sqlalchemy.url parameter not defined in configuration file')

            iso = config.get('ckan.api_basic.iso', '')

            if iso == '':
                log.info(
                    'API basic fu   nction - error detected, ckan.api_basic. parameter not defined in configuration file')
                abort(403, 'Forbidden, ckan.api_basic. parameter not defined in configuration file')

            postgre_str = 'postgresql://'

            user_pass = con_string[con_string.find(postgre_str) + len(postgre_str):con_string.find('@')]
            user = user_pass[:user_pass.find(':')]
            password = user_pass[user_pass.find(':') + 1:]

            host_sch = con_string[con_string.find('@') + 1:]
            host = host_sch[:host_sch.find('/')]

            schema = host_sch[host_sch.find('/') + 1:]

            if schema.find('?') <> -1:
                schema = schema[:schema.find('?')]

            log.info('API basic function execute_query - Validations ok, execute query')
            log.info(
                'export PGPASSWORD=\'' + password + '\'; export PGCLIENTENCODING=\'' + iso + '\'; psql -h \'' + host + '\' -U \'' + user + '\' -d \'' + schema + '\' -c \"' + query + '\"')

            try:
                result = subprocess.check_output(
                    #'export PGPASSWORD=\'' + password + '\'; export PGCLIENTENCODING=\'' + iso + '\'; psql -h \'' + host + '\' -U \'' + user + '\' -d \'' + schema + '\' -c \"' + query + '\"',
                    'export PGCLIENTENCODING=\'' + iso + '\'; psql ' + con_string + ' -c  \"' + query + '\"',
                    stderr=subprocess.STDOUT, shell=True)
                print result
            except:
                try:
                    result = subprocess.check_output(
                        #'export PGPASSWORD=\'' + password + '\'; export PGCLIENTENCODING=; psql -h \'' + host + '\' -U \'' + user + '\' -d \'' + schema + '\' -c \"' + query + '\"',
                        'export PGCLIENTENCODING=; psql ' + con_string + ' -c \"' + query + '\"',
                        stderr=subprocess.STDOUT, shell=True)
                    print result
                except subprocess.CalledProcessError as e:
                    print e.output
                    print 'Error running command: ' + '"' + e.cmd + '"' + ' see above shell error'
                    print 'Return code: ' + str(e.returncode)
                    return e.returncode, e.cmd

        def execute_script_sql(self):

            if not request.method == 'POST':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic function - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            content_type = request.headers.get('Content-Type', '')

            if not content_type.startswith('text/plain'):
                log.info('API basic function - error detected, invalid content type')
                abort(415, 'Content-Type should be text/plain')

            path = request.params.get('path', '')

            if path == '':
                log.info('API basic function - error detected, need path param in post parameter')
                abort(400, 'Bad Request, need path param')

            try:
                open(path)
            except (OSError, IOError) as e:
                log.info('API basic function - file path must be exist and execute permissions setted')
                abort(400, 'File path must be exist and execute permissions setted')

            con_string = config.get('sqlalchemy.url', '')

            if con_string == '':
                log.info('API basic function - error detected, sqlalchemy.url parameter not defined in configuration file')
                abort(403, 'Forbidden, sqlalchemy.url parameter not defined in configuration file')

            iso = config.get('ckan.api_basic.iso', '')

            if iso == '':
                log.info(
                    'API basic function - error detected, ckan.api_basic. parameter not defined in configuration file')
                abort(403, 'Forbidden, ckan.api_basic. parameter not defined in configuration file')

            postgre_str = 'postgresql://'

            user_pass = con_string[con_string.find(postgre_str) + len(postgre_str):con_string.find('@')]
            user = user_pass[:user_pass.find(':')]
            password = user_pass[user_pass.find(':') + 1:]

            host_sch = con_string[con_string.find('@') + 1:]
            host = host_sch[:host_sch.find('/')]
            schema = host_sch[host_sch.find('/') + 1:]

            if schema.find('?') <> -1:
                schema = schema[:schema.find('?')]

            log.info('API basic function execute_script_sql- Validations ok, execute script sql')

            try:
                result = subprocess.check_output(
                    #'export PGPASSWORD=\'' + password + '\'; export PGCLIENTENCODING=\'' + iso + '\'; psql -h \'' + host + '\' -U \'' + user + '\' -d \'' + schema + '\' -a -f ' + path,
                    'export PGCLIENTENCODING=\'' + iso + '\'; psql ' + con_string + ' -a -f ' + path,
                    stderr=subprocess.STDOUT, shell=True)
                print result
            except:
                try:
                    result = subprocess.check_output(
                        #'export PGPASSWORD=\'' + password + '\'; export PGCLIENTENCODING=; psql -h \'' + host + '\' -U \'' + user + '\' -d \'' + schema + '\' -a -f ' + path,
                        'export PGCLIENTENCODING=; psql ' + con_string + ' -a -f ' + path,
                        stderr=subprocess.STDOUT, shell=True)
                    print result
                except subprocess.CalledProcessError as e:
                    print e.output
                    print 'Error running command: ' + '"' + e.cmd + '"' + ' see above shell error'
                    print 'Return code: ' + str(e.returncode)
                    return e.returncode, e.cmd

        def execute_command(self):

            if not request.method == 'POST':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic function - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            if not request.body:
                log.info('API basic function - error detected, no request body received')
                abort(400, 'No body data received')

            content_type = request.headers.get('Content-Type', '')

            if not content_type.startswith('text/plain'):
                log.info('API basic function - error detected, invalid content type')
                abort(415, 'Content-Type should be text/plain')

            command = request.body
            init_path = request.params.get('init_path', '')
            env_path = request.params.get('env_path', '')

            log.info('API basic function execute_command - Validations ok, execute command')

            if not init_path and not env_path:
                result = subprocess.check_output(shlex.split(command), preexec_fn=os.setsid)
                print result
            elif not init_path:
                newEnv = os.environ.copy()
                newEnv['PATH'] = env_path
                result = subprocess.check_output(shlex.split(command), env=newEnv, preexec_fn=os.setsid)
                print result
            elif not env_path:
                result = subprocess.check_output(shlex.split(command), cwd=init_path, preexec_fn=os.setsid)
                print result
            else:
                newEnv = os.environ.copy()
                newEnv['PATH'] = env_path
                result = subprocess.check_output(shlex.split(command), cwd=init_path, env=newEnv,
                                                     preexec_fn=os.setsid)
            print result

        def add_file(self):
            if not request.method == 'POST':
                log.info('API basic function - error detected, incorrect method used in call')
                abort(405, 'Method not allowed')

            if not c.userobj:
                log.info('API basic function - error detected, need user login')
                abort(403, 'Forbidden, need user login')

            if not c.userobj.sysadmin:
                log.info('API basic function - error detected, need API-Key')
                abort(403, 'Forbidden, need API-Key')

            if not request.body:
                log.info('API basic function - error detected, no request body received')
                abort(400, 'No body data received')

            content_type = request.headers.get('Content-Type', '')

            if not content_type.startswith('text/plain'):
                log.info('API basic function - error detected, invalid content type')
                abort(415, 'Content-Type should be text/plain')

            content = request.body
            file_path = request.params.get('file_path', '')
            
            if not file_path:
                log.info('API basic function - error detected, no param file_path received')
                abort(400, 'No param file_path received')

            log.info('API basic function execute_command - Validations ok, execute command')

            if file_path and content:
                self.create_file(file_path,content)
