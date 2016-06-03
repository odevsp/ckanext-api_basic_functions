import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class Api_Basic_FunctionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'api_basic_functions')

    def before_map(self, map):
        map.connect('/api_basic/reindex_solr',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='reindex_solr')
        map.connect('/api_basic/clear_index_solr',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='clear_index_solr')
        map.connect('/api_basic/execute_query',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='execute_query')
        map.connect('/api_basic/execute_script_sql',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='execute_script_sql')
        map.connect('/api_basic/execute_command',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='execute_command')
        map.connect('/api_basic/add_file',
                controller='ckanext.api_basic_functions.controller:Resource_api_basic_functionsController',
                action='add_file')
        return map
