# GNU GENERAL PUBLIC LICENSE
#
# 2023 Jadson Bonfim Ribeiro <contato@jadsonbr.com.br>
## Versão alterada 2024 Eduardo Soares <edufrancoreis@hotmail.com>

import os
import jpype
import pathlib
from pyreportjasper.config import Config
from pyreportjasper.db import Db
import jpype.imports
from jpype.types import *
from enum import Enum


class Report:
    config = None
    input_file = None
    defaultLocale = None
    initial_input_type = None
    output = None
    
    TypeJava = Enum('TypeJava', [
                             ('BigInteger', 'java.math.BigInteger'),
                             ('Array', 'java.lang.reflect.Array'),
                             ('ArrayList', 'java.util.ArrayList'),
                             ('String', 'java.lang.String'),
                             ('Integer', 'java.lang.Integer'),
                             ('Boolean', 'java.lang.Boolean'),
                             ('Float', 'java.lang.Float'), 
                             ('Date', 'java.util.Date'),
                        ])
  

    def __init__(self, config: Config, input_file):
        self.SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
        self.LIB_PATH = os.path.join(self.SCRIPT_DIR, 'libs')
        self.JDBC_PATH = os.path.join(self.LIB_PATH, 'jdbc')
        if not os.path.exists(self.LIB_PATH):
            raise NameError('Library directory not found at {0}'.format(self.LIB_PATH))
        self.config = config
        if not jpype.isJVMStarted():
            classpath = [
                os.path.join(self.LIB_PATH, "*"),
                os.path.join(self.JDBC_PATH, "*"),
            ]

            if self.config.resource and os.path.isdir(self.config.resource):
                classpath.append(os.path.join(self.config.resource, "*"))

            if self.config.jvm_classpath:
                classpath.append(self.config.jvm_classpath)

            if self.config.jvm_classpath is None:
                jvm_args = [
                    "-Djava.system.class.loader=org.update4j.DynamicClassLoader",
                    "-Dlog4j.configurationFile={}".format(
                        os.path.join(self.LIB_PATH, 'log4j2.xml')),
                    "-XX:InitialHeapSize=512M",
                    "-XX:CompressedClassSpaceSize=64M",
                    "-XX:MaxMetaspaceSize=128M",                            
                    "-Xmx{}".format(self.config.jvm_maxmem),
                ]
                jvm_args.extend(self.config.jvm_opts or ())
                jpype.startJVM(*jvm_args, classpath=classpath)

        self.Locale = jpype.JPackage('java').util.Locale
        self.String = jpype.JPackage('java').lang.String
        self.jvJRLoader = jpype.JPackage('net').sf.jasperreports.engine.util.JRLoader
        self.JasperReport = jpype.JPackage('net').sf.jasperreports.engine.JasperReport
        self.JasperPrint = jpype.JPackage('net').sf.jasperreports.engine.JasperPrint
        self.JRXmlLoader = jpype.JPackage('net').sf.jasperreports.engine.xml.JRXmlLoader
        self.jvJasperCompileManager = jpype.JPackage('net').sf.jasperreports.engine.JasperCompileManager
        self.LocaleUtils = jpype.JPackage('org').apache.commons.lang.LocaleUtils
        self.Locale = jpype.JPackage('java').util.Locale
        self.jvJasperFillManager = jpype.JPackage('net').sf.jasperreports.engine.JasperFillManager
        self.JREmptyDataSource = jpype.JPackage('net').sf.jasperreports.engine.JREmptyDataSource
        self.JasperExportManager = jpype.JPackage('net').sf.jasperreports.engine.JasperExportManager
        self.FileOutputStream = jpype.JPackage('java').io.FileOutputStream
        self.JRRtfExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRRtfExporter
        self.SimpleExporterInput = jpype.JPackage('net').sf.jasperreports.export.SimpleExporterInput
        self.SimpleWriterExporterOutput = jpype.JPackage('net').sf.jasperreports.export.SimpleWriterExporterOutput
        self.JRDocxExporter = jpype.JPackage('net').sf.jasperreports.engine.export.ooxml.JRDocxExporter
        self.JRPptxExporter = jpype.JPackage('net').sf.jasperreports.engine.export.ooxml.JRPptxExporter
        self.JRXlsxExporter = jpype.JPackage('net').sf.jasperreports.engine.export.ooxml.JRXlsxExporter
        self.SimpleOutputStreamExporterOutput = jpype.JPackage('net').sf.jasperreports.export.SimpleOutputStreamExporterOutput
        self.JROdsExporter = jpype.JPackage('net').sf.jasperreports.engine.export.oasis.JROdsExporter
        self.JROdtExporter = jpype.JPackage('net').sf.jasperreports.engine.export.oasis.JROdtExporter
        self.HtmlExporter = jpype.JPackage('net').sf.jasperreports.engine.export.HtmlExporter
        self.SimpleHtmlExporterOutput = jpype.JPackage('net').sf.jasperreports.export.SimpleHtmlExporterOutput
        self.JRXmlExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRXmlExporter
        self.SimpleXmlExporterOutput = jpype.JPackage('net').sf.jasperreports.export.SimpleXmlExporterOutput
        self.HashMap = jpype.JPackage('java').util.HashMap
        self.JRXlsExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRXlsExporter
        self.SimpleXlsReportConfiguration = jpype.JPackage('net').sf.jasperreports.export.SimpleXlsReportConfiguration
        self.JRXlsMetadataExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRXlsMetadataExporter
        self.SimpleXlsMetadataReportConfiguration = jpype.JPackage('net').sf.jasperreports.export.SimpleXlsMetadataReportConfiguration
        self.JRXlsxExporter = jpype.JPackage('net').sf.jasperreports.engine.export.ooxml.JRXlsxExporter
        self.SimpleXlsxReportConfiguration = jpype.JPackage('net').sf.jasperreports.export.SimpleXlsxReportConfiguration
        self.JRCsvExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRCsvExporter
        self.SimpleCsvExporterConfiguration = jpype.JPackage('net').sf.jasperreports.export.SimpleCsvExporterConfiguration
        self.JRCsvMetadataExporter = jpype.JPackage('net').sf.jasperreports.engine.export.JRCsvMetadataExporter
        self.SimpleCsvMetadataExporterConfiguration = jpype.JPackage('net').sf.jasperreports.export.SimpleCsvMetadataExporterConfiguration
        self.JRSaver = jpype.JPackage('net').sf.jasperreports.engine.util.JRSaver
        self.File = jpype.JPackage('java').io.File
        self.ByteArrayInputStream = jpype.JPackage('java').io.ByteArrayInputStream
        self.ByteArrayOutputStream = jpype.JPackage('java').io.ByteArrayOutputStream
        self.ApplicationClasspath = jpype.JPackage('br').com.acesseonline.classpath.ApplicationClasspath

        if self.config.useJaxen:
            self.DefaultJasperReportsContext = jpype.JPackage('net').sf.jasperreports.engine.DefaultJasperReportsContext
            self.context = self.DefaultJasperReportsContext.getInstance()
            self.JRPropertiesUtil = jpype.JPackage('net').sf.jasperreports.engine.JRPropertiesUtil
            self.JRPropertiesUtil.getInstance(self.context).setProperty(
                "net.sf.jasperreports.xpath.executer.factory",
                "net.sf.jasperreports.engine.util.xml.JaxenXPathExecuterFactory"
            )

        # Lendo o arquivo de entrada (bytes ou caminho)
        if isinstance(input_file, str) or isinstance(input_file, pathlib.PurePath):
            if not os.path.isfile(input_file):
                raise NameError('input_file is not file.')
            with open(input_file, 'rb') as file:
                self.input_file = file.read()
        elif isinstance(input_file, bytes):
            self.input_file = input_file
        else:
            raise NameError('input_file does not have a valid type. Please enter the file path or its bytes')

        self.defaultLocale = self.Locale.getDefault()

        if self.config.has_resource():
            self.add_jar_class_path(self.config.resource)

            if os.path.isdir(self.config.resource):
                try:
                    res = self.File(self.config.resource)
                    self.ApplicationClasspath.add(res)
                except Exception as ex:
                    raise NameError(
                        'It was not possible to add the path {0} to the Class Path: ERROR: {1}' \
                        .format(self.config.resource, str(ex))
                    )

        if self.config.has_jdbc_dir():
            self.add_jar_class_path(self.config.jdbcDir)

        # Tenta carregar como .jasper ou .jrprint
        try:
            j_object = self.jvJRLoader.loadObject(self.ByteArrayInputStream(self.input_file))
            cast_error = True
            try:
                self.jasper_report = jpype.JObject(j_object, self.JasperReport)
                cast_error = False
                self.initial_input_type = 'JASPER_REPORT'
            except:
                pass
            try:
                self.jasper_print = jpype.JObject(j_object, self.JasperPrint)
                cast_error = False
                self.initial_input_type = 'JASPER_PRINT'
            except:
                pass

            if cast_error:
                raise NameError('input file: {0} is not of a valid type'.format(self.input_file))
        except Exception:
            # Se não for .jasper/.jrprint, tenta compilar .jrxml
            try:
                self.jasper_design = self.JRXmlLoader.load(self.ByteArrayInputStream(self.input_file))
                self.initial_input_type = 'JASPER_DESIGN'
                self.compile()
            except Exception as ex:
                raise NameError('input file: {0} is not a valid jrxml file:'.format(str(ex)))

        # Prepara subreports
        self.jasper_subreports = {}
        for subreport_name, subreport_file in self.config.subreports.items():
            try:
                with open(subreport_file, 'rb') as subreport_file_bytes:
                    subreport_jasper_design = self.JRXmlLoader.load(self.ByteArrayInputStream(subreport_file_bytes.read()))
                    ext_sub_report = os.path.splitext(subreport_file)[-1]
                    sub_report_without_ext = os.path.splitext(subreport_file)[0]
                    jasper_file_subreport = str(sub_report_without_ext) + '.jasper'
                    if ext_sub_report == '.jrxml':
                        print("Compiling: {}".format(subreport_file))
                        self.jvJasperCompileManager.compileReportToFile(subreport_file, jasper_file_subreport)
                    self.jasper_subreports[subreport_name] = self.jvJasperCompileManager.compileReport(subreport_jasper_design)
            except Exception:
                raise NameError('input file: {0} is not a valid jrxml file'.format(subreport_name))

    def compile(self):
        self.jasper_report = self.jvJasperCompileManager.compileReport(self.jasper_design)
        if self.config.is_write_jasper():
            if self.config.output:
                base = os.path.splitext(self.config.output)[0]
            else:
                base = os.path.splitext(self.input_file)[0]
            new_input = base + ".jasper"
            self.JRSaver.saveObject(self.jasper_report, new_input)
            self.config.input = new_input

    def compile_to_file(self):
        if self.initial_input_type == "JASPER_DESIGN":
            try:
                base = os.path.splitext(self.config.output)[0]
                self.JRSaver.saveObject(self.jasper_report, base + ".jasper")
            except Exception as ex:
                raise NameError('outputFile {}.jasper could not be written: {}'.format(base, ex))
        else:
            raise NameError('input file: {0} is not a valid jrxml file'.format(self.input_file))

    def fill(self):
        self.fill_internal()

    def fill_internal(self):
        parameters = self.HashMap()

        # Converte params para tipos Java (quando configurado)
        for key, value in self.config.params.items():
            if isinstance(value, dict):
                type_var = value.get('type')
                if isinstance(type_var, self.TypeJava):
                    type_instance_java = type_var.value
                    type_name = type_var.name
                    if type_instance_java:
                        if type_name == 'BigInteger':
                            val = str(value.get('value'))
                            value_java = jpype.JClass(type_instance_java)(val)
                        elif type_name == 'Array':
                            list_values = value.get('value')
                            first_val = list_values[0]
                            if isinstance(first_val, int):
                                IntArrayCls = JArray(JInt)
                                value_java = IntArrayCls(list_values)
                            elif isinstance(first_val, str):
                                StrArrayCls = JArray(JString)
                                value_java = StrArrayCls(list_values)
                            else:
                                raise NameError('Array type only accepts Int and Str')
                        elif type_name == 'ArrayList':
                            from java.util import ArrayList
                            value_java = ArrayList()
                            for itm in value.get('value'):
                                if isinstance(itm, int):
                                    value_java.add(JInt(itm))
                                elif isinstance(itm, str):
                                    value_java.add(JString(itm))
                                elif isinstance(itm, bool):
                                    value_java.add(JBoolean(itm))
                                elif isinstance(itm, float):
                                    value_java.add(JFloat(itm))
                                else:
                                    raise NameError('ArrayList type only accepts int, str, bool or float')
                        elif type_name == 'String':
                            value_java = jpype.JClass(type_instance_java)(value.get('value'))
                        elif type_name == 'Integer':
                            val = str(value.get('value'))
                            value_java = jpype.JClass(type_instance_java)(val)
                        elif type_name == 'Boolean':
                            if not isinstance(value.get('value'), bool):
                                raise NameError('Parameter {} is not of type bool'.format(key))
                            value_java = jpype.JClass(type_instance_java)(value.get('value'))
                        elif type_name == 'Float':
                            if not isinstance(value.get('value'), float):
                                raise NameError('Parameter {} is not float'.format(key))
                            value_java = jpype.JClass(type_instance_java)(value.get('value'))
                        elif type_name == 'Date':
                            from java.util import Calendar, Date
                            from java.text import SimpleDateFormat
                            format_in = value.get('format_input', 'yyyy-MM-dd')
                            sdf = SimpleDateFormat(format_in)
                            value_java = sdf.parse(value.get('value'))
                        else:
                            raise NameError('Unknown TypeJava: {}'.format(type_name))
                        parameters.put(key, value_java)
                    else:
                        raise NameError('Instance JAVA not locate')
                else:
                    # Se não é TypeJava, insere do jeito que veio
                    parameters.put(key, value)
            else:
                parameters.put(key, value)

        # Carrega subreports
        for subreport_key, subreport in self.jasper_subreports.items():
            parameters.put(subreport_key, subreport)

        try:
            if self.config.locale:
                self.config.locale = self.LocaleUtils.toLocale(self.config.locale)
                self.Locale.setDefault(self.config.locale)

            if self.config.dbType is None:
                empty_data_source = self.JREmptyDataSource()
                self.jasper_print = self.jvJasperFillManager.fillReport(
                    self.jasper_report, parameters, empty_data_source
                )
            elif self.config.dbType == 'csv':
                db = Db()
                ds = db.get_csv_datasource(self.config)
                self.jasper_print = self.jvJasperFillManager.fillReport(self.jasper_report, parameters, ds)
            elif self.config.dbType == 'xml':
                if self.config.xmlXpath is None:
                    self.config.xmlXpath = self.get_main_dataset_query()
                db = Db()
                ds = db.get_xml_datasource(self.config)
                self.jasper_print = self.jvJasperFillManager.fillReport(self.jasper_report, parameters, ds)
            elif self.config.dbType == 'json':
                if self.config.jsonQuery is None:
                    self.config.jsonQuery = self.get_main_dataset_query()
                db = Db()
                ds = db.get_json_datasource(self.config)
                if self.config.jsonLocale:
                    ds.setLocale(self.LocaleUtils.toLocale(self.config.jsonLocale))
                self.jasper_print = self.jvJasperFillManager.fillReport(self.jasper_report, parameters, ds)
            elif self.config.dbType == 'jsonql':
                if self.config.jsonQLQuery is None:
                    self.config.jsonQuery = self.get_main_dataset_query()
                db = Db()
                ds = db.get_jsonql_datasource(self.config)
                self.jasper_print = self.jvJasperFillManager.fillReport(self.jasper_report, parameters, ds)
            else:
                db = Db()
                con = db.get_connection(self.config)
                self.jasper_print = self.jvJasperFillManager.fillReport(self.jasper_report, parameters, con)
                con.close()
        except Exception as ex:
            raise NameError('Erro fill internal: {}'.format(str(ex)))

    # =========================================================================
    # Métodos de exportação - todos retornam bytes
    # =========================================================================

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    def export_pdf(self):
        """Retorna o arquivo PDF em bytes."""
        output_stream = self.ByteArrayOutputStream()
        self.JasperExportManager.exportReportToPdfStream(self.jasper_print, output_stream)
        return output_stream.toByteArray()

    def export_html(self):
        """Retorna o relatório em HTML (string codificada em bytes)."""
        exporter = self.HtmlExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleHtmlExporterOutput(byte_out))

        exporter.exportReport()
        return byte_out.toByteArray()

    def export_rtf(self):
        """Retorna o relatório em RTF (bytes)."""
        exporter = self.JRRtfExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleWriterExporterOutput(byte_out))

        exporter.exportReport()
        return byte_out.toByteArray()

    def export_docx(self):
        """Retorna o relatório em DOCX (bytes)."""
        exporter = self.JRDocxExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_odt(self):
        """Retorna o relatório em ODT (bytes)."""
        exporter = self.JROdtExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_xml(self):
        """Retorna o relatório em XML (bytes)."""
        exporter = self.JRXmlExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        out_xml = self.SimpleXmlExporterOutput(byte_out)
        out_xml.setEmbeddingImages(False)
        exporter.setExporterOutput(out_xml)
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_xls(self):
        """Retorna o relatório em XLS (bytes)."""
        date_formats = self.HashMap()
        date_formats.put("EEE, MMM d, yyyy", "ddd, mmm d, yyyy")

        exporter = self.JRXlsExporter()
        rep_config = self.SimpleXlsReportConfiguration()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))

        rep_config.setDetectCellType(True)
        rep_config.setFormatPatternsMap(date_formats)
        exporter.setConfiguration(rep_config)
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_xls_meta(self):
        """Retorna o relatório em XLS (com metadata) (bytes)."""
        date_formats = self.HashMap()
        date_formats.put("EEE, MMM d, yyyy", "ddd, mmm d, yyyy")

        exporter = self.JRXlsMetadataExporter()
        rep_config = self.SimpleXlsMetadataReportConfiguration()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))

        rep_config.setDetectCellType(True)
        rep_config.setFormatPatternsMap(date_formats)
        exporter.setConfiguration(rep_config)
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_xlsx(self):
        """Retorna o relatório em XLSX (bytes)."""
        date_formats = self.HashMap()
        date_formats.put("EEE, MMM d, yyyy", "ddd, mmm d, yyyy")

        exporter = self.JRXlsxExporter()
        rep_config = self.SimpleXlsxReportConfiguration()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))

        rep_config.setDetectCellType(True)
        rep_config.setFormatPatternsMap(date_formats)
        exporter.setConfiguration(rep_config)
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_csv(self):
        """Retorna o relatório em CSV (bytes)."""
        exporter = self.JRCsvExporter()
        configuration = self.SimpleCsvExporterConfiguration()
        configuration.setFieldDelimiter(self.config.outFieldDel)

        exporter.setConfiguration(configuration)
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleWriterExporterOutput(byte_out, self.config.outCharset))

        exporter.exportReport()
        return byte_out.toByteArray()

    def export_csv_meta(self):
        """Retorna o relatório em CSV (com metadata) (bytes)."""
        exporter = self.JRCsvMetadataExporter()
        configuration = self.SimpleCsvMetadataExporterConfiguration()
        configuration.setFieldDelimiter(self.config.outFieldDel)

        exporter.setConfiguration(configuration)
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleWriterExporterOutput(byte_out, self.config.outCharset))

        exporter.exportReport()
        return byte_out.toByteArray()

    def export_ods(self):
        """Retorna o relatório em ODS (bytes)."""
        exporter = self.JROdsExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_pptx(self):
        """Retorna o relatório em PPTX (bytes)."""
        exporter = self.JRPptxExporter()
        exporter.setExporterInput(self.SimpleExporterInput(self.jasper_print))

        byte_out = self.ByteArrayOutputStream()
        exporter.setExporterOutput(self.SimpleOutputStreamExporterOutput(byte_out))
        exporter.exportReport()

        return byte_out.toByteArray()

    def export_jrprint(self):
        """Retorna o relatório em JRPRINT (bytes)."""
        byte_out = self.ByteArrayOutputStream()
        self.JRSaver.saveObject(self.jasper_print, byte_out)
        return byte_out.toByteArray()


    def get_report_parameters(self):
        """
        Retorna uma lista de objetos JRParameter do report.
        """
        if self.jasper_report is not None:
            return_val = self.jasper_report.getParameters()
            return return_val
        else:
            raise NameError("Parameters could not be read from {}".format(self.input_file))

    def get_main_dataset_query(self):
        """
        Para JSON, JSONQL e outros data types que precisam de query, 
        usar a query principal contida no próprio relatório.
        """
        if self.initial_input_type == "JASPER_DESIGN":
            return self.jasper_design.getMainDesignDataset().getQuery().getText()
        elif self.initial_input_type == "JASPER_REPORT":
            return self.jasper_report.getMainDataset().getQuery().getText()
        else:
            raise NameError('No query for input type: {}'.format(self.initial_input_type))

    def add_jar_class_path(self, dir_or_jar):
        try:
            if os.path.isdir(dir_or_jar):
                jpype.addClassPath(os.path.join(dir_or_jar, "*"))
            elif os.path.splitext(dir_or_jar)[-1] == '.jar':
                jpype.addClassPath(dir_or_jar)
        except Exception as ex:
            raise NameError("Error adding class path: {}".format(ex))
