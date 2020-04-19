from pprint import pprint
import csv
import re
from itertools import zip_longest


def refine_phone_number(in_str: str) -> str:
    """
    out format:
    +7(999)999-99-99
    +7(999)999-99-99 доб.9999;
    """
    pref = '+7'
    phone_regex_pattern = r"(?P<prefix>8|\+7)\s*\(*(?P<code>\d{3})[)-]*\s*(?P<part1>\d{3})[-\s]*(?P<part2>\d{2})[-\s]*(?P<part3>\d{2})[\s,(]*(?:доб)*(?:\.\s)*(?P<ext>\d*)"
    in_str = in_str.strip()
    out_phone = ''
    phone_regex = re.compile(phone_regex_pattern)

    res = phone_regex.match(in_str)
    if res and len(res.groups()) == 6:
        out_phone = '{}({}){}-{}-{}'.format(pref,res.group("code"),res.group("part1"),res.group("part2"),res.group("part3"))
        if res.group('ext'):
            out_phone +=' доб.{}'.format(res.group("ext"))
    return out_phone


def merge_duplicates(contacts):
    """
    Merge duplicate contacts automatically by simple logic.
    Function compares contacts by last name.
    Manual review of conflicts not implemented! Proper data can be lost!
    :param contacts:
    :return:
    """
    last_names = dict()  # dict contains list of indexes of contacts with the same last name. Key is last name
    for i in range(len(contacts)):  # fill in last_name dict
        name = contacts[i][0]
        if name in last_names.keys():
            last_names[name].append(i)
        else:
            last_names[name] = [i]
    ref_contacts = []
    for i in range(len(contacts)):  # merge duplicates.
        name = contacts[i][0]
        if len(last_names.get(name)) > 1:
            dups = [contacts[j] for j in last_names.get(name)]
            ref_contacts.append([next((d for d in di if d), '') for di in zip(*dups)])
            last_names[name] = []
        elif len(last_names.get(name)) == 1:
            ref_contacts.append(contacts[i])
    return ref_contacts


with open("phonebook_raw.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
    header = [next(reader)]
    contacts = list(reader)
    contacts_refined = []

    for contact in contacts:
        fio = str(contact[0]).strip().split()+str(contact[1]).strip().split()+str(contact[2]).strip().split()
        fio = [i[0] for i in list(zip_longest(fio, ['']*3, fillvalue=''))]
        contacts_refined.append(fio + [str(contact[3]).strip(),str(contact[4]).strip()] + [refine_phone_number(contact[-2])] + [str(contact[6]).strip()])
    contacts_refined = merge_duplicates(contacts_refined)

with open("phonebook.csv", "w", encoding='utf-8', newline='\n') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(header)
  datawriter.writerows(contacts_refined)