#!/usr/bin/env python3

from ccmm.dats.datsobj import DatsObj
import ccmm.dats.util as util
import logging
import sys

# Produce a DATS Material for a single subject/donor.

def get_subject_dats_material(p_subject, gh_subject):
    subj_id = p_subject['SUBJID']['mapped_value']

    # human experimental subject/patient
    subject_sex = DatsObj("Dimension", [
            ("name", DatsObj("Annotation", [("value", "Gender")])),
            ("description", "Gender of the subject"),
            ("identifier", DatsObj("Identifier", [("identifier", "SEX"), ("identifierSource", "GTEx")])),
            ("values", [ p_subject['SEX']['mapped_value'] ])
            ])

    subject_age = DatsObj("Dimension", [
            ("name", DatsObj("Annotation", [("value", "Age range")])),
            ("description", "Age range of the subject"),
            ("identifier", DatsObj("Identifier", [("identifier", "AGE"), ("identifierSource", "GTEx")])),
            ("values", [ p_subject['AGE']['mapped_value'] ])
            ])

    subject_hardy_scale = DatsObj("Dimension", [
            ("name", DatsObj("Annotation", [("value", "Hardy scale")])),
            ("description", "Hardy scale death classification for the subject"),
            ("identifier", DatsObj("Identifier", [("identifier", "DTHHRDY"), ("identifierSource", "GTEx")])),
            ("values", [ p_subject['DTHHRDY']['mapped_value'] ])
            ])

    subject_characteristics = [
        subject_sex,
        subject_age,
        subject_hardy_scale
        ]

    # use URI from GTEx id dump if present
    identifier = subj_id
    if gh_subject is not None:
        identifier = gh_subject['Destination URL']['raw_value']

    # human experimental subject/patient
    subject_material = DatsObj("Material", [
            ("name", subj_id),
            ("identifier", DatsObj("Identifier", [("identifier", identifier)] )),
            ("description", "GTEx subject " + subj_id),
            ("characteristics", subject_characteristics),
            ("taxonomy", util.get_taxon_human()),
            ("roles", util.get_donor_roles())
            ])

    return subject_material

# Produce a dict of DATS subject/donor Materials, indexed by GTEx subject id.

def get_subjects_dats_materials(p_subjects, gh_subjects):
    dats_subjects = {}

    for s in p_subjects:
        # subject phenotype info from GTEx Portal file
        p_subject = p_subjects[s]
        # subject info from GTEx GitHub id dump
        gh_subject = gh_subjects[s]
        subj_id = p_subject['SUBJID']['mapped_value']
        subj_material = get_subject_dats_material(p_subject, gh_subject)
        dats_subjects[subj_id] = subj_material
    
    return dats_subjects
