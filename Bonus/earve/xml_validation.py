from lxml import etree

def validate_xml(xml_file, xsd_file):
    # Чтение XSD схемы
    with open(xsd_file, 'rb') as f:
        xsd_doc = etree.XML(f.read())

    # Создание XMLSchema объекта
    xsd_schema = etree.XMLSchema(xsd_doc)

    # Чтение XML файла
    with open(xml_file, 'rb') as f:
        xml_doc = etree.XML(f.read())

    # Валидация XML против XSD схемы
    if xsd_schema.validate(xml_doc):
        print("XML файл валиден.")
    else:
        print("XML файл не валиден!")
        for error in xsd_schema.error_log:
            print(f"Ошибка на строке {error.line}, колонке {error.column}: {error.message}")

# Пример использования
if __name__ == "__main__":
    xml_file = '/Users/elenamin/PycharmProjects/sampling_test/e-arve.xml'
    xsd_file = '/Users/docha/Downloads/e-invoice_ver1.2.EN.xsd'
    validate_xml(xml_file, xsd_file)