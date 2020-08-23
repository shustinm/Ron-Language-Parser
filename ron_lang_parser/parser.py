from .format import MethodDescription
from lxml import etree
from xml_dataclasses import dump, XmlDataclass


def str_to_xml(s: str):
    xml_root = MethodDescription(s)
    xml_element = dump(xml_root, 'Method', {})    
    return etree.tostring(xml_element, encoding='unicode', pretty_print=True)

