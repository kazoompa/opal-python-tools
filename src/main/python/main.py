import subprocess
import json
import os


class Main:
  HOST = "https://opal.maelstrom-research.org:8443"
  USR = "rhaeri"
  PWD = "G3p!Kaz66mpa"

  def run(self):
    # self.find_variable_taxonomy(self.get_datasources(), 'Mlstr_cogscale', 'Emotional', 'NPI')
    self.validate_variable_taxonomies()

  def find_taxonomy_info(self, taxonomies, taxonomyName, vocabularyName, termName):
    for taxonomy in taxonomies:
      if taxonomy['name'] == taxonomyName:
        for vocabulary in taxonomy['vocabularies']:
          if vocabulary['name'] == vocabularyName:
            for term in vocabulary['terms']:
              if term['name'] == termName:
                return True

    return False

  def validate_variable_taxonomies(self):
    taxonomies = self.get_taxonomies()
    dsData = self.get_datasource('study-datasets')
    print "Variables tagged with invalid taxonomies"
    print "Dataset\tTable\tVariable\tTaxonomy\tVocabulary\tTerm"

    for datasource in dsData.iterkeys():
      for table in dsData[datasource]:
        variables = self.get_variables(datasource, table)
        for variable in variables:
          if 'attributes' in variable:
            for attribute in variable['attributes']:
              if 'namespace' in attribute:
                taxonomyName = attribute['namespace']
                vocabularyName = attribute['name']
                termName = attribute['value']
                if not self.find_taxonomy_info(self.get_taxonomies(), taxonomyName, vocabularyName, termName):
                  print "%s\t%s\t%s\t%s\t%s\t%s" \
                        % ( datasource, table, variable['name'], taxonomyName, vocabularyName, termName)

  def get_taxonomies(self):
    ws = "/system/conf/taxonomies"
    cmd = ["opal", "rest", ws, "-o", Main.HOST, "-u", Main.USR, "-p", Main.PWD, "-j"]
    dumpProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return json.loads(dumpProcess.communicate()[0])

  def get_variables(self, datasource, table):
    ws = "/datasource/%s/table/%s/variables" % (datasource, table)
    cmd = ["opal", "rest", ws, "-o", Main.HOST, "-u", Main.USR, "-p", Main.PWD, "-j"]
    dumpProcess = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return json.loads(dumpProcess.communicate()[0])


  def get_datasource(self, datasourceName):
    dumpCommand = ["opal", "rest", "/datasource/%s" % datasourceName , "-o", "https://opal.maelstrom-research.org:8443", "-u", "rhaeri",
                   "-p", "G3p!Kaz66mpa", "-j"]
    dumpProcess = subprocess.Popen(dumpCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dumpOutput = dumpProcess.communicate()[0]
    ds = {}
    ds[datasourceName] = json.loads(dumpOutput)['table']
    return ds

  def get_datasources(self):
    dumpCommand = ["opal", "rest", "/datasources", "-o", "https://opal.maelstrom-research.org:8443", "-u", "rhaeri",
                   "-p", "G3p!Kaz66mpa", "-j"]
    dumpProcess = subprocess.Popen(dumpCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    dumpOutput = dumpProcess.communicate()[0]
    # print dumpOutput
    datasources = json.loads(dumpOutput)
    dsNames = {}

    for ds in datasources:
      if 'table' in ds:
        dsNames[os.path.basename(ds['link'])] = ds['table']

    return dsNames


if __name__ == "__main__":
  Main().run()


