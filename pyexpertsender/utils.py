import xml.etree.ElementTree as ET

xsi = 'http://www.w3.org/2001/XMLSchema-instance'
xs = 'http://www.w3.org/2001/XMLSchema'


def camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate_entity(data_dict, data_type, parent, name='Data'):
        data = ET.SubElement(parent, camel_case(name))
        data.set('xsi:type', data_type)

        if isinstance(data_dict, dict):
            for key, value in data_dict.iteritems():
                if isinstance(value, dict):
                    generate_entity(value['data'], value['type'], data, key)
                elif isinstance(value, list):
                    for item in value:
                        generate_entity(item, data_type, data, key)
                else:
                    ET.SubElement(data, camel_case(key)).text = unicode(value)
        else:
            ET.SubElement(data, camel_case(name)).text = unicode(data_dict)
        return data


def generate_request_xml(api_key, data_type, dict_tree):
    root = ET.Element('ApiRequest')
    root.set('xmlns:xsi', xsi)
    root.set('xmlns:xs', xs)
    api_key_element = ET.SubElement(root, 'ApiKey')
    api_key_element.text = api_key
    generate_entity(dict_tree, data_type, root)

    return ET.tostring(root)
