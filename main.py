#!/usr/bin/env python

import getpass
from collections import namedtuple
from lxml import objectify
from project import Project
from importer import Importer

def read_xml_sourcefile(file_name):
  all_text = open(file_name).read()
  return objectify.fromstring(all_text)

#file_name = raw_input('Path to JIRA XML query file: ')
file_name = "export.xml"
all_xml = read_xml_sourcefile(file_name);

jiraProj = "LUCENENET"
#jiraProj = raw_input('JIRA project name to use: ')
us = "bongohrtech"
#us = raw_input('GitHub account name: ')
#repo = raw_input('GitHub project name: ')
repo = "lucenenet"
#user = raw_input('GitHub username: ')
user = "bongohrtech"
#pw = getpass.getpass('GitHub password: ')
pw = "****"

Options = namedtuple("Options", "user passwd account repo")
opts = Options(user=user, passwd=pw, account=us, repo=repo)

project = Project(jiraProj)

for item in all_xml.channel.item:
  project.add_item(item)

project.merge_labels_and_components()
project.prettify()

'''
Steps:
  1. Create any milestones
  2. Create any labels
  3. Create each issue with comments, linking them to milestones and labels
  4: Post-process all comments to replace issue id placeholders with the real ones
'''
importer = Importer(opts, project)

importer.import_milestones()
importer.import_labels()
importer.import_issues()
importer.post_process_comments()