import six
from kubernetes.client import ApiClient

class CoreAppApiV1(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
    def call_api_get_controller(self,url, **kwargs):
        local_var_params = locals()
        all_params = ['pretty', 'allow_watch_bookmarks', '_continue', 'field_selector', 'label_selector', 'limit', 'resource_version', 'timeout_seconds', 'watch']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_namespace" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'pretty' in local_var_params:
            query_params.append(('pretty', local_var_params['pretty']))  # noqa: E501
        if 'allow_watch_bookmarks' in local_var_params:
            query_params.append(('allowWatchBookmarks', local_var_params['allow_watch_bookmarks']))  # noqa: E501
        if '_continue' in local_var_params:
            query_params.append(('continue', local_var_params['_continue']))  # noqa: E501
        if 'field_selector' in local_var_params:
            query_params.append(('fieldSelector', local_var_params['field_selector']))  # noqa: E501
        if 'label_selector' in local_var_params:
            query_params.append(('labelSelector', local_var_params['label_selector']))  # noqa: E501
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'resource_version' in local_var_params:
            query_params.append(('resourceVersion', local_var_params['resource_version']))  # noqa: E501
        if 'timeout_seconds' in local_var_params:
            query_params.append(('timeoutSeconds', local_var_params['timeout_seconds']))  # noqa: E501
        if 'watch' in local_var_params:
            query_params.append(('watch', local_var_params['watch']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/yaml', 'application/vnd.kubernetes.protobuf', 'application/json;stream=watch', 'application/vnd.kubernetes.protobuf;stream=watch'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerToken']  # noqa: E501
        return self.api_client.call_api(
            url, 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='V1NamespaceList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_daemonsets_by_name_with_http_info(self,name,**kwargs):
        return self.call_api_get_controller("/apis/apps/v1/namespaces/default/deployments/"+name)

    def list_daemonsets_by_name(self,name,**kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_daemonsets_by_name_with_http_info(name,**kwargs)
        else:
            (data) = self.list_daemonsets_by_name_with_http_info(name,**kwargs)
            return data