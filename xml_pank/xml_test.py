import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('statement.xml')

# Get the root element
root = tree.getroot()

# Access the elements and attributes
for child in root:
    print(child.tag, child.attrib)
    for subchild in child:
        print(subchild.tag, subchild.text)

def print_element(element):
    # Выводим имя элемента и его атрибуты
    print(element.tag, element.attrib, element.text)

    # Рекурсивно вызываем эту же функцию для всех дочерних элементов
    for child in element:

        print_element(child)


# Выводим информацию о каждом элементе
print_element(root)

# for child in root:
#     print(child.tag, child.text)
#     for grandchild in child:
#         print(grandchild.tag, grandchild.text)
#         for great_grandchild in grandchild:
#             print(great_grandchild.tag, great_grandchild.text)
